-- Migration 001: Add Continual Sync Fields
-- Date: 2025-11-22
-- Purpose: Enhance imported_files table to support Garmin Express auto-sync

-- Add columns to imported_files for sync tracking
ALTER TABLE imported_files ADD COLUMN IF NOT EXISTS file_size BIGINT;
ALTER TABLE imported_files ADD COLUMN IF NOT EXISTS modified_time TIMESTAMP;
ALTER TABLE imported_files ADD COLUMN IF NOT EXISTS first_seen_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;
ALTER TABLE imported_files ADD COLUMN IF NOT EXISTS source TEXT DEFAULT 'manual';
ALTER TABLE imported_files ADD COLUMN IF NOT EXISTS last_error TEXT;

-- Update existing records to have a source
UPDATE imported_files SET source = 'manual' WHERE source IS NULL;

-- Create table for tracking Garmin Express devices
CREATE TABLE IF NOT EXISTS garmin_express_devices (
    device_id TEXT PRIMARY KEY,
    device_path TEXT NOT NULL,
    device_name TEXT,
    enabled BOOLEAN DEFAULT TRUE,
    last_sync_at TIMESTAMP,
    file_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create index on source for faster filtering
CREATE INDEX IF NOT EXISTS idx_imported_files_source ON imported_files(source);
CREATE INDEX IF NOT EXISTS idx_imported_files_modified ON imported_files(modified_time);
