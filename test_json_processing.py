#!/usr/bin/env python3
"""
Test script for JSON processing pipeline with real Garmin GDPR export data
"""

import sys
import os
import logging
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_path))

from db.connection import get_db
from ingestion.json_parser import (
    scan_json_files,
    load_json_file,
    parse_sleep_json,
    parse_daily_summary_json,
    insert_sleep_data,
    process_sleep_json_files
)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def explore_gdpr_structure():
    """Explore the GDPR export structure to understand JSON file organization"""

    # Common locations for GDPR exports
    possible_paths = [
        "/tmp/sample_garmin_json",  # Our test data
        "/tmp/DI_CONNECT",  # If extracted to /tmp
        "/tmp/garmin_export",
        "/tmp/export",
        "/Users/laurawhite/Downloads/DI_CONNECT",
        "/Users/laurawhite/Desktop/DI_CONNECT"
    ]

    logger.info("Exploring GDPR export structure...")

    for base_path in possible_paths:
        if os.path.exists(base_path):
            logger.info(f"Found GDPR export at: {base_path}")

            # Look for sleep files
            sleep_files = scan_json_files(base_path, "sleep_*.json")
            if sleep_files:
                logger.info(f"Found {len(sleep_files)} sleep JSON files")
                for i, file_path in enumerate(sleep_files[:5]):  # Show first 5
                    logger.info(f"  {i+1}. {file_path}")
                if len(sleep_files) > 5:
                    logger.info(f"  ... and {len(sleep_files) - 5} more")

            # Look for UDS files
            uds_files = scan_json_files(base_path, "*UdsFile*.json")
            if uds_files:
                logger.info(f"Found {len(uds_files)} UDS daily summary files")
                for i, file_path in enumerate(uds_files[:3]):  # Show first 3
                    logger.info(f"  {i+1}. {file_path}")
                if len(uds_files) > 3:
                    logger.info(f"  ... and {len(uds_files) - 3} more")

            # Look for other JSON files
            all_json = scan_json_files(base_path)
            logger.info(f"Total JSON files found: {len(all_json)}")

            return base_path

    logger.warning("No GDPR export directory found in common locations")
    logger.info("Please extract your GDPR export to /tmp/DI_CONNECT or update the script")
    return None

def test_sleep_json_parsing(gdpr_path: str):
    """Test sleep JSON parsing with real data"""

    logger.info("=== Testing Sleep JSON Parsing ===")

    # Find sleep files
    sleep_files = scan_json_files(gdpr_path, "sleep_*.json")

    if not sleep_files:
        logger.warning("No sleep JSON files found")
        return False

    logger.info(f"Testing with {min(3, len(sleep_files))} sleep files...")

    # Test parsing individual files
    for i, file_path in enumerate(sleep_files[:3]):
        try:
            logger.info(f"\n--- Testing file {i+1}: {os.path.basename(file_path)} ---")

            # Load JSON
            json_data = load_json_file(file_path)
            if not json_data:
                logger.error(f"Failed to load {file_path}")
                continue

            logger.info(f"JSON loaded successfully, {len(json_data)} top-level keys")
            logger.info(f"Keys: {list(json_data.keys())[:10]}")  # Show first 10 keys

            # Parse sleep data
            parsed_data = parse_sleep_json(json_data, file_path)

            if parsed_data.get("error"):
                logger.error(f"Parsing failed: {parsed_data['error']}")
                continue

            sleep_records = parsed_data.get("sleep_records", [])
            logger.info(f"Parsed {len(sleep_records)} sleep records")

            if sleep_records:
                record = sleep_records[0]
                logger.info(f"Sample record:")
                logger.info(f"  Date: {record.get('date')}")
                logger.info(f"  Start: {record.get('sleep_start_gmt')}")
                logger.info(f"  End: {record.get('sleep_end_gmt')}")
                logger.info(f"  Deep sleep: {record.get('deep_sleep_seconds')}s")
                logger.info(f"  Light sleep: {record.get('light_sleep_seconds')}s")
                logger.info(f"  REM sleep: {record.get('rem_sleep_seconds')}s")
                logger.info(f"  Confirmation: {record.get('sleep_window_confirmation_type')}")

        except Exception as e:
            logger.error(f"Error testing {file_path}: {e}")

    return True

def test_database_insertion():
    """Test inserting parsed data into database"""

    logger.info("=== Testing Database Insertion ===")

    try:
        # Get database connection
        db = get_db()
        logger.info("Database connection established")

        # Check current sleep_detailed count
        cursor = db.connection.execute("SELECT COUNT(*) FROM sleep_detailed")
        before_count = cursor.fetchone()[0]
        logger.info(f"Sleep records before import: {before_count}")

        # Find a test sleep file
        gdpr_path = explore_gdpr_structure()
        if not gdpr_path:
            return False

        sleep_files = scan_json_files(gdpr_path, "sleep_*.json")
        if not sleep_files:
            logger.error("No sleep files found for testing")
            return False

        # Test with one file
        test_file = sleep_files[0]
        logger.info(f"Testing insertion with: {os.path.basename(test_file)}")

        json_data = load_json_file(test_file)
        parsed_data = parse_sleep_json(json_data, test_file)

        if parsed_data.get("error"):
            logger.error(f"Cannot test insertion due to parsing error: {parsed_data['error']}")
            return False

        # Insert data
        records_inserted = insert_sleep_data(parsed_data, db.connection)
        logger.info(f"Inserted {records_inserted} records")

        # Check final count
        cursor = db.connection.execute("SELECT COUNT(*) FROM sleep_detailed")
        after_count = cursor.fetchone()[0]
        logger.info(f"Sleep records after import: {after_count}")

        # Show sample data
        if after_count > before_count:
            cursor = db.connection.execute("""
                SELECT date, sleep_start_gmt, deep_sleep_seconds, light_sleep_seconds,
                       sleep_window_confirmation_type
                FROM sleep_detailed
                ORDER BY date DESC LIMIT 3
            """)
            logger.info("Sample inserted data:")
            for row in cursor.fetchall():
                logger.info(f"  {row[0]}: {row[1]} | Deep: {row[2]}s | Light: {row[3]}s | Type: {row[4]}")

        return True

    except Exception as e:
        logger.error(f"Database insertion test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_bulk_processing():
    """Test bulk processing of all sleep files"""

    logger.info("=== Testing Bulk Sleep Processing ===")

    try:
        gdpr_path = explore_gdpr_structure()
        if not gdpr_path:
            return False

        db = get_db()

        # Process all sleep files
        summary = process_sleep_json_files(gdpr_path, db.connection)

        logger.info("Bulk processing results:")
        logger.info(f"  Files found: {summary['files_found']}")
        logger.info(f"  Files processed: {summary['files_processed']}")
        logger.info(f"  Total records: {summary['total_records']}")
        logger.info(f"  Duplicates skipped: {summary['duplicates_skipped']}")
        logger.info(f"  Errors: {summary['errors']}")

        if summary['error_files']:
            logger.info("Error files:")
            for error in summary['error_files']:
                logger.info(f"  {error['file']}: {error['error']}")

        # Final database check
        cursor = db.connection.execute("SELECT COUNT(*) FROM sleep_detailed")
        total_sleep_records = cursor.fetchone()[0]
        logger.info(f"Total sleep records in database: {total_sleep_records}")

        return summary['errors'] == 0

    except Exception as e:
        logger.error(f"Bulk processing test failed: {e}")
        return False

if __name__ == "__main__":
    logger.info("🚀 Starting JSON processing tests...")

    success = True

    # 1. Explore GDPR structure
    gdpr_path = explore_gdpr_structure()
    if gdpr_path:
        # 2. Test individual sleep file parsing
        if test_sleep_json_parsing(gdpr_path):
            # 3. Test database insertion
            if test_database_insertion():
                # 4. Test bulk processing
                success = test_bulk_processing()
            else:
                success = False
        else:
            success = False
    else:
        success = False

    if success:
        logger.info("🎉 All JSON processing tests completed successfully!")
    else:
        logger.error("❌ Some tests failed")

    sys.exit(0 if success else 1)