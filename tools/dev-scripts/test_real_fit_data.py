#!/usr/bin/env python3
"""
Test script for real FIT file parsing and database insertion
"""

import sys
import os
import logging
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_path))

from db.connection import get_db
from ingestion.fit_folder import parse_fit_file, insert_fit_data, process_fit_folder

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def test_with_real_fit_files():
    """Test with the extracted real FIT files"""

    # Test files
    fit_files = [
        "/tmp/laura.white@gmail.com_108471997439.fit",    # Activity file
        "/tmp/laura.white@gmail.com_53902275619.fit",     # Monitoring file
        "/tmp/laura.white@gmail.com_76966352163.fit"      # Monitoring file
    ]

    try:
        # Get database connection
        db = get_db()
        logger.info("Database connection established")

        total_records = 0

        for fit_file in fit_files:
            if not os.path.exists(fit_file):
                logger.warning(f"Skipping missing file: {fit_file}")
                continue

            logger.info(f"\n=== Processing {fit_file} ===")

            # Parse the file
            parsed_data = parse_fit_file(fit_file)

            if "error" in parsed_data:
                logger.error(f"Parsing error: {parsed_data['error']}")
                continue

            # Show what we found
            logger.info(f"Sleep records: {len(parsed_data.get('sleep_records', []))}")
            logger.info(f"HRV records: {len(parsed_data.get('hrv_records', []))}")
            logger.info(f"Stress records: {len(parsed_data.get('stress_records', []))}")
            logger.info(f"Daily steps: {len(parsed_data.get('daily_steps', []))}")
            logger.info(f"Activities: {len(parsed_data.get('activities', []))}")
            logger.info(f"Sessions: {len(parsed_data.get('sessions', []))}")
            logger.info(f"Records: {len(parsed_data.get('records', []))}")

            # Insert into database
            records_inserted = insert_fit_data(parsed_data, db.connection)
            total_records += records_inserted
            logger.info(f"Inserted {records_inserted} records")

        # Check what's in the database
        logger.info(f"\n=== Database Summary ===")

        cursor = db.connection.execute("SELECT COUNT(*) FROM imported_files")
        file_count = cursor.fetchone()[0]
        logger.info(f"Files imported: {file_count}")

        cursor = db.connection.execute("SELECT COUNT(*) FROM stress_records")
        stress_count = cursor.fetchone()[0]
        logger.info(f"Stress records: {stress_count}")

        cursor = db.connection.execute("SELECT COUNT(*) FROM daily_steps")
        steps_count = cursor.fetchone()[0]
        logger.info(f"Daily steps records: {steps_count}")

        cursor = db.connection.execute("SELECT COUNT(*) FROM activities")
        activity_count = cursor.fetchone()[0]
        logger.info(f"Activity records: {activity_count}")

        # Show some sample data
        if stress_count > 0:
            cursor = db.connection.execute("SELECT timestamp, stress_level FROM stress_records LIMIT 5")
            logger.info("Sample stress data:")
            for row in cursor.fetchall():
                logger.info(f"  {row[0]}: stress level {row[1]}")

        if steps_count > 0:
            cursor = db.connection.execute("SELECT date, step_count FROM daily_steps LIMIT 5")
            logger.info("Sample daily steps:")
            for row in cursor.fetchall():
                logger.info(f"  {row[0]}: {row[1]} steps")

        logger.info(f"\nTest completed! Total records inserted: {total_records}")
        return True

    except Exception as e:
        logger.error(f"Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_with_real_fit_files()
    sys.exit(0 if success else 1)