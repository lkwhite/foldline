# Foldline Fitness Tracking Features - Implementation Plan

## 📋 Overview
Complete implementation of four key fitness tracking features: Daily Summaries (UDS), Fitness Assessments (VO2 Max), Menstrual Health Tracking, and Body Composition & Hydration. The database schemas are already complete - this plan focuses on building the parsing, processing, and API layers.

## Current Implementation Status

### 📊 Daily Summaries (UDS files) - **75% Complete**
- ✅ **Database schema** (`daily_summaries` table) - comprehensive fields for steps, calories, heart rate, stress, body battery
- ✅ **JSON parser** (`parse_daily_summary_json()`) - handles UDS file parsing
- ✅ **Database insertion** (`insert_daily_summary_data()`) - fully implemented with conflict handling
- ❌ **API endpoint processing** - stubbed out in `main.py:294-296` with TODO comment
- ❌ **Metrics analysis functions** - no heatmaps or trend analysis yet

### 🫁 Fitness Assessments (VO2 Max) - **20% Complete**
- ✅ **Database schema** (`fitness_assessments` table) - supports VO2 max, fitness age, MET values, sport tracking
- ❌ **JSON parser** - no parsing function exists
- ❌ **Database insertion** - no insertion function
- ❌ **API endpoints** - no VO2 progression tracking
- ❌ **FIT file extraction** - not implemented in `fit_folder.py`

### 🩸 Menstrual Health Tracking - **20% Complete**
- ✅ **Database schema** (`menstrual_cycles` table) - comprehensive cycle tracking with fertility windows, ovulation estimates
- ❌ **JSON parser** - no parsing function
- ❌ **Database insertion** - no insertion function
- ❌ **API endpoints** - no cycle tracking endpoints
- ❌ **Analysis functions** - no cycle predictions or insights

### ⚖️ Body Composition & Hydration - **20% Complete**
- ✅ **Database schemas** - `body_composition` (weight, body fat, muscle mass, BMI) and `hydration_logs` tables
- ❌ **JSON parsers** - no parsing functions for either feature
- ❌ **Database insertion** - no insertion functions
- ❌ **API endpoints** - no body metrics endpoints
- ❌ **FIT file support** - no extraction from FIT files

---

## 🎯 Phase 1: Complete Daily Summaries (Quick Win)
**Status**: 75% complete - just needs API wiring

### Task 1.1: Wire up Daily Summaries API Endpoint
**File**: `backend/main.py:294-296`
- Replace the TODO comment with actual implementation
- Call `process_daily_summary_json_files()` function
- Return processed data count and status
- **Reference**: `process_sleep_json_files()` at line 284 for pattern

### Task 1.2: Implement Daily Summaries Metrics
**Files**: `backend/metrics/` (create new file: `daily_summaries.py`)
- Build functions for:
  - `get_daily_steps_heatmap()` - step count calendar visualization
  - `get_calories_trends()` - calorie burn patterns over time
  - `get_heart_rate_zones()` - HR distribution analysis
  - `get_body_battery_analysis()` - energy level patterns
  - `get_stress_insights()` - stress level trends
- **Reference**: Existing stubs in `sleep.py`, `hrv.py` for function signatures

---

## 🎯 Phase 2: Fitness Assessments (VO2 Max Tracking)
**Status**: 20% complete - needs full implementation

### Task 2.1: Build Fitness Assessments JSON Parser
**File**: `backend/ingestion/json_parser.py`
- Add `parse_fitness_assessment_json(json_data)` function
- Parse fields: assessment_date, vo2_max_value, fitness_age, max_met, sport, sub_sport, calibrated_data
- **Reference**: `parse_daily_summary_json()` at lines 213-272 for structure

### Task 2.2: Database Insertion Function
**File**: `backend/ingestion/json_parser.py`
- Add `insert_fitness_assessment_data(conn, assessment_data)` function
- Implement ON CONFLICT DO UPDATE for deduplication
- **Reference**: `insert_daily_summary_data()` at lines 393-504 for pattern

### Task 2.3: Processing Pipeline and API
**File**: `backend/main.py`
- Add `process_fitness_assessment_json_files()` function
- Add API endpoint: `/api/fitness-assessments/process`
- **Reference**: `process_sleep_json_files()` for implementation pattern

### Task 2.4: VO2 Max Analysis Functions
**Files**: `backend/metrics/` (create: `fitness_assessments.py`)
- `get_vo2_max_progression()` - VO2 trends over time
- `get_fitness_age_analysis()` - fitness age vs chronological age
- `get_sport_specific_metrics()` - VO2 by sport/activity type
- `get_fitness_level_distribution()` - percentile rankings

---

## 🎯 Phase 3: Menstrual Health Tracking
**Status**: 20% complete - needs full implementation

### Task 3.1: Menstrual Cycle JSON Parser
**File**: `backend/ingestion/json_parser.py`
- Add `parse_menstrual_cycle_json(json_data)` function
- Parse: cycle_start_date, cycle_end_date, cycle_length_days, period_start_date, period_end_date, fertility_window_start, fertility_window_end, ovulation_estimated_date, etc.

### Task 3.2: Database Operations
**File**: `backend/ingestion/json_parser.py`
- Add `insert_menstrual_cycle_data(conn, cycle_data)` function
- Handle overlapping cycles and data updates

### Task 3.3: API and Analysis
**File**: `backend/main.py` + `backend/metrics/` (create: `menstrual_health.py`)
- Add processing function and API endpoint
- Analysis functions:
  - `get_cycle_length_trends()` - cycle regularity tracking
  - `get_fertility_window_predictions()` - ovulation predictions
  - `get_period_symptoms_correlation()` - if symptom data available

---

## 🎯 Phase 4: Body Composition & Hydration
**Status**: 20% complete - needs full implementation

### Task 4.1: Body Composition JSON Parser
**File**: `backend/ingestion/json_parser.py`
- Add `parse_body_composition_json(json_data)` function
- Parse: measurement_date, weight_kg, body_fat_percentage, muscle_mass_kg, bone_mass_kg, water_percentage, visceral_fat_rating, metabolic_age, bmi, measurement_source

### Task 4.2: Hydration JSON Parser
**File**: `backend/ingestion/json_parser.py`
- Add `parse_hydration_json(json_data)` function
- Parse: log_date, timestamp_gmt, value_ml, estimated_sweat_loss_ml, hydration_source, activity_id

### Task 4.3: Database Operations
**File**: `backend/ingestion/json_parser.py`
- Add `insert_body_composition_data(conn, body_data)` function
- Add `insert_hydration_data(conn, hydration_data)` function

### Task 4.4: API and Analysis
**Files**: `backend/main.py` + `backend/metrics/` (create: `body_metrics.py`)
- Add processing functions and API endpoints
- Analysis functions:
  - `get_weight_trends()` - weight change over time
  - `get_body_composition_analysis()` - muscle/fat ratio trends
  - `get_hydration_patterns()` - daily fluid intake patterns
  - `get_bmi_progression()` - BMI tracking and health ranges

---

## 🎯 Phase 5: FIT File Integration
**Status**: Needs extension for new data types

### Task 5.1: Extend FIT File Parser
**File**: `backend/ingestion/fit_folder.py`
- Modify `parse_fit_file()` function to extract:
  - Fitness test records (VO2 max assessments)
  - Body composition records (weight, body fat)
  - Hydration records (fluid intake)
- **Reference**: Existing sleep record extraction at lines 200+ for pattern

---

## 🎯 Phase 6: Testing & Validation

### Task 6.1: Comprehensive Test Suite
**Files**: `backend/tests/` directory
- Create test files for each new feature:
  - `test_daily_summaries.py`
  - `test_fitness_assessments.py`
  - `test_menstrual_health.py`
  - `test_body_composition.py`
  - `test_hydration.py`

### Task 6.2: Data Validation & Error Handling
**All parser files**
- Add input validation for JSON data
- Handle missing or malformed data gracefully
- Add logging for debugging
- Implement proper error responses in API endpoints

---

## 📁 Key File Locations

| Component | File Path | Status |
|-----------|-----------|--------|
| Database Schema | `backend/db/schema.sql:171-285` | ✅ Complete |
| JSON Parsers | `backend/ingestion/json_parser.py` | 🔄 Partial |
| FIT Processing | `backend/ingestion/fit_folder.py` | 🔄 Needs extension |
| API Endpoints | `backend/main.py` | 🔄 Mostly stubbed |
| Metrics Functions | `backend/metrics/*.py` | ❌ Empty placeholders |
| Database Connection | `backend/db/connection.py` | ✅ Complete |

---

## 🔧 Implementation Guidelines

1. **Follow Existing Patterns**: Use `parse_daily_summary_json()` and `insert_daily_summary_data()` as templates
2. **Error Handling**: Include try/catch blocks and proper logging
3. **Database Transactions**: Use connection transactions for data integrity
4. **API Consistency**: Follow FastAPI patterns established in existing endpoints
5. **Testing**: Write tests for each parser and database function
6. **Documentation**: Add docstrings to all new functions

---

## 📊 Expected Outcomes

After completion, the system will support:
- ✅ Complete daily activity summaries with visualizations
- ✅ VO2 max progression tracking and fitness assessments
- ✅ Menstrual cycle monitoring with predictions
- ✅ Body composition trends and hydration tracking
- ✅ Unified FIT file and JSON processing for all data types
- ✅ Comprehensive API endpoints for frontend integration

**Estimated Implementation Time**: 15-20 development sessions focusing on one feature at a time.

---

## 📝 Implementation Notes

### Data Sources Expected:
- **Daily Summaries**: UDS JSON files from Garmin Connect export
- **Fitness Assessments**: JSON files containing VO2 max test results
- **Menstrual Cycles**: JSON files from Garmin's menstrual tracking feature
- **Body Composition**: JSON files from compatible smart scales or manual entries
- **Hydration**: JSON files from Garmin hydration tracking or manual logs
- **FIT Files**: Binary FIT files containing comprehensive activity and health data

### Priority Order:
1. **Daily Summaries** - Quick win, mostly implemented
2. **Fitness Assessments** - High value for athletes and fitness enthusiasts
3. **Body Composition & Hydration** - Popular tracking metrics
4. **Menstrual Health** - Important for specific user segment
5. **FIT File Extensions** - Enhanced data capture
6. **Testing & Validation** - Ensure reliability

This plan provides a comprehensive roadmap for completing the fitness tracking features while building on the existing, well-designed database schema and established patterns in the codebase.