-- Foldline Database Schema
-- This can be used with SQLite or DuckDB

-- ============================================================================
-- Configuration / Metadata
-- ============================================================================

CREATE TABLE IF NOT EXISTS config (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Store app settings like data_root, last_sync_time, etc.

-- ============================================================================
-- File Tracking (for deduplication)
-- ============================================================================

CREATE TABLE IF NOT EXISTS imported_files (
    file_hash TEXT PRIMARY KEY,
    file_path TEXT NOT NULL,
    file_type TEXT NOT NULL,  -- 'fit', 'tcx', 'json', 'zip'
    imported_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    record_count INTEGER DEFAULT 0
);

-- ============================================================================
-- Sleep Data
-- ============================================================================

CREATE TABLE IF NOT EXISTS sleep_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date DATE NOT NULL UNIQUE,
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    duration_minutes INTEGER,
    deep_sleep_minutes INTEGER,
    light_sleep_minutes INTEGER,
    rem_sleep_minutes INTEGER,
    awake_minutes INTEGER,
    sleep_score REAL,
    source_file_hash TEXT,
    imported_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (source_file_hash) REFERENCES imported_files(file_hash)
);

CREATE INDEX IF NOT EXISTS idx_sleep_date ON sleep_records(date);

-- ============================================================================
-- Heart Rate Data
-- ============================================================================

CREATE TABLE IF NOT EXISTS resting_hr (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date DATE NOT NULL UNIQUE,
    resting_hr INTEGER NOT NULL,
    source_file_hash TEXT,
    imported_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (source_file_hash) REFERENCES imported_files(file_hash)
);

CREATE INDEX IF NOT EXISTS idx_rhr_date ON resting_hr(date);

-- ============================================================================
-- HRV (Heart Rate Variability)
-- ============================================================================

CREATE TABLE IF NOT EXISTS hrv_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date DATE NOT NULL UNIQUE,
    hrv_value REAL NOT NULL,  -- Could be RMSSD, SDNN, etc.
    measurement_type TEXT,
    source_file_hash TEXT,
    imported_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (source_file_hash) REFERENCES imported_files(file_hash)
);

CREATE INDEX IF NOT EXISTS idx_hrv_date ON hrv_records(date);

-- ============================================================================
-- Stress Scores
-- ============================================================================

CREATE TABLE IF NOT EXISTS stress_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TIMESTAMP NOT NULL,
    stress_level INTEGER,  -- 0-100
    source_file_hash TEXT,
    imported_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (source_file_hash) REFERENCES imported_files(file_hash)
);

CREATE INDEX IF NOT EXISTS idx_stress_timestamp ON stress_records(timestamp);

-- Daily aggregated stress
CREATE TABLE IF NOT EXISTS daily_stress (
    date DATE PRIMARY KEY,
    avg_stress REAL,
    max_stress INTEGER,
    min_stress INTEGER,
    rest_stress REAL,
    activity_stress REAL
);

-- ============================================================================
-- Steps
-- ============================================================================

CREATE TABLE IF NOT EXISTS daily_steps (
    date DATE PRIMARY KEY,
    step_count INTEGER NOT NULL,
    distance_meters REAL,
    calories REAL,
    source_file_hash TEXT,
    imported_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (source_file_hash) REFERENCES imported_files(file_hash)
);

CREATE INDEX IF NOT EXISTS idx_steps_date ON daily_steps(date);

-- ============================================================================
-- Training Load / Activities
-- ============================================================================

CREATE TABLE IF NOT EXISTS activities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    activity_id TEXT UNIQUE,  -- Garmin activity ID
    start_time TIMESTAMP NOT NULL,
    activity_type TEXT,
    duration_seconds INTEGER,
    distance_meters REAL,
    avg_hr INTEGER,
    max_hr INTEGER,
    training_load REAL,
    training_effect_aerobic REAL,
    training_effect_anaerobic REAL,
    source_file_hash TEXT,
    imported_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (source_file_hash) REFERENCES imported_files(file_hash)
);

CREATE INDEX IF NOT EXISTS idx_activities_start ON activities(start_time);

-- ============================================================================
-- Views for quick queries
-- ============================================================================

-- Combined daily metrics view
CREATE VIEW IF NOT EXISTS daily_metrics AS
SELECT
    COALESCE(s.date, rhr.date, hs.date, ds.date) AS date,
    s.duration_minutes AS sleep_duration,
    s.sleep_score,
    rhr.resting_hr,
    hs.hrv_value,
    ds.avg_stress,
    ds.step_count
FROM sleep_records s
FULL OUTER JOIN resting_hr rhr ON s.date = rhr.date
FULL OUTER JOIN hrv_records hs ON s.date = hs.date
FULL OUTER JOIN (
    SELECT date, avg_stress FROM daily_stress
) ds ON s.date = ds.date
FULL OUTER JOIN daily_steps dsteps ON s.date = dsteps.date;
