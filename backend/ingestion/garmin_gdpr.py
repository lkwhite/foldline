"""
Garmin GDPR Export Parser

Handles extraction and parsing of Garmin "Export My Data" zip files.
Processes FIT, TCX, and JSON files to extract:
  - Sleep data
  - Resting HR
  - HRV (Heart Rate Variability)
  - Stress scores
  - Steps
  - Training load
"""

import zipfile
import os
import tempfile
import shutil
from pathlib import Path
from typing import Dict, List, Any, Optional, Callable
import logging
import json

logger = logging.getLogger(__name__)


def extract_garmin_export(zip_path: str, extract_to: Optional[str] = None) -> Dict[str, Any]:
    """
    Extract a Garmin GDPR export zip file

    Args:
        zip_path: Path to the .zip file
        extract_to: Directory to extract files to (if None, uses temp directory)

    Returns:
        Summary dict with extracted file counts and types
    """
    logger.info(f"Extracting GDPR export: {zip_path}")

    # Validate ZIP file exists
    if not os.path.exists(zip_path):
        raise FileNotFoundError(f"ZIP file not found: {zip_path}")

    if not zipfile.is_zipfile(zip_path):
        raise ValueError(f"File is not a valid ZIP archive: {zip_path}")

    # Create extraction directory
    if extract_to is None:
        extract_to = tempfile.mkdtemp(prefix="foldline_gdpr_")
        logger.info(f"Using temporary extraction directory: {extract_to}")
    else:
        os.makedirs(extract_to, exist_ok=True)

    summary = {
        "total_files": 0,
        "fit_files": [],
        "tcx_files": [],
        "json_files": [],
        "extract_path": extract_to,
        "di_connect_found": False,
        "file_categories": {
            "sleep": [],
            "daily_summaries": [],
            "activities": [],
            "hrv": [],
            "stress": [],
            "fitness_assessments": [],
            "hydration": [],
            "menstrual_cycles": [],
            "body_composition": [],
            "other": []
        }
    }

    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            # Get list of all files in ZIP
            all_files = zip_ref.namelist()
            logger.info(f"ZIP contains {len(all_files)} files")

            # Extract all files
            zip_ref.extractall(extract_to)
            logger.info(f"Extracted to: {extract_to}")

            # Find DI_CONNECT directory
            di_connect_path = None
            for root, dirs, files in os.walk(extract_to):
                if "DI_CONNECT" in dirs:
                    di_connect_path = os.path.join(root, "DI_CONNECT")
                    summary["di_connect_found"] = True
                    logger.info(f"Found DI_CONNECT directory: {di_connect_path}")
                    break

            # If DI_CONNECT not found, use extraction root
            if not di_connect_path:
                logger.warning("DI_CONNECT directory not found, scanning entire extraction")
                di_connect_path = extract_to

            # Recursively scan and categorize files
            for root, dirs, files in os.walk(di_connect_path):
                for file in files:
                    full_path = os.path.join(root, file)
                    file_lower = file.lower()
                    summary["total_files"] += 1

                    # Categorize by file extension
                    if file_lower.endswith('.fit'):
                        summary["fit_files"].append(full_path)
                        # Categorize FIT files by subdirectory
                        if "activities" in root.lower() or "fitness" in root.lower():
                            summary["file_categories"]["activities"].append(full_path)
                        else:
                            summary["file_categories"]["other"].append(full_path)

                    elif file_lower.endswith('.tcx'):
                        summary["tcx_files"].append(full_path)
                        summary["file_categories"]["activities"].append(full_path)

                    elif file_lower.endswith('.json'):
                        summary["json_files"].append(full_path)

                        # Categorize JSON files by filename pattern
                        if "sleep" in file_lower:
                            summary["file_categories"]["sleep"].append(full_path)
                        elif "udsfile" in file_lower or "dailysummary" in file_lower or "summarizedactivities" in file_lower:
                            summary["file_categories"]["daily_summaries"].append(full_path)
                        elif "hrv" in file_lower:
                            summary["file_categories"]["hrv"].append(full_path)
                        elif "stress" in file_lower:
                            summary["file_categories"]["stress"].append(full_path)
                        elif "fitnessage" in file_lower or "vo2max" in file_lower:
                            summary["file_categories"]["fitness_assessments"].append(full_path)
                        elif "hydration" in file_lower:
                            summary["file_categories"]["hydration"].append(full_path)
                        elif "menstrual" in file_lower:
                            summary["file_categories"]["menstrual_cycles"].append(full_path)
                        elif "weight" in file_lower or "bodycomposition" in file_lower:
                            summary["file_categories"]["body_composition"].append(full_path)
                        else:
                            summary["file_categories"]["other"].append(full_path)

        # Log summary of categorized files
        logger.info(f"Extraction complete: {summary['total_files']} files")
        logger.info(f"  FIT files: {len(summary['fit_files'])}")
        logger.info(f"  TCX files: {len(summary['tcx_files'])}")
        logger.info(f"  JSON files: {len(summary['json_files'])}")
        logger.info(f"File categories:")
        for category, files in summary["file_categories"].items():
            if files:
                logger.info(f"  {category}: {len(files)} files")

    except Exception as e:
        logger.error(f"Error extracting ZIP file: {e}")
        raise

    return summary


def process_gdpr_export(
    zip_path: str,
    db_connection,
    progress_callback: Optional[Callable[[str, int, int], None]] = None,
    cleanup_temp: bool = True
) -> Dict[str, Any]:
    """
    Complete pipeline to process a GDPR export

    1. Extract zip
    2. Parse all relevant files (FIT and JSON)
    3. Insert into DB with deduplication
    4. Return comprehensive summary

    Args:
        zip_path: Path to Garmin GDPR export ZIP file
        db_connection: Database connection
        progress_callback: Optional callback function(operation, current, total)
        cleanup_temp: Whether to delete temporary extraction directory

    Returns:
        Comprehensive summary of import operation
    """
    logger.info(f"Processing GDPR export: {zip_path}")

    summary = {
        "success": False,
        "zip_path": zip_path,
        "total_files_found": 0,
        "total_files_processed": 0,
        "total_records_inserted": 0,
        "duplicates_skipped": 0,
        "errors": 0,
        "error_details": [],
        "extract_path": None,
        "processing_time_seconds": 0,
        "by_category": {
            "fit_files": {"found": 0, "processed": 0, "records": 0, "errors": 0},
            "sleep_json": {"found": 0, "processed": 0, "records": 0, "errors": 0},
            "daily_summaries": {"found": 0, "processed": 0, "records": 0, "errors": 0},
            "hrv": {"found": 0, "processed": 0, "records": 0, "errors": 0},
            "stress": {"found": 0, "processed": 0, "records": 0, "errors": 0},
            "fitness_assessments": {"found": 0, "processed": 0, "records": 0, "errors": 0},
            "hydration": {"found": 0, "processed": 0, "records": 0, "errors": 0},
            "menstrual_cycles": {"found": 0, "processed": 0, "records": 0, "errors": 0},
            "body_composition": {"found": 0, "processed": 0, "records": 0, "errors": 0}
        }
    }

    import time
    start_time = time.time()
    extract_path = None

    try:
        # Step 1: Extract ZIP file
        logger.info("Step 1: Extracting GDPR export ZIP file")
        if progress_callback:
            progress_callback("Extracting ZIP file", 0, 100)

        extraction_summary = extract_garmin_export(zip_path)
        extract_path = extraction_summary["extract_path"]
        summary["extract_path"] = extract_path
        summary["total_files_found"] = extraction_summary["total_files"]

        logger.info(f"Extracted {summary['total_files_found']} files to {extract_path}")

        # Step 2: Process FIT files
        fit_files = extraction_summary["fit_files"]
        summary["by_category"]["fit_files"]["found"] = len(fit_files)

        if fit_files:
            logger.info(f"Step 2: Processing {len(fit_files)} FIT files")
            from ingestion.fit_folder import parse_fit_file, insert_fit_data

            for idx, fit_file in enumerate(fit_files):
                try:
                    if progress_callback:
                        progress_callback(f"Processing FIT files", idx + 1, len(fit_files))

                    # Parse FIT file
                    parsed_data = parse_fit_file(fit_file)

                    if "error" in parsed_data:
                        logger.warning(f"Error parsing {fit_file}: {parsed_data['error']}")
                        summary["by_category"]["fit_files"]["errors"] += 1
                        summary["error_details"].append({
                            "file": fit_file,
                            "type": "fit",
                            "error": parsed_data["error"]
                        })
                        continue

                    # Insert into database
                    records_inserted = insert_fit_data(parsed_data, db_connection, source="gdpr")

                    if records_inserted > 0:
                        summary["by_category"]["fit_files"]["processed"] += 1
                        summary["by_category"]["fit_files"]["records"] += records_inserted
                        summary["total_records_inserted"] += records_inserted
                        summary["total_files_processed"] += 1
                    else:
                        # Check if it was a duplicate
                        file_hash = parsed_data.get("file_hash")
                        if file_hash:
                            cursor = db_connection.execute(
                                "SELECT file_hash FROM imported_files WHERE file_hash = ?",
                                (file_hash,)
                            )
                            if cursor.fetchone():
                                summary["duplicates_skipped"] += 1
                                logger.debug(f"Skipped duplicate FIT file: {fit_file}")

                except Exception as e:
                    logger.error(f"Error processing FIT file {fit_file}: {e}")
                    summary["by_category"]["fit_files"]["errors"] += 1
                    summary["errors"] += 1
                    summary["error_details"].append({
                        "file": fit_file,
                        "type": "fit",
                        "error": str(e)
                    })

        # Step 3: Process JSON files by category
        from ingestion.json_parser import (
            load_json_file, parse_sleep_json, parse_daily_summary_json,
            insert_sleep_data, insert_daily_summary_data
        )

        # Process sleep JSON files
        sleep_files = extraction_summary["file_categories"]["sleep"]
        summary["by_category"]["sleep_json"]["found"] = len(sleep_files)

        if sleep_files:
            logger.info(f"Step 3a: Processing {len(sleep_files)} sleep JSON files")

            for idx, sleep_file in enumerate(sleep_files):
                try:
                    if progress_callback:
                        progress_callback(f"Processing sleep JSON", idx + 1, len(sleep_files))

                    json_data = load_json_file(sleep_file)
                    if not json_data:
                        summary["by_category"]["sleep_json"]["errors"] += 1
                        continue

                    parsed_data = parse_sleep_json(json_data, sleep_file)

                    if parsed_data.get("error"):
                        logger.warning(f"Error parsing sleep {sleep_file}: {parsed_data['error']}")
                        summary["by_category"]["sleep_json"]["errors"] += 1
                        summary["error_details"].append({
                            "file": sleep_file,
                            "type": "sleep_json",
                            "error": parsed_data["error"]
                        })
                        continue

                    records_inserted = insert_sleep_data(parsed_data, db_connection, source="gdpr")

                    if records_inserted > 0:
                        summary["by_category"]["sleep_json"]["processed"] += 1
                        summary["by_category"]["sleep_json"]["records"] += records_inserted
                        summary["total_records_inserted"] += records_inserted
                        summary["total_files_processed"] += 1
                    else:
                        summary["duplicates_skipped"] += 1

                except Exception as e:
                    logger.error(f"Error processing sleep JSON {sleep_file}: {e}")
                    summary["by_category"]["sleep_json"]["errors"] += 1
                    summary["errors"] += 1
                    summary["error_details"].append({
                        "file": sleep_file,
                        "type": "sleep_json",
                        "error": str(e)
                    })

        # Process daily summary JSON files
        daily_summary_files = extraction_summary["file_categories"]["daily_summaries"]
        summary["by_category"]["daily_summaries"]["found"] = len(daily_summary_files)

        if daily_summary_files:
            logger.info(f"Step 3b: Processing {len(daily_summary_files)} daily summary JSON files")

            for idx, summary_file in enumerate(daily_summary_files):
                try:
                    if progress_callback:
                        progress_callback(f"Processing daily summaries", idx + 1, len(daily_summary_files))

                    json_data = load_json_file(summary_file)
                    if not json_data:
                        summary["by_category"]["daily_summaries"]["errors"] += 1
                        continue

                    parsed_data = parse_daily_summary_json(json_data, summary_file)

                    if parsed_data.get("error"):
                        logger.warning(f"Error parsing daily summary {summary_file}: {parsed_data['error']}")
                        summary["by_category"]["daily_summaries"]["errors"] += 1
                        summary["error_details"].append({
                            "file": summary_file,
                            "type": "daily_summary",
                            "error": parsed_data["error"]
                        })
                        continue

                    records_inserted = insert_daily_summary_data(parsed_data, db_connection, source="gdpr")

                    if records_inserted > 0:
                        summary["by_category"]["daily_summaries"]["processed"] += 1
                        summary["by_category"]["daily_summaries"]["records"] += records_inserted
                        summary["total_records_inserted"] += records_inserted
                        summary["total_files_processed"] += 1
                    else:
                        summary["duplicates_skipped"] += 1

                except Exception as e:
                    logger.error(f"Error processing daily summary {summary_file}: {e}")
                    summary["by_category"]["daily_summaries"]["errors"] += 1
                    summary["errors"] += 1
                    summary["error_details"].append({
                        "file": summary_file,
                        "type": "daily_summary",
                        "error": str(e)
                    })

        # Calculate success rate
        success_rate = 0
        if summary["total_files_found"] > 0:
            success_rate = (summary["total_files_processed"] / summary["total_files_found"]) * 100

        # Mark as successful if we met the 95% threshold
        summary["success"] = success_rate >= 95.0 and summary["total_files_processed"] > 0
        summary["success_rate"] = round(success_rate, 2)

        # Record processing time
        summary["processing_time_seconds"] = round(time.time() - start_time, 2)

        logger.info(f"GDPR export processing complete:")
        logger.info(f"  Files found: {summary['total_files_found']}")
        logger.info(f"  Files processed: {summary['total_files_processed']}")
        logger.info(f"  Records inserted: {summary['total_records_inserted']}")
        logger.info(f"  Duplicates skipped: {summary['duplicates_skipped']}")
        logger.info(f"  Errors: {summary['errors']}")
        logger.info(f"  Success rate: {summary['success_rate']}%")
        logger.info(f"  Processing time: {summary['processing_time_seconds']}s")

    except Exception as e:
        logger.error(f"Critical error processing GDPR export: {e}")
        summary["success"] = False
        summary["errors"] += 1
        summary["error_details"].append({
            "file": zip_path,
            "type": "critical",
            "error": str(e)
        })
        raise

    finally:
        # Cleanup temporary extraction directory if requested
        if cleanup_temp and extract_path and os.path.exists(extract_path):
            try:
                shutil.rmtree(extract_path)
                logger.info(f"Cleaned up temporary extraction directory: {extract_path}")
            except Exception as e:
                logger.warning(f"Failed to cleanup temp directory {extract_path}: {e}")

    return summary
