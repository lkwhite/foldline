-- Migration 001: Add Continual Sync Fields
-- Date: 2025-11-22
-- Purpose: Enhance imported_files table to support Garmin Express auto-sync
--
-- NOTE: This migration is now obsolete as schema.sql already includes all these fields.
-- Keeping for historical reference, but all operations use IF NOT EXISTS to be idempotent.

-- These columns are already in schema.sql, so ALTER TABLE will be skipped if they exist
-- DuckDB doesn't support IF NOT EXISTS for ALTER TABLE ADD COLUMN, so we skip this
-- ALTER TABLE imported_files ADD COLUMN IF NOT EXISTS file_size BIGINT;
-- ALTER TABLE imported_files ADD COLUMN IF NOT EXISTS modified_time TIMESTAMP;
-- ALTER TABLE imported_files ADD COLUMN IF NOT EXISTS first_seen_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;
-- ALTER TABLE imported_files ADD COLUMN IF NOT EXISTS source TEXT DEFAULT 'manual';
-- ALTER TABLE imported_files ADD COLUMN IF NOT EXISTS last_error TEXT;

-- Update existing records to have a source (safe, won't affect new DBs)
-- UPDATE imported_files SET source = 'manual' WHERE source IS NULL;

-- Create table for tracking Garmin Express devices (idempotent with IF NOT EXISTS)
CREATE TABLE IF NOT EXISTS garmin_express_devices (
    device_id TEXT PRIMARY KEY,
    device_path TEXT NOT NULL,
    device_name TEXT,
    enabled BOOLEAN DEFAULT TRUE,
    last_sync_at TIMESTAMP,
    file_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes (idempotent with IF NOT EXISTS)
CREATE INDEX IF NOT EXISTS idx_imported_files_source ON imported_files(source);
CREATE INDEX IF NOT EXISTS idx_imported_files_modified ON imported_files(modified_time);
CREATE INDEX IF NOT EXISTS idx_garmin_express_enabled ON garmin_express_devices(enabled);
