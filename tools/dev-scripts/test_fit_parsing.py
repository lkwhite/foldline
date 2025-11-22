#!/usr/bin/env python3
"""
Test script for FIT file parsing with real user data
"""

import sys
import os
import logging
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_path))

from db.connection import get_db
from ingestion.fit_folder import parse_fit_file, scan_fit_directory, process_fit_folder

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def test_single_fit_file():
    """Test parsing a single FIT file"""
    fit_file_path = "/tmp/laura.white@gmail.com_PrimaryTrainingBackup.fit"

    if not os.path.exists(fit_file_path):
        logger.error(f"FIT file not found: {fit_file_path}")
        return False

    logger.info(f"Testing FIT file parsing: {fit_file_path}")

    try:
        # Parse the FIT file
        parsed_data = parse_fit_file(fit_file_path)

        if "error" in parsed_data:
            logger.error(f"Parsing error: {parsed_data['error']}")
            return False

        # Display summary
        logger.info("=== FIT File Parsing Results ===")
        logger.info(f"File path: {parsed_data['file_path']}")
        logger.info(f"File hash: {parsed_data['file_hash']}")
        logger.info(f"Sleep records: {len(parsed_data.get('sleep_records', []))}")
        logger.info(f"HRV records: {len(parsed_data.get('hrv_records', []))}")
        logger.info(f"Stress records: {len(parsed_data.get('stress_records', []))}")
        logger.info(f"Daily steps: {len(parsed_data.get('daily_steps', []))}")
        logger.info(f"Activities: {len(parsed_data.get('activities', []))}")
        logger.info(f"Sessions: {len(parsed_data.get('sessions', []))}")
        logger.info(f"Records: {len(parsed_data.get('records', []))}")

        # Show file info
        if parsed_data.get('file_info'):
            logger.info(f"File info: {parsed_data['file_info']}")

        # Show sample session data if available
        if parsed_data.get('sessions'):
            logger.info(f"First session sample: {parsed_data['sessions'][0]}")

        return True

    except Exception as e:
        logger.error(f"Error testing FIT file: {e}")
        return False

def test_database_insertion():
    """Test database schema initialization and data insertion"""
    logger.info("Testing database operations...")

    try:
        # Initialize database
        db = get_db()
        logger.info("Database connection established")

        # Parse the FIT file
        fit_file_path = "/tmp/laura.white@gmail.com_PrimaryTrainingBackup.fit"
        parsed_data = parse_fit_file(fit_file_path)

        if "error" in parsed_data:
            logger.error(f"Cannot test insertion - parsing error: {parsed_data['error']}")
            return False

        # Test data insertion
        from ingestion.fit_folder import insert_fit_data

        records_inserted = insert_fit_data(parsed_data, db.connection)
        logger.info(f"Successfully inserted {records_inserted} records into database")

        # Verify data in database
        cursor = db.connection.execute("SELECT COUNT(*) FROM imported_files")
        file_count = cursor.fetchone()[0]
        logger.info(f"Files in database: {file_count}")

        cursor = db.connection.execute("SELECT COUNT(*) FROM sleep_records")
        sleep_count = cursor.fetchone()[0]
        logger.info(f"Sleep records in database: {sleep_count}")

        cursor = db.connection.execute("SELECT COUNT(*) FROM activities")
        activity_count = cursor.fetchone()[0]
        logger.info(f"Activities in database: {activity_count}")

        return True

    except Exception as e:
        logger.error(f"Error testing database operations: {e}")
        return False

def test_folder_processing():
    """Test the complete folder processing pipeline"""
    logger.info("Testing folder processing pipeline...")

    # Create test directory with our FIT file
    test_dir = "/tmp/test_fit_folder"
    os.makedirs(test_dir, exist_ok=True)

    # Copy FIT file to test directory
    import shutil
    source_file = "/tmp/laura.white@gmail.com_PrimaryTrainingBackup.fit"
    dest_file = f"{test_dir}/test_backup.fit"

    if os.path.exists(source_file):
        shutil.copy2(source_file, dest_file)
    else:
        logger.error("Source FIT file not available for folder test")
        return False

    try:
        # Get database connection
        db = get_db()

        # Process the folder
        summary = process_fit_folder(test_dir, db.connection)

        logger.info("=== Folder Processing Results ===")
        logger.info(f"Files found: {summary['files_found']}")
        logger.info(f"Files processed: {summary['files_processed']}")
        logger.info(f"Total records: {summary['total_records']}")
        logger.info(f"Duplicates skipped: {summary['duplicates_skipped']}")
        logger.info(f"Errors: {summary['errors']}")

        if summary['error_files']:
            logger.error(f"Error files: {summary['error_files']}")

        # Clean up test directory
        shutil.rmtree(test_dir)

        return summary['errors'] == 0

    except Exception as e:
        logger.error(f"Error testing folder processing: {e}")
        return False

if __name__ == "__main__":
    logger.info("Starting FIT file parsing tests with real user data...")

    # Test 1: Parse single FIT file
    logger.info("\n=== Test 1: Single FIT File Parsing ===")
    success1 = test_single_fit_file()

    # Test 2: Database operations
    logger.info("\n=== Test 2: Database Insertion ===")
    success2 = test_database_insertion()

    # Test 3: Complete folder processing
    logger.info("\n=== Test 3: Folder Processing Pipeline ===")
    success3 = test_folder_processing()

    # Summary
    logger.info("\n=== Test Summary ===")
    logger.info(f"Single file parsing: {'PASS' if success1 else 'FAIL'}")
    logger.info(f"Database insertion: {'PASS' if success2 else 'FAIL'}")
    logger.info(f"Folder processing: {'PASS' if success3 else 'FAIL'}")

    if success1 and success2 and success3:
        logger.info("All tests PASSED! FIT file processing implementation is working.")
        sys.exit(0)
    else:
        logger.error("Some tests FAILED. Check the logs above for details.")
        sys.exit(1)