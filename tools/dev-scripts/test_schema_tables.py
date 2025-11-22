#!/usr/bin/env python3
"""
Test script to verify the new JSON database tables are working
"""

import sys
import os
import logging
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_path))

from db.connection import get_db

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def test_new_tables():
    """Test that all new JSON tables can be queried"""

    try:
        # Get database connection
        db = get_db()
        logger.info("Database connection established")

        # List of new tables to test
        new_tables = [
            'sleep_detailed',
            'daily_summaries',
            'fitness_assessments',
            'hydration_logs',
            'menstrual_cycles',
            'body_composition'
        ]

        logger.info("Testing new JSON data tables...")

        for table in new_tables:
            try:
                # Test that table exists and can be queried
                cursor = db.connection.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                logger.info(f"✅ Table '{table}' exists and is queryable (currently has {count} rows)")

                # Test that we can describe the table structure
                cursor = db.connection.execute(f"PRAGMA table_info({table})")
                columns = cursor.fetchall()
                logger.info(f"   → {len(columns)} columns defined")

            except Exception as e:
                logger.error(f"❌ Table '{table}' failed: {e}")
                return False

        # Test the views as well
        try:
            cursor = db.connection.execute("SELECT COUNT(*) FROM daily_metrics")
            count = cursor.fetchone()[0]
            logger.info(f"✅ View 'daily_metrics' exists and is queryable ({count} rows)")
        except Exception as e:
            logger.error(f"❌ View 'daily_metrics' failed: {e}")
            return False

        # Test sample insert on one of the new tables
        try:
            logger.info("Testing sample data insertion...")

            # Insert a test sleep_detailed record
            cursor = db.connection.execute("""
                INSERT INTO sleep_detailed
                (id, date, sleep_start_gmt, sleep_end_gmt, deep_sleep_seconds, light_sleep_seconds,
                 sleep_window_confirmation_type, source_file_hash)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                999999,  # Test ID
                '2024-01-01',
                '2024-01-01 02:00:00',
                '2024-01-01 08:00:00',
                7200,  # 2 hours deep sleep
                14400, # 4 hours light sleep
                'ENHANCED_CONFIRMED_FINAL',
                'test_hash_123'
            ))

            db.connection.commit()
            logger.info("✅ Sample data insertion successful")

            # Verify the insert
            cursor = db.connection.execute("SELECT COUNT(*) FROM sleep_detailed WHERE id = 999999")
            count = cursor.fetchone()[0]

            if count == 1:
                logger.info("✅ Sample data retrieval successful")

                # Clean up test data
                db.connection.execute("DELETE FROM sleep_detailed WHERE id = 999999")
                db.connection.commit()
                logger.info("✅ Test cleanup completed")
            else:
                logger.error(f"❌ Expected 1 test record, found {count}")
                return False

        except Exception as e:
            logger.error(f"❌ Sample data test failed: {e}")
            return False

        logger.info("🎉 All new JSON data tables are working correctly!")
        return True

    except Exception as e:
        logger.error(f"Database test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_new_tables()
    sys.exit(0 if success else 1)