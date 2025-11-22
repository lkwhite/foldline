"""
Sync Engine

Handles incremental synchronization of Garmin Express device folders.

Implements CONTINUAL_SYNC_SPEC.md §3.4 Folder Scanning Algorithm:
1. Recursively walk subdirectories
2. Identify files where:
   - Extension matches .fit or .FIT
   - File has not been ingested (checked via file_hash)
   - Or file has changed (size/timestamp/hash differs)
3. Pass new/updated files to FIT parser

Never writes to Garmin Express folders (read-only).
"""

import os
from pathlib import Path
from typing import Dict, Any, List, Optional
import logging
from datetime import datetime

# Import from existing modules
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from ingestion.fit_folder import (
    scan_fit_directory,
    compute_file_hash,
    get_file_metadata,
    parse_fit_file,
    insert_fit_data
)

logger = logging.getLogger(__name__)


def get_last_sync_time(device_id: str, db_connection) -> Optional[datetime]:
    """
    Get the last successful sync time for a device

    Args:
        device_id: Garmin Express device ID
        db_connection: Database connection

    Returns:
        Datetime of last sync, or None if never synced
    """
    try:
        cursor = db_connection.execute(
            "SELECT last_sync_at FROM garmin_express_devices WHERE device_id = ?",
            (device_id,)
        )
        row = cursor.fetchone()
        if row and row[0]:
            return datetime.fromisoformat(row[0]) if isinstance(row[0], str) else row[0]
    except Exception as e:
        logger.error(f"Error getting last sync time for device {device_id}: {e}")

    return None


def update_last_sync_time(device_id: str, db_connection):
    """
    Update the last_sync_at timestamp for a device

    Args:
        device_id: Garmin Express device ID
        db_connection: Database connection
    """
    try:
        db_connection.execute(
            """UPDATE garmin_express_devices
               SET last_sync_at = CURRENT_TIMESTAMP
               WHERE device_id = ?""",
            (device_id,)
        )
        db_connection.commit()
    except Exception as e:
        logger.error(f"Error updating last sync time for device {device_id}: {e}")


def is_file_changed(file_path: str, db_connection) -> bool:
    """
    Check if a file has changed since last import

    Args:
        file_path: Path to the file
        db_connection: Database connection

    Returns:
        True if file is new or changed, False if unchanged
    """
    file_hash = compute_file_hash(file_path)
    metadata = get_file_metadata(file_path)

    try:
        cursor = db_connection.execute(
            """SELECT file_size, modified_time
               FROM imported_files
               WHERE file_hash = ?""",
            (file_hash,)
        )
        row = cursor.fetchone()

        if not row:
            # File is new (not in database)
            logger.debug(f"File is new: {file_path}")
            return True

        stored_size, stored_mtime = row

        # Check if size or modified time changed
        if stored_size != metadata['file_size']:
            logger.info(f"File size changed: {file_path} (was {stored_size}, now {metadata['file_size']})")
            return True

        if stored_mtime != metadata['modified_time']:
            logger.info(f"File modified time changed: {file_path}")
            return True

        # File is unchanged
        logger.debug(f"File unchanged: {file_path}")
        return False

    except Exception as e:
        logger.error(f"Error checking file change status for {file_path}: {e}")
        # On error, treat as changed to be safe
        return True


def sync_garmin_express_device(device_id: str, device_path: str, db_connection) -> Dict[str, Any]:
    """
    Perform incremental sync for a Garmin Express device

    Implements CONTINUAL_SYNC_SPEC.md §3.4 Folder Scanning Algorithm

    Args:
        device_id: Garmin Express device ID
        device_path: Path to device folder
        db_connection: Database connection

    Returns:
        Sync summary with statistics
    """
    logger.info(f"Starting sync for device {device_id} at {device_path}")

    summary = {
        "device_id": device_id,
        "device_path": device_path,
        "sync_start": datetime.now().isoformat(),
        "files_scanned": 0,
        "files_new": 0,
        "files_updated": 0,
        "files_skipped": 0,
        "files_error": 0,
        "total_records": 0,
        "errors": [],
        "sync_end": None,
        "duration_seconds": None
    }

    start_time = datetime.now()

    try:
        # Get last sync time (for logging purposes)
        last_sync = get_last_sync_time(device_id, db_connection)
        logger.info(f"Last sync: {last_sync or 'Never'}")

        # 1. Recursively scan for FIT files
        fit_files = scan_fit_directory(device_path)
        summary["files_scanned"] = len(fit_files)

        if not fit_files:
            logger.info(f"No FIT files found in {device_path}")
            summary["sync_end"] = datetime.now().isoformat()
            summary["duration_seconds"] = (datetime.now() - start_time).total_seconds()
            return summary

        # 2. Process each file (new or changed only)
        for file_path in fit_files:
            try:
                # Check if file is new or changed
                if not is_file_changed(file_path, db_connection):
                    summary["files_skipped"] += 1
                    continue

                # File is new or changed - parse it
                logger.info(f"Processing file: {file_path}")
                parsed_data = parse_fit_file(file_path)

                if "error" in parsed_data:
                    logger.error(f"Failed to parse {file_path}: {parsed_data['error']}")
                    summary["files_error"] += 1
                    summary["errors"].append({
                        "file": file_path,
                        "error": parsed_data["error"]
                    })
                    continue

                # Check if this is a new file or update
                file_hash = parsed_data["file_hash"]
                cursor = db_connection.execute(
                    "SELECT file_hash FROM imported_files WHERE file_hash = ?",
                    (file_hash,)
                )
                is_new = cursor.fetchone() is None

                # Insert data into database
                records_inserted = insert_fit_data(parsed_data, db_connection, source="garmin_express")

                if records_inserted > 0:
                    if is_new:
                        summary["files_new"] += 1
                    else:
                        summary["files_updated"] += 1
                    summary["total_records"] += records_inserted
                    logger.info(f"Processed {file_path}: {records_inserted} records")
                else:
                    # File was parsed but no records extracted
                    summary["files_skipped"] += 1
                    logger.debug(f"No records extracted from {file_path}")

            except Exception as e:
                logger.error(f"Error processing file {file_path}: {e}")
                summary["files_error"] += 1
                summary["errors"].append({
                    "file": file_path,
                    "error": str(e)
                })

        # 3. Update device last_sync_at timestamp
        update_last_sync_time(device_id, db_connection)

        # Final summary
        end_time = datetime.now()
        summary["sync_end"] = end_time.isoformat()
        summary["duration_seconds"] = (end_time - start_time).total_seconds()

        logger.info(f"Sync complete for device {device_id}: "
                   f"{summary['files_new']} new, {summary['files_updated']} updated, "
                   f"{summary['files_skipped']} skipped, {summary['files_error']} errors, "
                   f"{summary['total_records']} total records")

    except Exception as e:
        logger.error(f"Error during sync for device {device_id}: {e}")
        summary["errors"].append({
            "file": device_path,
            "error": str(e)
        })
        summary["sync_end"] = datetime.now().isoformat()
        summary["duration_seconds"] = (datetime.now() - start_time).total_seconds()

    return summary


def register_device(device_id: str, device_path: str, device_name: str, db_connection):
    """
    Register a Garmin Express device in the database

    Args:
        device_id: Garmin Express device ID
        device_path: Path to device folder
        device_name: Device name (or ID if name unavailable)
        db_connection: Database connection
    """
    try:
        # Check if device already exists
        cursor = db_connection.execute(
            "SELECT device_id FROM garmin_express_devices WHERE device_id = ?",
            (device_id,)
        )
        if cursor.fetchone():
            logger.info(f"Device {device_id} already registered, updating path")
            db_connection.execute(
                """UPDATE garmin_express_devices
                   SET device_path = ?, device_name = ?
                   WHERE device_id = ?""",
                (device_path, device_name, device_id)
            )
        else:
            logger.info(f"Registering new device: {device_id}")
            db_connection.execute(
                """INSERT INTO garmin_express_devices
                   (device_id, device_path, device_name, enabled)
                   VALUES (?, ?, ?, TRUE)""",
                (device_id, device_path, device_name)
            )

        db_connection.commit()
        logger.info(f"Device {device_id} registered successfully")

    except Exception as e:
        logger.error(f"Error registering device {device_id}: {e}")
        raise


def get_enabled_devices(db_connection) -> List[Dict[str, Any]]:
    """
    Get list of enabled Garmin Express devices

    Args:
        db_connection: Database connection

    Returns:
        List of device dictionaries
    """
    try:
        cursor = db_connection.execute(
            """SELECT device_id, device_path, device_name, last_sync_at, file_count
               FROM garmin_express_devices
               WHERE enabled = TRUE
               ORDER BY device_name"""
        )
        rows = cursor.fetchall()

        devices = []
        for row in rows:
            devices.append({
                "device_id": row[0],
                "device_path": row[1],
                "device_name": row[2],
                "last_sync_at": row[3],
                "file_count": row[4]
            })

        return devices

    except Exception as e:
        logger.error(f"Error getting enabled devices: {e}")
        return []


def sync_all_enabled_devices(db_connection) -> Dict[str, Any]:
    """
    Sync all enabled Garmin Express devices

    Args:
        db_connection: Database connection

    Returns:
        Summary of all syncs
    """
    logger.info("Syncing all enabled devices...")

    overall_summary = {
        "devices_synced": 0,
        "total_files_new": 0,
        "total_files_updated": 0,
        "total_files_skipped": 0,
        "total_files_error": 0,
        "total_records": 0,
        "device_summaries": []
    }

    devices = get_enabled_devices(db_connection)

    for device in devices:
        logger.info(f"Syncing device: {device['device_name']} ({device['device_id']})")

        summary = sync_garmin_express_device(
            device['device_id'],
            device['device_path'],
            db_connection
        )

        overall_summary["devices_synced"] += 1
        overall_summary["total_files_new"] += summary["files_new"]
        overall_summary["total_files_updated"] += summary["files_updated"]
        overall_summary["total_files_skipped"] += summary["files_skipped"]
        overall_summary["total_files_error"] += summary["files_error"]
        overall_summary["total_records"] += summary["total_records"]
        overall_summary["device_summaries"].append(summary)

    logger.info(f"All devices synced: {overall_summary['devices_synced']} devices, "
               f"{overall_summary['total_records']} total records")

    return overall_summary
