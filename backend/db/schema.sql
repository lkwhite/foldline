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
    id INTEGER PRIMARY KEY,
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
    imported_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_sleep_date ON sleep_records(date);

-- ============================================================================
-- Heart Rate Data
-- ============================================================================

CREATE TABLE IF NOT EXISTS resting_hr (
    id INTEGER PRIMARY KEY,
    date DATE NOT NULL UNIQUE,
    resting_hr INTEGER NOT NULL,
    source_file_hash TEXT,
    imported_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_rhr_date ON resting_hr(date);

-- ============================================================================
-- HRV (Heart Rate Variability)
-- ============================================================================

CREATE TABLE IF NOT EXISTS hrv_records (
    id INTEGER PRIMARY KEY,
    date DATE NOT NULL UNIQUE,
    hrv_value REAL NOT NULL,  -- Could be RMSSD, SDNN, etc.
    measurement_type TEXT,
    source_file_hash TEXT,
    imported_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_hrv_date ON hrv_records(date);

-- ============================================================================
-- Stress Scores
-- ============================================================================

CREATE TABLE IF NOT EXISTS stress_records (
    id INTEGER PRIMARY KEY,
    timestamp TIMESTAMP NOT NULL,
    stress_level INTEGER,  -- 0-100
    source_file_hash TEXT,
    imported_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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
    id INTEGER PRIMARY KEY,
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
    imported_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_activities_start ON activities(start_time);

-- ============================================================================
-- Enhanced Sleep Data (from JSON)
-- ============================================================================

CREATE TABLE IF NOT EXISTS sleep_detailed (
    id INTEGER PRIMARY KEY,
    date DATE NOT NULL UNIQUE,
    sleep_start_gmt TIMESTAMP,
    sleep_end_gmt TIMESTAMP,
    deep_sleep_seconds INTEGER,
    light_sleep_seconds INTEGER,
    rem_sleep_seconds INTEGER,
    awake_sleep_seconds INTEGER,
    sleep_window_confirmation_type TEXT,  -- ENHANCED_CONFIRMED_FINAL, etc.
    average_respiration REAL,
    lowest_respiration REAL,
    highest_respiration REAL,
    average_spo2 REAL,
    lowest_spo2 REAL,
    average_sleep_hr REAL,
    source_file_hash TEXT,
    imported_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_sleep_detailed_date ON sleep_detailed(date);
CREATE INDEX IF NOT EXISTS idx_sleep_detailed_confirmation ON sleep_detailed(sleep_window_confirmation_type);

-- ============================================================================
-- Daily Summaries (from UDS JSON files)
-- ============================================================================

CREATE TABLE IF NOT EXISTS daily_summaries (
    id INTEGER PRIMARY KEY,
    date DATE NOT NULL UNIQUE,
    step_count INTEGER,
    calories_burned REAL,
    distance_meters REAL,
    floors_climbed INTEGER,
    active_minutes INTEGER,
    sedentary_minutes INTEGER,
    min_heart_rate INTEGER,
    max_heart_rate INTEGER,
    resting_heart_rate INTEGER,
    avg_heart_rate INTEGER,
    stress_avg REAL,
    stress_max INTEGER,
    stress_min INTEGER,
    body_battery_charged INTEGER,
    body_battery_drained INTEGER,
    body_battery_start INTEGER,
    body_battery_end INTEGER,
    intensity_minutes_moderate INTEGER,
    intensity_minutes_vigorous INTEGER,
    source_file_hash TEXT,
    imported_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_daily_summaries_date ON daily_summaries(date);

-- ============================================================================
-- Fitness Assessments (VO2 Max, Fitness Age)
-- ============================================================================

CREATE TABLE IF NOT EXISTS fitness_assessments (
    id INTEGER PRIMARY KEY,
    assessment_date DATE NOT NULL,
    vo2_max_value REAL,
    fitness_age INTEGER,
    max_met REAL,
    sport TEXT,
    sub_sport TEXT,
    calibrated_data BOOLEAN,
    source_file_hash TEXT,
    imported_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(assessment_date, sport, sub_sport)
);

CREATE INDEX IF NOT EXISTS idx_fitness_assessments_date ON fitness_assessments(assessment_date);
CREATE INDEX IF NOT EXISTS idx_fitness_assessments_vo2 ON fitness_assessments(vo2_max_value);

-- ============================================================================
-- Hydration Logs
-- ============================================================================

CREATE TABLE IF NOT EXISTS hydration_logs (
    id INTEGER PRIMARY KEY,
    log_date DATE NOT NULL,
    timestamp_gmt TIMESTAMP NOT NULL,
    value_ml INTEGER,
    estimated_sweat_loss_ml INTEGER,
    hydration_source TEXT,  -- manual, activity, etc.
    activity_id TEXT,
    source_file_hash TEXT,
    imported_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_hydration_date ON hydration_logs(log_date);
CREATE INDEX IF NOT EXISTS idx_hydration_timestamp ON hydration_logs(timestamp_gmt);

-- ============================================================================
-- Menstrual Cycles
-- ============================================================================

CREATE TABLE IF NOT EXISTS menstrual_cycles (
    id INTEGER PRIMARY KEY,
    cycle_start_date DATE NOT NULL,
    cycle_end_date DATE,
    cycle_length_days INTEGER,
    period_start_date DATE,
    period_end_date DATE,
    period_length_days INTEGER,
    cycle_confirmed BOOLEAN,
    fertility_window_start DATE,
    fertility_window_end DATE,
    ovulation_estimated_date DATE,
    hormonal_contraception BOOLEAN,
    skin_temperature_enabled BOOLEAN,
    source_file_hash TEXT,
    imported_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_menstrual_cycles_start ON menstrual_cycles(cycle_start_date);
CREATE INDEX IF NOT EXISTS idx_menstrual_cycles_period ON menstrual_cycles(period_start_date);

-- ============================================================================
-- Body Composition & Biometrics
-- ============================================================================

CREATE TABLE IF NOT EXISTS body_composition (
    id INTEGER PRIMARY KEY,
    measurement_date DATE NOT NULL,
    weight_kg REAL,
    body_fat_percentage REAL,
    muscle_mass_kg REAL,
    bone_mass_kg REAL,
    water_percentage REAL,
    visceral_fat_rating INTEGER,
    metabolic_age INTEGER,
    bmi REAL,
    measurement_source TEXT,  -- scale, manual, etc.
    source_file_hash TEXT,
    imported_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_body_composition_date ON body_composition(measurement_date);
CREATE INDEX IF NOT EXISTS idx_body_composition_weight ON body_composition(weight_kg);

-- Additional indexes for JSON data performance
CREATE INDEX IF NOT EXISTS idx_daily_summaries_steps ON daily_summaries(step_count);
CREATE INDEX IF NOT EXISTS idx_daily_summaries_rhr ON daily_summaries(resting_heart_rate);
CREATE INDEX IF NOT EXISTS idx_fitness_assessments_sport ON fitness_assessments(sport, sub_sport);
CREATE INDEX IF NOT EXISTS idx_hydration_timestamp ON hydration_logs(timestamp_gmt);
CREATE INDEX IF NOT EXISTS idx_hydration_activity ON hydration_logs(activity_id);
CREATE INDEX IF NOT EXISTS idx_sleep_detailed_gmt ON sleep_detailed(sleep_start_gmt);
CREATE INDEX IF NOT EXISTS idx_body_composition_source ON body_composition(measurement_source);

-- ============================================================================
-- Views for quick queries
-- ============================================================================

-- Combined daily metrics view
CREATE VIEW IF NOT EXISTS daily_metrics AS
SELECT
    COALESCE(s.date, rhr.date, hs.date, dst.date, dsteps.date) AS date,
    s.duration_minutes AS sleep_duration,
    s.sleep_score,
    rhr.resting_hr,
    hs.hrv_value,
    dst.avg_stress,
    dsteps.step_count
FROM sleep_records s
FULL OUTER JOIN resting_hr rhr ON s.date = rhr.date
FULL OUTER JOIN hrv_records hs ON s.date = hs.date
FULL OUTER JOIN daily_stress dst ON s.date = dst.date
FULL OUTER JOIN daily_steps dsteps ON s.date = dsteps.date;
