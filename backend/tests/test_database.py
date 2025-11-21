"""
Tests for database connection and operations.

Tests:
- Database initialization
- Schema loading
- Connection management
- Basic CRUD operations
- Deduplication logic
"""
import tempfile
from pathlib import Path

import pytest

from db.connection import Database, get_db


class TestDatabaseInitialization:
    """Tests for Database class initialization"""

    def test_init_with_custom_path(self):
        """Should initialize with custom database path"""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / "custom.db"
            db = Database(str(db_path))

            assert db.db_path == str(db_path)

    def test_init_with_default_path(self):
        """Should use default path if none provided"""
        db = Database()

        assert db.db_path is not None
        assert ".foldline" in db.db_path
        assert db.db_path.endswith(".db")

    def test_init_creates_directory(self):
        """Should create parent directories if they don't exist"""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / "nested" / "path" / "test.db"
            db = Database(str(db_path))

            # Directory should exist after init
            assert db_path.parent.exists()


class TestDatabaseConnection:
    """Tests for database connection management"""

    def test_connect_returns_connection(self, temp_db):
        """Should return connection object"""
        conn = temp_db.connect()

        assert conn is not None

    def test_connect_multiple_times(self, temp_db):
        """Should handle multiple connect calls"""
        conn1 = temp_db.connect()
        conn2 = temp_db.connect()

        # Should return connection objects
        assert conn1 is not None
        assert conn2 is not None

    def test_close_connection(self, temp_db):
        """Should close connection cleanly"""
        temp_db.connect()
        temp_db.close()

        # Should not raise error
        assert True

    def test_connection_after_close(self, temp_db):
        """Should be able to reconnect after close"""
        temp_db.connect()
        temp_db.close()

        conn = temp_db.connect()
        assert conn is not None


class TestSchemaInitialization:
    """Tests for schema initialization"""

    def test_initialize_schema(self, temp_db):
        """Should initialize schema from schema.sql"""
        temp_db.connect()
        temp_db.initialize_schema()

        # Should not raise error
        # When implemented, should create tables

    def test_schema_creates_tables(self, temp_db):
        """Should create expected tables"""
        temp_db.connect()
        temp_db.initialize_schema()

        # When schema execution is implemented, verify tables exist:
        # Expected tables: config, imported_files, sleep_records, resting_hr,
        # hrv_records, stress_records, daily_stress, daily_steps, activities

        # For DuckDB:
        # result = temp_db.connection.execute(
        #     "SELECT table_name FROM information_schema.tables WHERE table_schema='main'"
        # ).fetchall()
        # table_names = [r[0] for r in result]

        # For SQLite:
        # result = temp_db.connection.execute(
        #     "SELECT name FROM sqlite_master WHERE type='table'"
        # ).fetchall()
        # table_names = [r[0] for r in result]

        # assert 'sleep_records' in table_names
        # assert 'hrv_records' in table_names
        # assert 'imported_files' in table_names

    def test_schema_idempotent(self, temp_db):
        """Should be safe to run schema initialization multiple times"""
        temp_db.connect()
        temp_db.initialize_schema()
        temp_db.initialize_schema()  # Should not error

        # Should not raise error


class TestDatabaseOperations:
    """Tests for basic database CRUD operations"""

    def test_insert_sleep_record(self, temp_db, sample_sleep_data):
        """Should insert sleep record successfully"""
        temp_db.connect()
        temp_db.initialize_schema()

        # When schema is implemented, test insert:
        # temp_db.connection.execute(
        #     """
        #     INSERT INTO sleep_records
        #     (date, duration_minutes, deep_minutes, light_minutes, rem_minutes, sleep_score)
        #     VALUES (?, ?, ?, ?, ?, ?)
        #     """,
        #     (
        #         sample_sleep_data['date'],
        #         sample_sleep_data['duration_minutes'],
        #         sample_sleep_data['deep_minutes'],
        #         sample_sleep_data['light_minutes'],
        #         sample_sleep_data['rem_minutes'],
        #         sample_sleep_data['sleep_score']
        #     )
        # )

        # result = temp_db.connection.execute(
        #     "SELECT * FROM sleep_records WHERE date = ?",
        #     (sample_sleep_data['date'],)
        # ).fetchone()

        # assert result is not None

    def test_query_sleep_record(self, temp_db, sample_sleep_data):
        """Should query inserted sleep record"""
        temp_db.connect()
        temp_db.initialize_schema()

        # When implemented:
        # Insert record
        # Query by date
        # Verify data matches

    def test_deduplication_check(self, temp_db):
        """Should track imported files and prevent duplicates"""
        temp_db.connect()
        temp_db.initialize_schema()

        # When implemented:
        # Insert file hash into imported_files
        # Check if hash exists
        # Verify deduplication logic

        test_hash = "abc123def456"
        test_path = "/path/to/test.fit"

        # temp_db.connection.execute(
        #     "INSERT INTO imported_files (file_hash, file_path, file_type) VALUES (?, ?, ?)",
        #     (test_hash, test_path, "fit")
        # )

        # Check if hash exists
        # result = temp_db.connection.execute(
        #     "SELECT file_hash FROM imported_files WHERE file_hash = ?",
        #     (test_hash,)
        # ).fetchone()

        # assert result is not None
        # assert result[0] == test_hash


class TestGetDbFunction:
    """Tests for get_db global instance function"""

    def test_get_db_returns_instance(self):
        """Should return Database instance"""
        # Note: This uses actual default path, not temp DB
        # Consider mocking or skipping if it creates real files

        # db = get_db()
        # assert isinstance(db, Database)
        # assert db.connection is not None

    def test_get_db_singleton(self):
        """Should return same instance on multiple calls"""
        # db1 = get_db()
        # db2 = get_db()
        # assert db1 is db2
        pass  # Skip for now to avoid creating real DB


class TestDatabaseTransactions:
    """Tests for transaction handling"""

    def test_rollback_on_error(self, temp_db):
        """Should rollback transaction on error"""
        temp_db.connect()
        temp_db.initialize_schema()

        # When implemented, test transaction rollback:
        # try:
        #     with temp_db.connection.begin():
        #         # Insert valid record
        #         # Insert invalid record (should fail)
        #         pass
        # except Exception:
        #     pass

        # Verify first record was rolled back

    def test_commit_on_success(self, temp_db):
        """Should commit transaction on success"""
        temp_db.connect()
        temp_db.initialize_schema()

        # When implemented, test successful commit
