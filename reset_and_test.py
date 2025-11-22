#!/usr/bin/env python3
"""
Reset test data and test JSON processing with clean database
"""

import sys
import os
import logging
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_path))

from db.connection import get_db
from ingestion.json_parser import process_sleep_json_files

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def reset_and_test():
    """Clear test data and test fresh JSON processing"""

    try:
        # Get database connection
        db = get_db()
        logger.info("Database connection established")

        # Clear test data
        logger.info("Clearing test data...")
        db.connection.execute("DELETE FROM imported_files WHERE file_path LIKE '/tmp/sample_garmin_json/%'")
        db.connection.execute("DELETE FROM sleep_detailed")
        db.connection.commit()
        logger.info("Test data cleared")

        # Check counts
        cursor = db.connection.execute("SELECT COUNT(*) FROM imported_files")
        files_count = cursor.fetchone()[0]
        cursor = db.connection.execute("SELECT COUNT(*) FROM sleep_detailed")
        sleep_count = cursor.fetchone()[0]
        logger.info(f"Database state - Files: {files_count}, Sleep: {sleep_count}")

        # Process sleep JSON files
        logger.info("Processing sleep JSON files...")
        summary = process_sleep_json_files("/tmp/sample_garmin_json", db.connection)

        logger.info("Processing results:")
        logger.info(f"  Files found: {summary['files_found']}")
        logger.info(f"  Files processed: {summary['files_processed']}")
        logger.info(f"  Total records: {summary['total_records']}")
        logger.info(f"  Duplicates skipped: {summary['duplicates_skipped']}")
        logger.info(f"  Errors: {summary['errors']}")

        if summary['error_files']:
            logger.info("Errors:")
            for error in summary['error_files']:
                logger.info(f"  {error['file']}: {error['error']}")

        # Check final database state
        cursor = db.connection.execute("SELECT COUNT(*) FROM sleep_detailed")
        final_sleep_count = cursor.fetchone()[0]
        logger.info(f"Final sleep records: {final_sleep_count}")

        if final_sleep_count > 0:
            # Show sample data
            cursor = db.connection.execute("""
                SELECT date, sleep_start_gmt,
                       deep_sleep_seconds, light_sleep_seconds, rem_sleep_seconds,
                       sleep_window_confirmation_type, average_respiration, average_spo2
                FROM sleep_detailed
                ORDER BY date
            """)
            logger.info("Imported sleep data:")
            for i, row in enumerate(cursor.fetchall()):
                logger.info(f"  {i+1}. {row[0]}: {row[1]}")
                logger.info(f"      Deep: {row[2]/3600:.1f}h, Light: {row[3]/3600:.1f}h, REM: {row[4]/3600:.1f}h")
                logger.info(f"      Type: {row[5]}, Respiration: {row[6]}, SpO2: {row[7]}")

        return summary['errors'] == 0

    except Exception as e:
        logger.error(f"Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = reset_and_test()
    if success:
        logger.info("🎉 JSON processing pipeline is working correctly!")
    else:
        logger.error("❌ JSON processing pipeline failed")
    sys.exit(0 if success else 1)