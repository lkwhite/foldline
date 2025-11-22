"""
Database Connection Manager

Handles initialization and connections to the local database.
Use DuckDB or SQLite based on preference.
"""

import os
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

# Choose your database backend
USE_DUCKDB = True  # Set to False to use SQLite instead

if USE_DUCKDB:
    import duckdb
else:
    import sqlite3


class Database:
    """Database connection manager"""

    def __init__(self, db_path: str = None):
        """
        Initialize database connection

        Args:
            db_path: Path to database file. If None, uses default location.
        """
        if db_path is None:
            # Default to user's home directory
            data_dir = Path.home() / ".foldline" / "data"
            data_dir.mkdir(parents=True, exist_ok=True)
            db_path = str(data_dir / "foldline.db")
        else:
            # Ensure parent directories exist for custom paths
            db_file_path = Path(db_path)
            db_file_path.parent.mkdir(parents=True, exist_ok=True)

        self.db_path = db_path
        self.connection = None

        logger.info(f"Database path: {self.db_path}")

    def connect(self):
        """Establish database connection"""
        if USE_DUCKDB:
            self.connection = duckdb.connect(self.db_path)
            logger.info("Connected to DuckDB")
        else:
            self.connection = sqlite3.connect(self.db_path)
            logger.info("Connected to SQLite")

        return self.connection

    def initialize_schema(self):
        """
        Initialize database schema from schema.sql
        """
        logger.info("Initializing database schema")

        if not self.connection:
            logger.error("No database connection available")
            return

        schema_path = Path(__file__).parent / "schema.sql"

        if not schema_path.exists():
            logger.warning("schema.sql not found, skipping initialization")
            return

        with open(schema_path) as f:
            schema_sql = f.read()

        try:
            if USE_DUCKDB:
                # DuckDB can execute multiple statements at once
                self.connection.execute(schema_sql)
            else:
                # SQLite needs executescript for multiple statements
                self.connection.executescript(schema_sql)

            logger.info("Schema initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize schema: {e}")
            raise

    def close(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()
            logger.info("Database connection closed")


# Global database instance
_db_instance = None


def get_db() -> Database:
    """
    Get the global database instance

    Returns:
        Database instance
    """
    global _db_instance

    if _db_instance is None:
        _db_instance = Database()
        _db_instance.connect()
        _db_instance.initialize_schema()

    return _db_instance
