#!/usr/bin/env python3
"""
Quick test of the fixed JSON processing with database insertion
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
    load_json_file,
    parse_sleep_json,
    insert_sleep_data
)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def quick_test():
    """Quick test of JSON processing with database insertion"""

    try:
        # Get database connection
        db = get_db()
        logger.info("Database connection established")

        # Check current count
        cursor = db.connection.execute("SELECT COUNT(*) FROM sleep_detailed")
        before_count = cursor.fetchone()[0]
        logger.info(f"Sleep records before: {before_count}")

        # Test with one sleep file
        test_file = "/tmp/sample_garmin_json/sleep_2024-01-15.json"
        logger.info(f"Testing with: {test_file}")

        # Load and parse
        json_data = load_json_file(test_file)
        parsed_data = parse_sleep_json(json_data, test_file)

        logger.info(f"Sleep records parsed: {len(parsed_data.get('sleep_records', []))}")

        if parsed_data.get("error"):
            logger.error(f"Parsing error: {parsed_data['error']}")
            return False

        # Insert data
        records_inserted = insert_sleep_data(parsed_data, db.connection)
        logger.info(f"Records inserted: {records_inserted}")

        # Check final count
        cursor = db.connection.execute("SELECT COUNT(*) FROM sleep_detailed")
        after_count = cursor.fetchone()[0]
        logger.info(f"Sleep records after: {after_count}")

        # Show inserted data
        if after_count > before_count:
            cursor = db.connection.execute("""
                SELECT date, sleep_start_gmt, deep_sleep_seconds, light_sleep_seconds,
                       rem_sleep_seconds, sleep_window_confirmation_type, average_respiration
                FROM sleep_detailed
                ORDER BY date DESC LIMIT 1
            """)
            row = cursor.fetchone()
            if row:
                logger.info(f"Inserted record:")
                logger.info(f"  Date: {row[0]}")
                logger.info(f"  Start: {row[1]}")
                logger.info(f"  Deep: {row[2]}s ({row[2]/3600:.1f}h)")
                logger.info(f"  Light: {row[3]}s ({row[3]/3600:.1f}h)")
                logger.info(f"  REM: {row[4]}s ({row[4]/3600:.1f}h)")
                logger.info(f"  Confirmation: {row[5]}")
                logger.info(f"  Avg respiration: {row[6]}")

        return True

    except Exception as e:
        logger.error(f"Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = quick_test()
    sys.exit(0 if success else 1)