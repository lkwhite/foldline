"""
FIT Folder Scanner

Walks a directory tree to find and parse .fit files
(e.g., from Garmin Express local storage)
"""

import os
from pathlib import Path
from typing import List, Dict, Any, Optional
import hashlib
import logging
from datetime import datetime

try:
    from fitparse import FitFile
except ImportError:
    FitFile = None
    logger.warning("fitparse not available - FIT file parsing will not work")

logger = logging.getLogger(__name__)


def scan_fit_directory(folder_path: str) -> List[str]:
    """
    Recursively scan a directory for .fit files

    Args:
        folder_path: Root directory to scan

    Returns:
        List of absolute paths to .fit files
    """
    logger.info(f"Scanning directory for FIT files: {folder_path}")

    fit_files = []

    if not os.path.exists(folder_path):
        logger.error(f"Directory does not exist: {folder_path}")
        return fit_files

    try:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if file.lower().endswith('.fit'):
                    full_path = os.path.join(root, file)
                    fit_files.append(full_path)
                    logger.debug(f"Found FIT file: {full_path}")

    except Exception as e:
        logger.error(f"Error scanning directory {folder_path}: {e}")

    logger.info(f"Found {len(fit_files)} FIT files in {folder_path}")
    return fit_files


def compute_file_hash(file_path: str) -> str:
    """
    Compute SHA256 hash of a file for deduplication

    Args:
        file_path: Path to the file

    Returns:
        Hex string of SHA256 hash
    """
    hasher = hashlib.sha256()

    with open(file_path, 'rb') as f:
        while chunk := f.read(8192):
            hasher.update(chunk)

    return hasher.hexdigest()


def get_file_metadata(file_path: str) -> Dict[str, Any]:
    """
    Get file metadata (size, modified time) for sync tracking

    Args:
        file_path: Path to the file

    Returns:
        Dict with file_size and modified_time
    """
    stat = os.stat(file_path)
    return {
        "file_size": stat.st_size,
        "modified_time": datetime.fromtimestamp(stat.st_mtime)
    }


def parse_fit_file(file_path: str) -> Dict[str, Any]:
    """
    Parse a single FIT file using fitparse library

    Args:
        file_path: Path to the FIT file

    Returns:
        Dictionary containing parsed data organized by message type
    """
    logger.info(f"Parsing FIT file: {file_path}")

    if FitFile is None:
        logger.error("fitparse library not available")
        return {"error": "fitparse not installed"}

    data = {
        "file_path": file_path,
        "file_hash": compute_file_hash(file_path),
        "sleep_records": [],
        "hrv_records": [],
        "stress_records": [],
        "daily_steps": [],
        "activities": [],
        "sessions": [],
        "records": [],
        "file_info": {}
    }

    try:
        fitfile = FitFile(file_path)
        logger.debug(f"Successfully opened FIT file: {file_path}")

        for record in fitfile.get_messages():
            message_type = record.name

            if message_type == 'file_id':
                # File metadata
                file_info = {}
                for field in record:
                    if field.value is not None:
                        file_info[field.name] = field.value
                data['file_info'] = file_info

            elif message_type == 'monitoring':
                # Daily summaries (steps, calories, etc.)
                monitoring_record = {}
                for field in record:
                    if field.value is not None:
                        monitoring_record[field.name] = field.value
                if monitoring_record:
                    data['daily_steps'].append(monitoring_record)

            elif message_type == 'stress_level':
                # Stress measurements
                stress_record = {}
                for field in record:
                    if field.value is not None:
                        stress_record[field.name] = field.value
                if stress_record:
                    data['stress_records'].append(stress_record)

            elif message_type == 'sleep':
                # Sleep data (rare in FIT files, usually in JSON)
                sleep_record = {}
                for field in record:
                    if field.value is not None:
                        sleep_record[field.name] = field.value
                if sleep_record:
                    data['sleep_records'].append(sleep_record)

            elif message_type == 'hrv':
                # Heart rate variability
                hrv_record = {}
                for field in record:
                    if field.value is not None:
                        hrv_record[field.name] = field.value
                if hrv_record:
                    data['hrv_records'].append(hrv_record)

            elif message_type == 'session':
                # Workout sessions
                session_record = {}
                for field in record:
                    if field.value is not None:
                        session_record[field.name] = field.value
                if session_record:
                    data['sessions'].append(session_record)

            elif message_type == 'activity':
                # Activity summaries
                activity_record = {}
                for field in record:
                    if field.value is not None:
                        activity_record[field.name] = field.value
                if activity_record:
                    data['activities'].append(activity_record)

            elif message_type == 'record':
                # Per-second data during activities
                record_data = {}
                for field in record:
                    if field.value is not None:
                        record_data[field.name] = field.value
                if record_data:
                    data['records'].append(record_data)

        # Log summary of parsed data
        summary = {
            'sleep_records': len(data['sleep_records']),
            'hrv_records': len(data['hrv_records']),
            'stress_records': len(data['stress_records']),
            'daily_steps': len(data['daily_steps']),
            'activities': len(data['activities']),
            'sessions': len(data['sessions']),
            'records': len(data['records'])
        }
        logger.info(f"Parsed FIT file {file_path}: {summary}")

    except Exception as e:
        logger.error(f"Error parsing FIT file {file_path}: {e}")
        data["error"] = str(e)

    return data


def insert_fit_data(parsed_data: Dict[str, Any], db_connection, source: str = "manual") -> int:
    """
    Insert parsed FIT data into the database

    Args:
        parsed_data: Data returned from parse_fit_file()
        db_connection: Database connection

    Returns:
        Number of records inserted
    """
    if not db_connection:
        logger.error("No database connection provided")
        return 0

    if "error" in parsed_data:
        logger.error(f"Cannot insert data with errors: {parsed_data['error']}")
        return 0

    file_hash = parsed_data["file_hash"]
    file_path = parsed_data["file_path"]
    total_inserted = 0

    try:
        # Get file metadata for sync tracking
        metadata = get_file_metadata(file_path)

        # Check if file already imported
        cursor = db_connection.execute(
            "SELECT file_hash FROM imported_files WHERE file_hash = ?",
            (file_hash,)
        )
        if cursor.fetchone():
            logger.info(f"File already imported: {file_path}")
            return 0

        # Insert file tracking record with sync metadata
        db_connection.execute(
            """INSERT INTO imported_files
               (file_hash, file_path, file_type, file_size, modified_time, source, record_count)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (file_hash, file_path, 'fit', metadata['file_size'],
             metadata['modified_time'], source, 0)  # Will update record_count later
        )

        # Insert sleep records
        for i, sleep_record in enumerate(parsed_data.get('sleep_records', [])):
            if 'local_start_time' in sleep_record and 'sleep_time' in sleep_record:
                start_time = sleep_record.get('local_start_time')
                duration_s = sleep_record.get('sleep_time', 0)
                duration_min = duration_s / 60 if duration_s else None

                # Extract date from start_time for the date field
                if hasattr(start_time, 'date'):
                    date = start_time.date()
                else:
                    date = start_time

                # Generate unique ID
                sleep_id = hash(file_hash + f"sleep_{i}") % (2**31)

                db_connection.execute(
                    """INSERT OR REPLACE INTO sleep_records
                       (id, date, start_time, duration_minutes, source_file_hash)
                       VALUES (?, ?, ?, ?, ?)""",
                    (sleep_id, date, start_time, duration_min, file_hash)
                )
                total_inserted += 1

        # Insert HRV records
        for i, hrv_record in enumerate(parsed_data.get('hrv_records', [])):
            if 'timestamp' in hrv_record and 'rmssd' in hrv_record:
                timestamp = hrv_record['timestamp']
                date = timestamp.date() if hasattr(timestamp, 'date') else timestamp

                # Generate unique ID
                hrv_id = hash(file_hash + f"hrv_{i}") % (2**31)

                db_connection.execute(
                    """INSERT OR REPLACE INTO hrv_records
                       (id, date, hrv_value, measurement_type, source_file_hash)
                       VALUES (?, ?, ?, ?, ?)""",
                    (hrv_id, date, hrv_record['rmssd'], 'rmssd', file_hash)
                )
                total_inserted += 1

        # Insert stress records
        for i, stress_record in enumerate(parsed_data.get('stress_records', [])):
            if 'stress_level_time' in stress_record and 'stress_level_value' in stress_record:
                # Generate unique ID
                stress_id = hash(file_hash + f"stress_{i}") % (2**31)

                db_connection.execute(
                    """INSERT INTO stress_records
                       (id, timestamp, stress_level, source_file_hash)
                       VALUES (?, ?, ?, ?)""",
                    (stress_id, stress_record['stress_level_time'], stress_record['stress_level_value'], file_hash)
                )
                total_inserted += 1

        # Insert daily steps from monitoring records
        for monitoring_record in parsed_data.get('daily_steps', []):
            if 'timestamp' in monitoring_record and 'steps' in monitoring_record:
                timestamp = monitoring_record['timestamp']
                date = timestamp.date() if hasattr(timestamp, 'date') else timestamp

                # Use INSERT OR IGNORE for DuckDB, then UPDATE if needed
                try:
                    db_connection.execute(
                        """INSERT INTO daily_steps
                           (date, step_count, distance_meters, calories, source_file_hash)
                           VALUES (?, ?, ?, ?, ?)""",
                        (date,
                         monitoring_record.get('steps', 0),
                         monitoring_record.get('distance'),
                         monitoring_record.get('active_calories'),
                         file_hash)
                    )
                    total_inserted += 1
                except:
                    # If insert fails due to duplicate, update instead
                    db_connection.execute(
                        """UPDATE daily_steps SET
                           step_count = ?, distance_meters = ?, calories = ?,
                           source_file_hash = ?, imported_at = CURRENT_TIMESTAMP
                           WHERE date = ?""",
                        (monitoring_record.get('steps', 0),
                         monitoring_record.get('distance'),
                         monitoring_record.get('active_calories'),
                         file_hash,
                         date)
                    )
                    # Don't increment total_inserted for updates

        # Insert activities from sessions
        for i, session in enumerate(parsed_data.get('sessions', [])):
            if 'start_time' in session:
                # Generate unique ID using file hash and index
                session_id = hash(file_hash + str(i)) % (2**31)  # Ensure positive 32-bit int

                db_connection.execute(
                    """INSERT INTO activities
                       (id, start_time, activity_type, duration_seconds, distance_meters,
                        avg_hr, max_hr, training_load, source_file_hash)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (session_id,
                     session.get('start_time'),
                     session.get('sport'),
                     session.get('total_elapsed_time'),
                     session.get('total_distance'),
                     session.get('avg_heart_rate'),
                     session.get('max_heart_rate'),
                     session.get('training_load_peak', 0),
                     file_hash)
                )
                total_inserted += 1

        # Update record count in imported_files
        db_connection.execute(
            "UPDATE imported_files SET record_count = ? WHERE file_hash = ?",
            (total_inserted, file_hash)
        )

        # Commit transaction
        db_connection.commit()
        logger.info(f"Inserted {total_inserted} records from {file_path}")

    except Exception as e:
        logger.error(f"Error inserting data from {file_path}: {e}")
        try:
            db_connection.rollback()
        except:
            pass  # Rollback may not be available in DuckDB
        return 0

    return total_inserted


def process_fit_folder(folder_path: str, db_connection) -> Dict[str, Any]:
    """
    Complete pipeline to process a FIT folder

    1. Scan for FIT files
    2. Parse each file
    3. Deduplicate based on hash
    4. Insert into DB
    5. Return summary

    Args:
        folder_path: Directory containing FIT files
        db_connection: Database connection

    Returns:
        Summary of processing results
    """
    logger.info(f"Processing FIT folder: {folder_path}")

    summary = {
        "files_found": 0,
        "files_processed": 0,
        "total_records": 0,
        "duplicates_skipped": 0,
        "errors": 0,
        "error_files": []
    }

    try:
        # 1. Scan for FIT files
        fit_files = scan_fit_directory(folder_path)
        summary["files_found"] = len(fit_files)

        if not fit_files:
            logger.info("No FIT files found in directory")
            return summary

        # 2. Process each FIT file
        for file_path in fit_files:
            try:
                logger.info(f"Processing file: {file_path}")

                # Parse the FIT file
                parsed_data = parse_fit_file(file_path)

                if "error" in parsed_data:
                    logger.error(f"Failed to parse {file_path}: {parsed_data['error']}")
                    summary["errors"] += 1
                    summary["error_files"].append({
                        "file": file_path,
                        "error": parsed_data["error"]
                    })
                    continue

                # Insert data into database
                records_inserted = insert_fit_data(parsed_data, db_connection)

                if records_inserted == 0:
                    # Check if it was a duplicate
                    file_hash = parsed_data["file_hash"]
                    cursor = db_connection.execute(
                        "SELECT file_hash FROM imported_files WHERE file_hash = ?",
                        (file_hash,)
                    )
                    if cursor.fetchone():
                        summary["duplicates_skipped"] += 1
                        logger.info(f"Skipped duplicate file: {file_path}")
                    else:
                        logger.warning(f"No records extracted from file: {file_path}")
                else:
                    summary["total_records"] += records_inserted
                    summary["files_processed"] += 1

            except Exception as e:
                logger.error(f"Error processing file {file_path}: {e}")
                summary["errors"] += 1
                summary["error_files"].append({
                    "file": file_path,
                    "error": str(e)
                })

        # Final summary log
        logger.info(f"Folder processing complete: {summary}")

    except Exception as e:
        logger.error(f"Error processing folder {folder_path}: {e}")
        summary["errors"] += 1
        summary["error_files"].append({
            "file": folder_path,
            "error": str(e)
        })

    return summary
