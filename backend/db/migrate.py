"""
Database Migration Runner

Applies migrations to the Foldline database.
"""

import os
import logging
from pathlib import Path
from typing import Optional
import duckdb
import sqlite3

logger = logging.getLogger(__name__)


def get_db_connection(db_path: str, use_duckdb: bool = True):
    """Get database connection (DuckDB or SQLite)"""
    if use_duckdb:
        try:
            conn = duckdb.connect(db_path)
            logger.info(f"Connected to DuckDB: {db_path}")
            return conn, "duckdb"
        except Exception as e:
            logger.warning(f"DuckDB connection failed: {e}, falling back to SQLite")

    conn = sqlite3.connect(db_path)
    logger.info(f"Connected to SQLite: {db_path}")
    return conn, "sqlite"


def get_applied_migrations(conn, db_type: str) -> set:
    """Get list of already-applied migrations"""
    try:
        if db_type == "duckdb":
            result = conn.execute("""
                SELECT migration_name FROM schema_migrations
                ORDER BY applied_at
            """).fetchall()
        else:
            cursor = conn.execute("""
                SELECT migration_name FROM schema_migrations
                ORDER BY applied_at
            """)
            result = cursor.fetchall()

        return {row[0] for row in result}
    except Exception:
        # schema_migrations table doesn't exist yet
        return set()


def create_migrations_table(conn, db_type: str):
    """Create the schema_migrations tracking table"""
    conn.execute("""
        CREATE TABLE IF NOT EXISTS schema_migrations (
            id INTEGER PRIMARY KEY,
            migration_name TEXT NOT NULL UNIQUE,
            applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    if db_type == "sqlite":
        conn.commit()
    logger.info("Created schema_migrations table")


def apply_migration(conn, db_type: str, migration_file: Path):
    """Apply a single migration file"""
    migration_name = migration_file.stem

    logger.info(f"Applying migration: {migration_name}")

    # Read migration SQL
    sql = migration_file.read_text()

    # Split into individual statements (basic split on semicolon)
    statements = [s.strip() for s in sql.split(';') if s.strip()]

    try:
        # Execute each statement
        for statement in statements:
            if statement and not statement.startswith('--'):
                conn.execute(statement)

        # Record migration as applied
        if db_type == "duckdb":
            conn.execute(
                "INSERT INTO schema_migrations (migration_name) VALUES (?)",
                [migration_name]
            )
        else:
            conn.execute(
                "INSERT INTO schema_migrations (migration_name) VALUES (?)",
                (migration_name,)
            )
            conn.commit()

        logger.info(f"✅ Migration applied: {migration_name}")
        return True

    except Exception as e:
        logger.error(f"❌ Migration failed: {migration_name} - {e}")
        if db_type == "sqlite":
            conn.rollback()
        raise


def run_migrations(db_path: str, migrations_dir: str, use_duckdb: bool = True):
    """
    Run all pending migrations

    Args:
        db_path: Path to database file
        migrations_dir: Directory containing migration files
        use_duckdb: Whether to use DuckDB (fallback to SQLite if False)
    """
    logger.info("Starting database migration...")

    # Connect to database
    conn, db_type = get_db_connection(db_path, use_duckdb)

    try:
        # Ensure migrations tracking table exists
        create_migrations_table(conn, db_type)

        # Get already-applied migrations
        applied = get_applied_migrations(conn, db_type)
        logger.info(f"Already applied migrations: {applied}")

        # Find migration files
        migrations_path = Path(migrations_dir)
        if not migrations_path.exists():
            logger.warning(f"Migrations directory not found: {migrations_dir}")
            return

        migration_files = sorted(migrations_path.glob("*.sql"))

        if not migration_files:
            logger.info("No migration files found")
            return

        # Apply pending migrations
        pending_count = 0
        for migration_file in migration_files:
            migration_name = migration_file.stem

            if migration_name in applied:
                logger.debug(f"⏭️  Skipping already-applied migration: {migration_name}")
                continue

            apply_migration(conn, db_type, migration_file)
            pending_count += 1

        if pending_count == 0:
            logger.info("✅ Database is up to date (no pending migrations)")
        else:
            logger.info(f"✅ Applied {pending_count} migration(s)")

    finally:
        conn.close()


if __name__ == "__main__":
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Default paths (can be overridden)
    DB_PATH = os.environ.get("FOLDLINE_DB_PATH", "./foldline.db")
    MIGRATIONS_DIR = os.path.join(
        os.path.dirname(__file__),
        "migrations"
    )

    logger.info(f"Database: {DB_PATH}")
    logger.info(f"Migrations directory: {MIGRATIONS_DIR}")

    # Run migrations
    run_migrations(DB_PATH, MIGRATIONS_DIR, use_duckdb=True)
