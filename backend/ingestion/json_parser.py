"""
JSON Data Parser for Garmin GDPR Export

Processes various JSON files from Garmin GDPR exports:
- Sleep data (DI_CONNECT/2019-2025/sleep_*.json)
- Daily summaries (DI_CONNECT/UdsFile_2019-2025)
- Fitness assessments (VO2 max, fitness age)
- Hydration logs
- Menstrual cycles
- Body composition data
"""

import os
import json
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime, date
import hashlib

logger = logging.getLogger(__name__)


def compute_file_hash(file_path: str) -> str:
    """Compute SHA256 hash of a JSON file for deduplication"""
    hasher = hashlib.sha256()

    with open(file_path, 'rb') as f:
        while chunk := f.read(8192):
            hasher.update(chunk)

    return hasher.hexdigest()


def parse_date(date_str: str) -> Optional[date]:
    """Parse various date formats found in Garmin JSON files"""
    if not date_str:
        return None

    # Common formats: "2024-01-15", "2024-01-15T08:30:00.0"
    try:
        if 'T' in date_str:
            return datetime.fromisoformat(date_str.replace('Z', '')).date()
        else:
            return datetime.fromisoformat(date_str).date()
    except (ValueError, TypeError):
        logger.warning(f"Could not parse date: {date_str}")
        return None


def parse_timestamp(ts_str: str) -> Optional[datetime]:
    """Parse timestamp formats found in Garmin JSON files"""
    if not ts_str:
        return None

    try:
        # Handle both with and without timezone
        if ts_str.endswith('Z'):
            ts_str = ts_str[:-1] + '+00:00'
        return datetime.fromisoformat(ts_str.replace('Z', ''))
    except (ValueError, TypeError):
        logger.warning(f"Could not parse timestamp: {ts_str}")
        return None


def scan_json_files(folder_path: str, pattern: str = "*.json") -> List[str]:
    """
    Recursively scan directory for JSON files matching pattern

    Args:
        folder_path: Root directory to scan
        pattern: Filename pattern to match

    Returns:
        List of absolute paths to matching JSON files
    """
    json_files = []

    if not os.path.exists(folder_path):
        logger.error(f"Directory does not exist: {folder_path}")
        return json_files

    try:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if file.lower().endswith('.json'):
                    # Apply pattern matching if specific pattern provided
                    if pattern != "*.json":
                        import fnmatch
                        if not fnmatch.fnmatch(file, pattern):
                            continue

                    full_path = os.path.join(root, file)
                    json_files.append(full_path)
                    logger.debug(f"Found JSON file: {full_path}")

    except Exception as e:
        logger.error(f"Error scanning directory {folder_path}: {e}")

    logger.info(f"Found {len(json_files)} JSON files in {folder_path}")
    return json_files


def load_json_file(file_path: str) -> Optional[Dict[str, Any]]:
    """
    Safely load and parse a JSON file

    Args:
        file_path: Path to JSON file

    Returns:
        Parsed JSON data or None if failed
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            logger.debug(f"Successfully loaded JSON from {file_path}")
            return data
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in {file_path}: {e}")
        return None
    except Exception as e:
        logger.error(f"Error loading JSON file {file_path}: {e}")
        return None


def parse_sleep_json(json_data: Dict[str, Any], file_path: str) -> Dict[str, Any]:
    """
    Parse sleep data from Garmin JSON files using field mappings

    Uses field_mappings.py to handle field name variations across
    different GDPR export versions
    """
    logger.info(f"Parsing sleep JSON: {file_path}")

    parsed_data = {
        "file_path": file_path,
        "file_hash": compute_file_hash(file_path),
        "sleep_records": [],
        "error": None
    }

    try:
        from ingestion.field_mappings import map_sleep_record, parse_date, parse_timestamp

        # Use field mappings to extract data
        sleep_record = map_sleep_record(json_data)

        # Extract sleep date
        sleep_date = None

        # Try to get date from calendar_date field
        if "calendar_date" in sleep_record:
            sleep_date = parse_date(sleep_record["calendar_date"])

        # Try to get date from sleep start timestamp
        if not sleep_date and "sleep_start_gmt" in sleep_record:
            start_ts = parse_timestamp(sleep_record["sleep_start_gmt"]) if isinstance(sleep_record["sleep_start_gmt"], str) else sleep_record["sleep_start_gmt"]
            if start_ts:
                sleep_date = start_ts.date()

        # Fallback: extract date from filename
        if not sleep_date:
            filename = os.path.basename(file_path)
            if "sleep_" in filename:
                date_part = filename.replace("sleep_", "").replace(".json", "")
                sleep_date = parse_date(date_part)

        if not sleep_date:
            raise ValueError("Could not determine sleep date from file")

        # Add date to record
        sleep_record["date"] = sleep_date

        # Convert string timestamps to datetime objects if needed
        for ts_field in ["sleep_start_gmt", "sleep_end_gmt"]:
            if ts_field in sleep_record and isinstance(sleep_record[ts_field], str):
                sleep_record[ts_field] = parse_timestamp(sleep_record[ts_field])

        # Only add if we have meaningful data
        if any(sleep_record.get(key) is not None for key in ["deep_sleep_seconds", "light_sleep_seconds", "rem_sleep_seconds"]):
            parsed_data["sleep_records"].append(sleep_record)
            logger.info(f"Parsed sleep record for {sleep_date}: {len(parsed_data['sleep_records'])} total")
        else:
            logger.warning(f"No meaningful sleep data found in {file_path}")

    except Exception as e:
        logger.error(f"Error parsing sleep JSON {file_path}: {e}")
        parsed_data["error"] = str(e)

    return parsed_data


def parse_daily_summary_json(json_data: Dict[str, Any], file_path: str) -> Dict[str, Any]:
    """
    Parse daily summary data from UDS JSON files using field mappings

    Uses field_mappings.py to handle field name variations across
    different GDPR export versions
    """
    logger.info(f"Parsing daily summary JSON: {file_path}")

    parsed_data = {
        "file_path": file_path,
        "file_hash": compute_file_hash(file_path),
        "daily_summaries": [],
        "error": None
    }

    try:
        from ingestion.field_mappings import map_daily_summary_record, parse_date

        # Use field mappings to extract data
        summary_record = map_daily_summary_record(json_data)

        # Extract date
        summary_date = None
        if "calendar_date" in summary_record:
            summary_date = parse_date(summary_record["calendar_date"]) if isinstance(summary_record["calendar_date"], str) else summary_record["calendar_date"]

        if not summary_date:
            raise ValueError("Could not determine summary date from file")

        # Add date to record
        summary_record["date"] = summary_date

        # Only add if we have meaningful data
        if any(summary_record.get(key) is not None for key in ["step_count", "calories_burned", "resting_heart_rate"]):
            parsed_data["daily_summaries"].append(summary_record)
            logger.info(f"Parsed daily summary for {summary_date}")
        else:
            logger.warning(f"No meaningful daily summary data found in {file_path}")

    except Exception as e:
        logger.error(f"Error parsing daily summary JSON {file_path}: {e}")
        parsed_data["error"] = str(e)

    return parsed_data


def insert_sleep_data(parsed_data: Dict[str, Any], db_connection) -> int:
    """
    Insert parsed sleep data into sleep_detailed table

    Args:
        parsed_data: Data returned from parse_sleep_json()
        db_connection: Database connection

    Returns:
        Number of records inserted
    """
    if not db_connection or parsed_data.get("error"):
        return 0

    file_hash = parsed_data["file_hash"]
    file_path = parsed_data["file_path"]
    total_inserted = 0

    try:
        # Check if file already imported
        cursor = db_connection.execute(
            "SELECT file_hash FROM imported_files WHERE file_hash = ?",
            (file_hash,)
        )
        if cursor.fetchone():
            logger.info(f"Sleep file already imported: {file_path}")
            return 0

        # Insert file tracking record
        db_connection.execute(
            """INSERT INTO imported_files (file_hash, file_path, file_type, record_count)
               VALUES (?, ?, ?, ?)""",
            (file_hash, file_path, 'json', 0)
        )

        # Insert sleep records
        for i, sleep_record in enumerate(parsed_data.get("sleep_records", [])):
            sleep_id = hash(file_hash + f"sleep_{i}") % (2**31)

            try:
                # Try INSERT first
                db_connection.execute(
                    """INSERT INTO sleep_detailed
                       (id, date, sleep_start_gmt, sleep_end_gmt, deep_sleep_seconds,
                        light_sleep_seconds, rem_sleep_seconds, awake_sleep_seconds,
                        sleep_window_confirmation_type, average_respiration, lowest_respiration,
                        highest_respiration, average_spo2, lowest_spo2, average_sleep_hr,
                        source_file_hash)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (sleep_id,
                     sleep_record["date"],
                     sleep_record["sleep_start_gmt"],
                     sleep_record["sleep_end_gmt"],
                     sleep_record["deep_sleep_seconds"],
                     sleep_record["light_sleep_seconds"],
                     sleep_record["rem_sleep_seconds"],
                     sleep_record["awake_sleep_seconds"],
                     sleep_record["sleep_window_confirmation_type"],
                     sleep_record["average_respiration"],
                     sleep_record["lowest_respiration"],
                     sleep_record["highest_respiration"],
                     sleep_record["average_spo2"],
                     sleep_record["lowest_spo2"],
                     sleep_record["average_sleep_hr"],
                     file_hash)
                )
                total_inserted += 1

            except Exception as duplicate_error:
                # If duplicate date, update existing record
                if "Duplicate key" in str(duplicate_error) or "UNIQUE constraint failed" in str(duplicate_error):
                    db_connection.execute(
                        """UPDATE sleep_detailed SET
                           sleep_start_gmt = ?, sleep_end_gmt = ?, deep_sleep_seconds = ?,
                           light_sleep_seconds = ?, rem_sleep_seconds = ?, awake_sleep_seconds = ?,
                           sleep_window_confirmation_type = ?, average_respiration = ?,
                           lowest_respiration = ?, highest_respiration = ?, average_spo2 = ?,
                           lowest_spo2 = ?, average_sleep_hr = ?, source_file_hash = ?
                           WHERE date = ?""",
                        (sleep_record["sleep_start_gmt"],
                         sleep_record["sleep_end_gmt"],
                         sleep_record["deep_sleep_seconds"],
                         sleep_record["light_sleep_seconds"],
                         sleep_record["rem_sleep_seconds"],
                         sleep_record["awake_sleep_seconds"],
                         sleep_record["sleep_window_confirmation_type"],
                         sleep_record["average_respiration"],
                         sleep_record["lowest_respiration"],
                         sleep_record["highest_respiration"],
                         sleep_record["average_spo2"],
                         sleep_record["lowest_spo2"],
                         sleep_record["average_sleep_hr"],
                         file_hash,
                         sleep_record["date"])
                    )
                else:
                    raise  # Re-raise if not a duplicate error

        # Update record count
        db_connection.execute(
            "UPDATE imported_files SET record_count = ? WHERE file_hash = ?",
            (total_inserted, file_hash)
        )

        db_connection.commit()
        logger.info(f"Inserted {total_inserted} sleep records from {file_path}")

    except Exception as e:
        logger.error(f"Error inserting sleep data from {file_path}: {e}")
        try:
            db_connection.rollback()
        except:
            pass
        return 0

    return total_inserted


def insert_daily_summary_data(parsed_data: Dict[str, Any], db_connection) -> int:
    """
    Insert parsed daily summary data into daily_summaries table

    Args:
        parsed_data: Data returned from parse_daily_summary_json()
        db_connection: Database connection

    Returns:
        Number of records inserted
    """
    if not db_connection or parsed_data.get("error"):
        return 0

    file_hash = parsed_data["file_hash"]
    file_path = parsed_data["file_path"]
    total_inserted = 0

    try:
        # Check if file already imported
        cursor = db_connection.execute(
            "SELECT file_hash FROM imported_files WHERE file_hash = ?",
            (file_hash,)
        )
        if cursor.fetchone():
            logger.info(f"Daily summary file already imported: {file_path}")
            return 0

        # Insert file tracking record
        db_connection.execute(
            """INSERT INTO imported_files (file_hash, file_path, file_type, record_count)
               VALUES (?, ?, ?, ?)""",
            (file_hash, file_path, 'json', 0)
        )

        # Insert daily summary records
        for i, summary_record in enumerate(parsed_data.get("daily_summaries", [])):
            summary_id = hash(file_hash + f"summary_{i}") % (2**31)

            db_connection.execute(
                """INSERT INTO daily_summaries
                   (id, date, step_count, calories_burned, distance_meters, floors_climbed,
                    active_minutes, sedentary_minutes, min_heart_rate, max_heart_rate,
                    resting_heart_rate, avg_heart_rate, stress_avg, stress_max, stress_min,
                    body_battery_charged, body_battery_drained, body_battery_start, body_battery_end,
                    intensity_minutes_moderate, intensity_minutes_vigorous, source_file_hash)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                   ON CONFLICT (date) DO UPDATE SET
                   step_count = excluded.step_count,
                   calories_burned = excluded.calories_burned,
                   distance_meters = excluded.distance_meters,
                   floors_climbed = excluded.floors_climbed,
                   active_minutes = excluded.active_minutes,
                   sedentary_minutes = excluded.sedentary_minutes,
                   min_heart_rate = excluded.min_heart_rate,
                   max_heart_rate = excluded.max_heart_rate,
                   resting_heart_rate = excluded.resting_heart_rate,
                   avg_heart_rate = excluded.avg_heart_rate,
                   stress_avg = excluded.stress_avg,
                   stress_max = excluded.stress_max,
                   stress_min = excluded.stress_min,
                   body_battery_charged = excluded.body_battery_charged,
                   body_battery_drained = excluded.body_battery_drained,
                   body_battery_start = excluded.body_battery_start,
                   body_battery_end = excluded.body_battery_end,
                   intensity_minutes_moderate = excluded.intensity_minutes_moderate,
                   intensity_minutes_vigorous = excluded.intensity_minutes_vigorous,
                   source_file_hash = excluded.source_file_hash,
                   imported_at = now()""",
                (summary_id,
                 summary_record["date"],
                 summary_record["step_count"],
                 summary_record["calories_burned"],
                 summary_record["distance_meters"],
                 summary_record["floors_climbed"],
                 summary_record["active_minutes"],
                 summary_record["sedentary_minutes"],
                 summary_record["min_heart_rate"],
                 summary_record["max_heart_rate"],
                 summary_record["resting_heart_rate"],
                 summary_record["avg_heart_rate"],
                 summary_record["stress_avg"],
                 summary_record["stress_max"],
                 summary_record["stress_min"],
                 summary_record["body_battery_charged"],
                 summary_record["body_battery_drained"],
                 summary_record["body_battery_start"],
                 summary_record["body_battery_end"],
                 summary_record["intensity_minutes_moderate"],
                 summary_record["intensity_minutes_vigorous"],
                 file_hash)
            )
            total_inserted += 1

        # Update record count
        db_connection.execute(
            "UPDATE imported_files SET record_count = ? WHERE file_hash = ?",
            (total_inserted, file_hash)
        )

        db_connection.commit()
        logger.info(f"Inserted {total_inserted} daily summary records from {file_path}")

    except Exception as e:
        logger.error(f"Error inserting daily summary data from {file_path}: {e}")
        try:
            db_connection.rollback()
        except:
            pass
        return 0

    return total_inserted


def process_sleep_json_files(folder_path: str, db_connection) -> Dict[str, Any]:
    """
    Process all sleep JSON files in a directory

    Args:
        folder_path: Directory containing sleep JSON files
        db_connection: Database connection

    Returns:
        Summary of processing results
    """
    logger.info(f"Processing sleep JSON files from: {folder_path}")

    summary = {
        "files_found": 0,
        "files_processed": 0,
        "total_records": 0,
        "duplicates_skipped": 0,
        "errors": 0,
        "error_files": []
    }

    try:
        # Find sleep JSON files
        sleep_files = scan_json_files(folder_path, "sleep_*.json")
        summary["files_found"] = len(sleep_files)

        if not sleep_files:
            logger.info("No sleep JSON files found")
            return summary

        # Process each sleep file
        for file_path in sleep_files:
            try:
                logger.info(f"Processing sleep file: {file_path}")

                # Load and parse JSON
                json_data = load_json_file(file_path)
                if not json_data:
                    summary["errors"] += 1
                    summary["error_files"].append({
                        "file": file_path,
                        "error": "Failed to load JSON"
                    })
                    continue

                # Parse sleep data
                parsed_data = parse_sleep_json(json_data, file_path)

                if parsed_data.get("error"):
                    summary["errors"] += 1
                    summary["error_files"].append({
                        "file": file_path,
                        "error": parsed_data["error"]
                    })
                    continue

                # Insert into database
                records_inserted = insert_sleep_data(parsed_data, db_connection)

                if records_inserted == 0:
                    # Check if it was a duplicate
                    file_hash = parsed_data["file_hash"]
                    cursor = db_connection.execute(
                        "SELECT file_hash FROM imported_files WHERE file_hash = ?",
                        (file_hash,)
                    )
                    if cursor.fetchone():
                        summary["duplicates_skipped"] += 1
                    else:
                        logger.warning(f"No sleep records extracted from {file_path}")
                else:
                    summary["total_records"] += records_inserted
                    summary["files_processed"] += 1

            except Exception as e:
                logger.error(f"Error processing sleep file {file_path}: {e}")
                summary["errors"] += 1
                summary["error_files"].append({
                    "file": file_path,
                    "error": str(e)
                })

        logger.info(f"Sleep files processing complete: {summary}")

    except Exception as e:
        logger.error(f"Error processing sleep folder {folder_path}: {e}")
        summary["errors"] += 1

    return summary