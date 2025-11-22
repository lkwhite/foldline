# Foldline Integration Plan: Handoff Doc vs. Current Codebase

**Date:** 2025-11-22
**Purpose:** Integrate knowledge from gar-mining handoff document with current Foldline implementation

---

## Executive Summary

The Foldline codebase has **exceeded** the handoff document recommendations in architecture and schema design, but is missing the **analytics algorithms** and **complete data import pipeline** that gar-mining perfected over years of production use.

**Current State:**
- ✅ **Architecture**: Superior (Tauri + SvelteKit + FastAPI vs. Streamlit)
- ✅ **Database**: Already using DuckDB as recommended
- ✅ **Schema**: More comprehensive than handoff (15 tables vs. 7)
- 🟨 **Data Import**: FIT parsing functional but GDPR extraction incomplete
- ❌ **Analytics**: All algorithms stubbed (this is the critical gap)
- ❌ **Visualization**: Not yet implemented (Plotly recommended)

**Integration Priority:**
1. **Port analytics algorithms** from handoff doc (highest value)
2. **Complete GDPR import** using handoff patterns
3. **Implement Plotly visualizations** using proven patterns
4. **Enhance FIT parsing** with handoff field mapping knowledge

---

## Detailed Comparison Matrix

| Feature | Handoff Doc (gar-mining) | Current Foldline | Status | Action |
|---------|--------------------------|------------------|--------|---------|
| **Architecture** |
| App Type | Streamlit web app | Tauri desktop app | ✅ Superior | Keep Foldline's approach |
| Backend | Python + Streamlit | FastAPI + Tauri | ✅ Superior | Keep Foldline's approach |
| Database | SQLite (manual schema) | DuckDB (w/ SQLite fallback) | ✅ Better | Keep DuckDB |
| Data Models | Python @dataclass | Pydantic (planned) | 🟨 Good | Implement Pydantic models |
| **Data Sources** |
| Primary Source | Garmin API (OAuth) | GDPR exports + FIT files | ✅ Better | No API = better privacy |
| API Client | garth + garminconnect | N/A (local-only) | ✅ Advantage | Keep local approach |
| FIT Parsing | Not implemented | fitparse library | ✅ Implemented | Enhance with handoff knowledge |
| GDPR Import | N/A (API-only) | Stub implementation | ❌ Missing | **Port from handoff** |
| **Database Schema** |
| Activities | ✅ Implemented | ✅ Enhanced version | ✅ Superior | Keep Foldline's |
| Sleep | ✅ Basic | ✅ Two tables (summary + detailed) | ✅ Superior | Keep both tables |
| Daily Stats | ✅ Implemented | ✅ daily_summaries table | ✅ Equivalent | Keep Foldline's |
| Stress | ✅ Implemented | ✅ Two tables (realtime + daily) | ✅ Superior | Keep both tables |
| Heart Rate | ✅ Two tables | ✅ resting_hr table | 🟨 Partial | Add HR time-series table |
| HRV | ❌ Not in schema | ✅ hrv_records table | ✅ Superior | Foldline innovation |
| Menstrual Cycles | ❌ Future feature | ✅ Implemented | ✅ Superior | Foldline innovation |
| Hydration | ❌ Not planned | ✅ hydration_logs table | ✅ Superior | Foldline innovation |
| Body Composition | ❌ Not planned | ✅ body_composition table | ✅ Superior | Foldline innovation |
| Fitness Assessments | ❌ Not planned | ✅ fitness_assessments table | ✅ Superior | Foldline innovation |
| File Tracking | ❌ No deduplication | ✅ imported_files (SHA256) | ✅ Superior | Keep Foldline's |
| Raw Data Backup | ✅ raw_data column | ❌ Not in schema | ❌ Missing | **Add raw_data columns** |
| **Analytics Algorithms** |
| Sleep-Activity Correlation | ✅ Fully implemented | ❌ Stubbed | ❌ Critical gap | **Port algorithm** |
| Health Score | ✅ Multi-metric weighted | ❌ Stubbed | ❌ Critical gap | **Port algorithm** |
| Recovery Detection | ✅ Composite scoring | ❌ Stubbed | ❌ Critical gap | **Port algorithm** |
| Stress Patterns | ✅ Day-of-week, chronic detection | ❌ Stubbed | ❌ Critical gap | **Port algorithm** |
| Correlation Matrix | ✅ Pearson + significance | 🟨 API defined | 🟨 Partial | **Implement logic** |
| Optimal Activity Range | ✅ Quartile analysis | ❌ Not planned | ❌ Nice-to-have | Port later |
| **Data Processing** |
| FIT File Scanning | N/A | ✅ Recursive directory scan | ✅ Implemented | Enhance with handoff |
| FIT Message Parsing | N/A | ✅ fitparse integration | ✅ Implemented | Add more message types |
| JSON Parsing | N/A | ✅ Sleep + UDS files | ✅ Implemented | Add more JSON types |
| Deduplication | ❌ INSERT OR REPLACE | ✅ SHA256 file hashing | ✅ Superior | Keep Foldline's |
| Error Resilience | ✅ Per-item try/catch | ✅ Implemented in FIT parser | ✅ Good | Keep pattern |
| Progress Tracking | ✅ SyncStatus model | 🟨 Planned (WebSocket) | 🟨 Partial | Implement WebSocket |
| **Visualization** |
| Library | Plotly | ❌ Not chosen | ❌ Missing | **Use Plotly** |
| Time Series Charts | ✅ Multi-panel with shared x-axis | ❌ Stubbed | ❌ Missing | **Port examples** |
| Heatmaps | ✅ Calendar heatmap | ❌ Stubbed | ❌ Missing | **Port examples** |
| Correlation Plots | ✅ Scatter + trend line | ❌ Stubbed | ❌ Missing | **Port examples** |
| Quality Zones | ✅ Background color bands | ❌ Not planned | ❌ Nice-to-have | Port later |
| Dashboard Layout | ✅ Streamlit columns | ✅ SvelteKit grid | ✅ Equivalent | Adapt patterns |
| **API Endpoints** |
| Health Check | ✅ Implicit | ✅ GET / | ✅ Implemented | Keep |
| Import GDPR | N/A | 🟨 POST /import/garmin-export | 🟨 Stub | **Complete implementation** |
| Import FIT Folder | N/A | ✅ POST /import/fit-folder | ✅ Implemented | Enhance |
| Import JSON Folder | N/A | ✅ POST /import/json-folder | ✅ Implemented | Enhance |
| Metrics Heatmap | N/A | 🟨 GET /metrics/heatmap | 🟨 Stub | **Implement queries** |
| Metrics Timeseries | N/A | 🟨 GET /metrics/timeseries | 🟨 Stub | **Implement queries** |
| Correlation | N/A | 🟨 GET /metrics/correlation | 🟨 Stub | **Implement algorithm** |
| Data Export | ✅ CSV export | ❌ Not implemented | ❌ Nice-to-have | Port later |
| **Frontend UI** |
| Navigation | Streamlit sidebar | ✅ SvelteKit navbar | ✅ Superior | Keep |
| Setup Page | N/A | ✅ Implemented | ✅ New feature | Keep |
| Dashboard | ✅ Streamlit metrics | ✅ SvelteKit cards | ✅ Equivalent | Enhance with handoff patterns |
| Heatmap View | ❌ Not implemented | ✅ UI ready | ✅ Superior | Add visualization library |
| Trends View | ✅ Time series page | ✅ UI ready | ✅ Equivalent | Add visualization library |
| Correlation View | ✅ Scatter plots | ✅ UI ready | ✅ Equivalent | Add visualization library |
| Settings | ✅ Basic config | ✅ Implemented | ✅ Equivalent | Keep |
| Theme Toggle | N/A | ✅ Dark/light mode | ✅ Superior | Foldline innovation |
| **Advanced Features** |
| Annotation System | ✅ Proposed (not implemented) | ❌ Not planned | ❌ Future | Add to roadmap |
| Predictive Models | ✅ Proposed (not implemented) | ❌ Not planned | ❌ Future | Add to roadmap |
| Flexible Time Windows | ✅ Proposed (not implemented) | ❌ Not planned | ❌ Future | Add to roadmap |
| Relationship Explorer | ✅ Proposed (not implemented) | ❌ Not planned | ❌ Future | Add to roadmap |
| FIT Directory Watcher | ✅ Proposed (not implemented) | ❌ Not planned | ❌ Future | Add to roadmap |

---

## Critical Gaps to Address

### Gap 1: Analytics Algorithms (HIGHEST PRIORITY)

**Problem:** All analytics functions return stubs or empty data.

**Impact:** Users can import data but cannot gain insights from it.

**Files Affected:**
- `backend/metrics/sleep.py` (all functions stubbed)
- `backend/metrics/hrv.py` (all functions stubbed)
- `backend/metrics/stress.py` (all functions stubbed)
- `backend/metrics/steps.py` (all functions stubbed)

**Solution from Handoff:** Port complete implementations from FOLDLINE_HANDOFF.md lines 744-2612

**Specific Algorithms to Port:**

1. **Sleep-Activity Correlation** (lines 753-793)
   ```python
   # From handoff: Bidirectional correlation with lagged features
   def analyze_sleep_to_activity(date_range):
       - Join sleep data with next-day activities
       - Add 7-day rolling averages
       - Calculate Pearson correlations with p-values
       - Return significant correlations (p < 0.05)
   ```
   **Port to:** New file `backend/analytics/correlation.py`

2. **Health Metrics Analyzer** (lines 795-888)
   ```python
   # From handoff: Multi-metric daily health query
   def get_daily_health_metrics(start_date, end_date):
       - JOIN all health data sources (sleep, stress, HR, steps)
       - Add derived metrics (sleep efficiency, HR range, deep sleep %)
       - Add lagged features (prev day, 7-day avg, 30-day baseline)
       - Return comprehensive DataFrame
   ```
   **Port to:** New file `backend/analytics/health_metrics.py`

3. **Recovery Day Detection** (lines 891-929)
   ```python
   # From handoff: Composite recovery score
   def identify_recovery_days(df, threshold=60):
       - Calculate HR deviation from baseline
       - Combine with sleep score and stress level
       - Weighted average (HR 40%, Sleep 30%, Stress 30%)
       - Flag days below threshold as needing recovery
   ```
   **Port to:** New file `backend/analytics/recovery.py`

4. **Health Score Generation** (lines 938-982)
   ```python
   # From handoff: 0-100 composite wellness score
   def generate_health_score(df):
       - Sleep score (already 0-100)
       - Activity score (steps / 10k goal)
       - Stress score (inverted)
       - HR score (deviation from baseline)
       - Weighted: Sleep 30%, Activity 25%, Stress 25%, HR 20%
   ```
   **Port to:** New file `backend/analytics/health_score.py`

5. **Stress Pattern Analysis** (lines 985-1025)
   ```python
   # From handoff: Comprehensive stress insights
   def analyze_stress_patterns(df):
       - Distribution by qualifier (calm/balanced/stressful)
       - Day-of-week patterns
       - Weekend vs. weekday comparison
       - Chronic stress detection (7+ days >55)
       - Correlations with sleep/steps/HR
   ```
   **Port to:** `backend/analytics/stress_analysis.py`

6. **Optimal Activity Range** (lines 1028-1091)
   ```python
   # From handoff: Find sweet spot for activity
   def get_optimal_activity_range(df, metric='steps'):
       - Quartile-based grouping
       - Analyze next-day recovery metrics
       - Find optimal quartile (best recovery)
       - Return recommended range
   ```
   **Port to:** `backend/analytics/activity_optimization.py`

**Implementation Priority:**
1. Health Metrics Analyzer (foundation for others)
2. Health Score Generation (visible user value)
3. Recovery Day Detection (training insight)
4. Sleep-Activity Correlation (research value)
5. Stress Pattern Analysis (health insight)
6. Optimal Activity Range (nice-to-have)

---

### Gap 2: Complete GDPR Import Pipeline

**Problem:** `backend/ingestion/garmin_gdpr.py` is entirely stubbed.

**Impact:** Users cannot easily import their complete Garmin data history.

**Solution from Handoff:** Implement extraction and parsing (lines 1456-1521)

**Implementation Steps:**

1. **ZIP Extraction** (lines 1459-1480)
   ```python
   # GDPR Export Structure (from handoff lines 716-728)
   garmin_export.zip
   ├── DI_CONNECT/
   │   ├── DI-Connect-Fitness/
   │   │   ├── <timestamp>_ACTIVITY.fit
   │   ├── DI-Connect-Wellness/
   │   │   ├── <date>_SLEEP.json
   │   │   ├── <date>_DAILYSUMMARY.json
   │   └── DI-Connect-User/
   │       └── user_profile.json
   ```

2. **GDPR JSON Field Mapping** (lines 1507-1521)
   ```python
   # Handoff shows GDPR uses different field names than API
   GDPR Field Name          → Foldline Schema Column
   ────────────────────────────────────────────────────
   sleepStartTimestampGMT   → start_time
   sleepEndTimestampGMT     → end_time
   totalSleepTime           → duration_minutes (convert from minutes)
   deepSleepSeconds         → deep_sleep_minutes (convert)
   lightSleepSeconds        → light_sleep_minutes
   remSleepSeconds          → rem_sleep_minutes
   awakeSleepSeconds        → awake_minutes
   ```

3. **Progress Tracking** (lines 1481-1505)
   - Use same pattern as `fit_folder.py`
   - Track total files vs. processed
   - Return summary with counts

**Port to:** `backend/ingestion/garmin_gdpr.py`

**Reference Implementation:**
- Handoff lines 1456-1557 (GDPR Importer class)
- Handoff lines 1523-1557 (FIT File Watcher - for future auto-sync)

---

### Gap 3: Visualization Library Integration

**Problem:** All chart views show "Data preview" stubs.

**Impact:** Users cannot see their data visually.

**Solution from Handoff:** Use Plotly (lines 1095-1380)

**Why Plotly (from handoff lines 1097-1104):**
- ✅ Interactive (zoom, pan, hover)
- ✅ Works in both Streamlit and SvelteKit (plotly.js)
- ✅ High-quality out of the box
- ✅ Complex layouts (subplots, dual axes)

**Proven Patterns to Port:**

1. **Time Series with Multiple Metrics** (lines 1108-1171)
   - Multi-panel subplots with shared x-axis
   - 7-day rolling averages as dashed lines
   - Goal lines (e.g., 10k steps)
   - Example: Stress + Resting HR + Steps

2. **Calendar Heatmap** (lines 1173-1200)
   - Week-by-week grid
   - Color intensity by value
   - Faceted by year

3. **Correlation Heatmap** (lines 1202-1230)
   - Square matrix layout
   - RdBu colorscale (red-white-blue)
   - Annotated with correlation values
   - Midpoint at 0

4. **Sleep Quality Zones** (lines 1232-1273)
   - Line chart with background color bands
   - Green (80-100), Yellow (60-80), Red (0-60)
   - Annotations for zone labels

5. **Scatter with Trend Line** (lines 1299-1332)
   - Scatter plot with size/color encoding
   - Linear regression trend line
   - Display r and p-values in title

**Implementation Strategy:**

**Frontend (SvelteKit):**
```typescript
// Install: npm install plotly.js-dist
import Plotly from 'plotly.js-dist';

// Fetch data from API
const data = await apiGet('/metrics/timeseries?metric=sleep&...');

// Render (from handoff lines 1732-1748)
const trace = {
    x: data.map(d => d.date),
    y: data.map(d => d.value),
    type: 'scatter',
    mode: 'lines'
};

Plotly.newPlot('chart-container', [trace], layout);
```

**Port to:**
- `frontend/src/lib/components/TimeSeriesChart.svelte`
- `frontend/src/lib/components/HeatmapChart.svelte`
- `frontend/src/lib/components/CorrelationChart.svelte`

---

### Gap 4: Missing Heart Rate Time Series Table

**Problem:** Foldline has `resting_hr` but not intra-day HR time series.

**Impact:** Cannot analyze HR patterns during activities or throughout the day.

**Solution from Handoff:** Add `heart_rate` table for high-resolution data (lines 359-376)

**Schema to Add:**

```sql
-- From handoff lines 359-376
CREATE TABLE IF NOT EXISTS heart_rate_timeseries (
    id INTEGER PRIMARY KEY,
    timestamp TIMESTAMP NOT NULL,
    heart_rate INTEGER NOT NULL,
    activity_id TEXT,  -- NULL for all-day monitoring, set for workouts
    source_file_hash TEXT,
    imported_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_hr_timestamp ON heart_rate_timeseries(timestamp);
CREATE INDEX idx_hr_activity ON heart_rate_timeseries(activity_id);
```

**Note:** This is a high-volume table (thousands of rows per activity). Consider DuckDB's columnar storage advantage here.

---

### Gap 5: Raw Data Backup Columns

**Problem:** No `raw_data TEXT` columns to store original JSON/FIT contents.

**Impact:** Cannot re-parse if schema changes or new fields are discovered.

**Solution from Handoff:** Add raw_data columns (lines 1981-1997)

**Rationale (from handoff lines 1983-1997):**
> "Real Example: Initially didn't capture training_effect. Found it in raw_data JSON 6 months later. Re-parsed without re-syncing."

**Schema Changes:**

```sql
-- Add to existing tables
ALTER TABLE sleep_records ADD COLUMN raw_data TEXT;
ALTER TABLE sleep_detailed ADD COLUMN raw_data TEXT;
ALTER TABLE activities ADD COLUMN raw_data TEXT;
ALTER TABLE daily_summaries ADD COLUMN raw_data TEXT;
ALTER TABLE stress_records ADD COLUMN raw_data TEXT;
-- etc. for all primary data tables
```

**Update Parsers:**
```python
# In fit_folder.py and json_parser.py
import json

# When inserting, also store raw:
sleep_record = {
    'date': parsed_date,
    'duration_minutes': duration,
    # ... other fields ...
    'raw_data': json.dumps(original_fit_messages)  # Store original
}
```

---

### Gap 6: Field Name Variation Handling

**Problem:** GDPR exports may use different field names than current parsers expect.

**Impact:** Parsing failures or missing data.

**Solution from Handoff:** Implement fallback field name pattern (lines 1961-1977)

**From handoff lines 1967-1973:**
```python
# Field Name Variations (from API experience, apply to GDPR too)
steps = data.get("steps") or data.get("totalSteps") or 0
resting_hr = data.get("restingHr") or data.get("restingHeartRate") or 0
```

**Enhance Parsers:**

```python
# In json_parser.py
def parse_daily_summary_json(json_data, file_path):
    # Use fallback pattern for robustness
    steps = json_data.get("totalSteps") or json_data.get("steps") or 0
    resting_hr = (
        json_data.get("restingHeartRate") or
        json_data.get("restingHr") or
        json_data.get("rhr") or
        None
    )
    # ... etc.
```

**Create Mapping Module:**
```python
# New file: backend/ingestion/field_mappings.py
SLEEP_FIELD_MAPPINGS = {
    'duration': ['totalSleepTime', 'sleepTimeSeconds', 'duration_minutes'],
    'deep_sleep': ['deepSleepSeconds', 'deepSleepDuration', 'deep_minutes'],
    # ... complete mapping for all fields
}

def get_field_value(data: dict, canonical_name: str, mappings: dict):
    """Try all known field name variations"""
    for variant in mappings.get(canonical_name, [canonical_name]):
        if variant in data:
            return data[variant]
    return None
```

---

## Schema Enhancements (Based on Handoff)

### Enhancement 1: Add Source Tracking to Activities

**Current:** Activities table exists but doesn't track source.

**Handoff Recommendation:** Lines 355-357
```sql
ALTER TABLE activities ADD COLUMN source TEXT;      -- 'gdpr', 'fit_file', 'manual'
ALTER TABLE activities ADD COLUMN file_path TEXT;   -- Link to original FIT
```

**Benefit:** Helps debug parsing issues and provides data provenance.

### Enhancement 2: Rename sync_log → import_log

**Current:** No sync_log or import_log table yet.

**Handoff Recommendation:** Lines 474-477
```sql
CREATE TABLE import_log (
    id INTEGER PRIMARY KEY,
    import_type TEXT NOT NULL,      -- 'gdpr_zip', 'fit_directory', 'manual'
    status TEXT NOT NULL,            -- 'success', 'error', 'partial'
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    files_processed INTEGER DEFAULT 0,
    records_inserted INTEGER DEFAULT 0,
    duplicates_skipped INTEGER DEFAULT 0,
    errors_count INTEGER DEFAULT 0,
    error_details TEXT,              -- JSON array of error messages
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Benefit:** Track import history for troubleshooting.

### Enhancement 3: Add Annotations Table

**Current:** Not in schema.

**Handoff Recommendation:** Lines 2671-2680 (future feature)
```sql
CREATE TABLE annotations (
    id INTEGER PRIMARY KEY,
    calendar_date TEXT NOT NULL,
    label TEXT NOT NULL,
    category TEXT,       -- 'life_event', 'illness', 'travel', 'injury'
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_annotations_date ON annotations(calendar_date);
```

**Benefit:** Let users explain metric anomalies (e.g., "Started new job" on high stress day).

---

## Proven Design Patterns to Adopt

### Pattern 1: Error Resilience (Lines 1999-2069)

**Current:** FIT folder parser uses this ✅
**Handoff Wisdom:**
```python
# DON'T do all-or-nothing:
for file in files:
    parse(file)  # Fails entire import if one file is corrupted

# DO per-item resilience:
for file in files:
    try:
        parse(file)
    except Exception as e:
        log_error(file, e)
        continue  # Keep processing other files
```

**Apply to:** GDPR importer when implemented.

### Pattern 2: Personal Baselines (Lines 2089-2102)

**Handoff Wisdom:** Same metric means different things for different people.

**Example:**
- Office worker: 10k steps = very active
- Warehouse worker: 10k steps = slow day

**Solution:**
- Use 30-day rolling averages as personal baselines
- Show percentile-based insights ("top 10% for you")
- Allow user-configurable goals

**Implement in:** Health score and recovery detection algorithms.

### Pattern 3: Date Attribution Clarity (Lines 2103-2123)

**Problem:** If you sleep 11pm Nov 21 → 7am Nov 22, which date?

**Garmin's Choice:** Date sleep **ended** (Nov 22)
**Impact on Analysis:** Must offset when correlating sleep → next-day activity

**Current Foldline Schema:** Uses `date DATE` in `sleep_records` but doesn't document attribution.

**Action:** Add comment to schema:
```sql
CREATE TABLE IF NOT EXISTS sleep_records (
    id INTEGER PRIMARY KEY,
    date DATE NOT NULL UNIQUE,  -- Date sleep ENDED (Garmin convention)
    -- ... rest of schema
);
```

### Pattern 4: Visualization Performance (Lines 2124-2145)

**Handoff Wisdom:** Plotly gets slow with >10k points.

**Solutions:**
1. Downsample for display
2. Aggregate to higher granularity (hourly → daily)
3. Use WebGL mode for large datasets

**Implement in:** Time series queries
```python
# In metrics/sleep.py
def get_sleep_timeseries(db, start_date, end_date, max_points=1000):
    # If date range too large, aggregate
    days = (end_date - start_date).days

    if days > 365:
        # Show weekly averages
        query = "SELECT DATE_TRUNC('week', date), AVG(duration_minutes) ..."
    elif days > 30:
        # Show daily values
        query = "SELECT date, duration_minutes ..."
    else:
        # Could show hourly if we had that data
        query = "SELECT date, duration_minutes ..."
```

---

## Implementation Roadmap

### Phase 1: Analytics Foundation (2-3 weeks)

**Goal:** Users can gain insights from imported data.

**Tasks:**
1. ✅ Create new directory: `backend/analytics/`
2. ✅ Port Health Metrics Analyzer
   - File: `backend/analytics/health_metrics.py`
   - Function: `get_daily_health_metrics(db, start_date, end_date)`
   - Returns unified DataFrame with all metrics + derived features

3. ✅ Implement actual metric queries
   - Update `backend/metrics/sleep.py::get_sleep_heatmap()`
   - Update `backend/metrics/sleep.py::get_sleep_timeseries()`
   - Update `backend/metrics/hrv.py::get_hrv_heatmap()`
   - Update `backend/metrics/stress.py::get_stress_heatmap()`
   - Update `backend/metrics/steps.py::get_steps_heatmap()`

4. ✅ Port Health Score algorithm
   - File: `backend/analytics/health_score.py`
   - Add endpoint: `GET /analytics/health-score?start_date&end_date`

5. ✅ Port Recovery Detection
   - File: `backend/analytics/recovery.py`
   - Add endpoint: `GET /analytics/recovery-days?start_date&end_date&threshold`

6. ✅ Port Correlation Analysis
   - File: `backend/analytics/correlation.py`
   - Implement: `GET /metrics/correlation` (currently stubbed)
   - Include Pearson, Spearman, p-values, lag support

**Deliverable:** Users can view heatmaps, trends, correlations, health scores, and recovery recommendations.

---

### Phase 2: Visualization (1-2 weeks)

**Goal:** Beautiful, interactive charts.

**Tasks:**
1. ✅ Install Plotly in frontend
   ```bash
   cd frontend
   npm install plotly.js-dist
   ```

2. ✅ Create chart components
   - `frontend/src/lib/components/TimeSeriesChart.svelte`
   - `frontend/src/lib/components/HeatmapChart.svelte`
   - `frontend/src/lib/components/CorrelationScatter.svelte`
   - `frontend/src/lib/components/HealthScoreGauge.svelte`

3. ✅ Integrate into pages
   - Update `frontend/src/routes/heatmaps/+page.svelte`
   - Update `frontend/src/routes/trends/+page.svelte`
   - Update `frontend/src/routes/correlation/+page.svelte`

4. ✅ Port visualization patterns from handoff
   - Multi-panel time series (handoff lines 1108-1171)
   - Calendar heatmap (lines 1173-1200)
   - Correlation matrix heatmap (lines 1202-1230)
   - Scatter with trend line (lines 1299-1332)

**Deliverable:** All visualization pages functional with Plotly charts.

---

### Phase 3: Complete GDPR Import (1 week)

**Goal:** One-click GDPR export import.

**Tasks:**
1. ✅ Implement `extract_garmin_export()` in `backend/ingestion/garmin_gdpr.py`
   - Extract ZIP to temporary directory
   - Categorize files by type (FIT, JSON, TCX)
   - Return file inventory

2. ✅ Implement `process_gdpr_export()` pipeline
   - Extract ZIP
   - Process all FIT files (use existing `process_fit_folder()`)
   - Process all JSON files (use existing `process_sleep_json_files()`)
   - Return comprehensive summary

3. ✅ Update `POST /import/garmin-export` endpoint
   - Currently stubbed in `backend/main.py`
   - Call `process_gdpr_export()`
   - Return detailed import summary

4. ✅ Test with real GDPR export
   - Use test file from gar-mining project
   - Validate all data types imported correctly

**Deliverable:** Users can import their complete Garmin history with one ZIP file.

---

### Phase 4: Schema Enhancements (3-5 days)

**Goal:** Add missing columns and tables from handoff recommendations.

**Tasks:**
1. ✅ Add `raw_data` columns to all primary tables
   ```sql
   ALTER TABLE sleep_records ADD COLUMN raw_data TEXT;
   ALTER TABLE activities ADD COLUMN raw_data TEXT;
   -- ... etc.
   ```

2. ✅ Add source tracking to activities
   ```sql
   ALTER TABLE activities ADD COLUMN source TEXT;
   ALTER TABLE activities ADD COLUMN file_path TEXT;
   ```

3. ✅ Create `import_log` table
   - Track all import operations
   - Store error details

4. ✅ Create `heart_rate_timeseries` table
   - For intra-day HR data
   - High-volume table (use DuckDB columnar advantage)

5. ✅ Update parsers to populate new columns
   - `fit_folder.py`: Store raw FIT messages in `raw_data`
   - `json_parser.py`: Store original JSON in `raw_data`

6. ✅ Migration script
   - `backend/db/migrations/001_add_raw_data_columns.sql`
   - Apply to existing databases

**Deliverable:** Enhanced schema with data provenance and re-parsing capability.

---

### Phase 5: Advanced Analytics (1-2 weeks)

**Goal:** Sophisticated insights and patterns.

**Tasks:**
1. ✅ Port Stress Pattern Analysis
   - File: `backend/analytics/stress_analysis.py`
   - Day-of-week patterns
   - Weekend vs. weekday
   - Chronic stress detection
   - Add endpoint: `GET /analytics/stress-patterns`

2. ✅ Port Sleep-Activity Correlation
   - File: `backend/analytics/sleep_activity.py`
   - Bidirectional analysis
   - Lagged correlations
   - Statistical significance testing
   - Add endpoint: `GET /analytics/sleep-activity-correlation`

3. ✅ Port Optimal Activity Range
   - File: `backend/analytics/activity_optimization.py`
   - Quartile analysis
   - Next-day recovery metrics
   - Add endpoint: `GET /analytics/optimal-activity-range`

4. ✅ Create comprehensive dashboard endpoint
   - Add: `GET /analytics/dashboard?date_range_days=30`
   - Returns all key metrics in one call:
     - Health score
     - Recovery status
     - Stress patterns
     - Sleep quality summary
     - Activity trends

**Deliverable:** Advanced analytics dashboard with actionable insights.

---

### Phase 6: Future Features (Future)

**Goal:** Implement proposed features from handoff doc.

**From handoff lines 2616-2776:**

1. **Annotations System**
   - Create `annotations` table
   - UI to add/edit annotations
   - Display on charts (vertical lines with labels)
   - Endpoint: `POST /annotations`, `GET /annotations`

2. **Flexible Time Windows**
   - Support grouping by: day, week, month, year
   - Year-over-year comparisons
   - Seasonal pattern analysis

3. **Relationship Explorer**
   - Interactive scatter plot
   - Dynamic axis selection (X, Y, Color, Size)
   - Real-time correlation calculation

4. **Predictive Models**
   - Predict tomorrow's stress/sleep/recovery
   - Use linear regression or XGBoost
   - Display confidence intervals

5. **FIT Directory Watcher**
   - Monitor `~/Garmin/` or user-selected directory
   - Auto-import new FIT files
   - Notify user of new activities

6. **Data Export**
   - CSV export for all data types
   - Parquet export for data science workflows
   - Endpoint: `GET /export/csv/{data_type}`

---

## Key Decisions Required

### Decision 1: DuckDB vs. SQLite

**Handoff Recommendation:** DuckDB (lines 1909-1939)
**Current Foldline:** DuckDB with SQLite fallback
**Recommendation:** **Keep DuckDB** ✅

**Rationale:**
- Better analytics performance (columnar storage)
- Native JSON support (for `raw_data` columns)
- Superior window functions (for rolling averages)
- Still local/embedded (privacy-first requirement)

**Action:** Remove SQLite fallback to simplify codebase.

### Decision 2: Plotly vs. Alternatives

**Handoff Recommendation:** Plotly (lines 1095-1104)
**Current Foldline:** Not chosen
**Recommendation:** **Use Plotly** ✅

**Rationale:**
- Battle-tested in gar-mining
- Works in both server (gar-mining) and client (Foldline)
- Interactive out of the box
- Complete examples in handoff doc

**Action:** Install `plotly.js-dist` and port visualization examples.

### Decision 3: Real-time Progress Updates

**Handoff Recommendation:** WebSocket for progress (lines 1596-1608)
**Current Foldline:** API defined but not implemented
**Recommendation:** **Implement WebSocket** ✅

**Rationale:**
- GDPR imports can take 5-10 minutes
- Users need real-time feedback
- Better UX than polling

**Action:** Add WebSocket endpoint to FastAPI, integrate in frontend.

### Decision 4: Migration from gar-mining Databases

**Handoff Question:** "Should we support importing from gar-mining SQLite databases?"
**Current Foldline:** Not planned
**Recommendation:** **Add migration tool** (Phase 6)

**Rationale:**
- Some users may have years of gar-mining data
- One-time migration script is low effort
- Increases adoption for existing gar-mining users

**Action:**
```python
# New file: backend/migrations/from_gar_mining.py
def migrate_gar_mining_db(gar_mining_db_path, foldline_db):
    """
    Migrate data from gar-mining SQLite to Foldline DuckDB

    Tables to migrate:
    - activities → activities
    - sleep_data → sleep_records
    - daily_stats → daily_summaries
    - stress_data → daily_stress
    - heart_rate_daily → resting_hr
    """
```

---

## Testing Strategy

### Unit Tests (Port from Handoff)

**From handoff lines in TESTING_PLAN.md:**

1. **FIT Parsing Tests**
   - Test message type parsing
   - Test field extraction
   - Test error handling

2. **Analytics Tests**
   - Test correlation calculations
   - Test health score formula
   - Test recovery detection logic
   - Test with edge cases (missing data, outliers)

3. **Database Tests**
   - Test schema creation
   - Test deduplication
   - Test query performance

### Integration Tests

1. **End-to-End Import**
   - Import real GDPR export
   - Verify all tables populated
   - Check record counts

2. **End-to-End Analytics**
   - Import sample data
   - Call all analytics endpoints
   - Verify outputs match expected patterns

### Test Data

**Use from handoff project:**
- Sample FIT files
- Sample GDPR export (anonymized)
- Known good outputs from gar-mining

**Create for Foldline:**
- Synthetic data generator for edge cases
- Performance test data (large datasets)

---

## Migration Checklist

### From Handoff Doc → Foldline

- [ ] **Phase 1: Analytics Foundation**
  - [ ] Port Health Metrics Analyzer
  - [ ] Implement all metric queries (sleep, HRV, stress, steps)
  - [ ] Port Health Score algorithm
  - [ ] Port Recovery Detection algorithm
  - [ ] Implement Correlation Analysis endpoint

- [ ] **Phase 2: Visualization**
  - [ ] Install Plotly
  - [ ] Create TimeSeriesChart component
  - [ ] Create HeatmapChart component
  - [ ] Create CorrelationScatter component
  - [ ] Integrate into all UI pages

- [ ] **Phase 3: Complete GDPR Import**
  - [ ] Implement ZIP extraction
  - [ ] Implement GDPR-specific field mappings
  - [ ] Complete `process_gdpr_export()` pipeline
  - [ ] Test with real GDPR export

- [ ] **Phase 4: Schema Enhancements**
  - [ ] Add `raw_data` columns
  - [ ] Add source tracking to activities
  - [ ] Create `import_log` table
  - [ ] Create `heart_rate_timeseries` table
  - [ ] Write migration script

- [ ] **Phase 5: Advanced Analytics**
  - [ ] Port Stress Pattern Analysis
  - [ ] Port Sleep-Activity Correlation
  - [ ] Port Optimal Activity Range
  - [ ] Create dashboard endpoint

- [ ] **Phase 6: Future Features**
  - [ ] Annotations system
  - [ ] Flexible time windows
  - [ ] Relationship explorer
  - [ ] Predictive models
  - [ ] FIT directory watcher
  - [ ] Data export

---

## Conclusion

The Foldline codebase has **exceptional architecture** and **superior schema design** compared to gar-mining, but is missing the **battle-tested analytics algorithms** that make the data actionable.

**Top Priorities:**
1. ✅ Port all analytics algorithms (Phase 1)
2. ✅ Integrate Plotly visualizations (Phase 2)
3. ✅ Complete GDPR import (Phase 3)

**Once complete, Foldline will have:**
- ✅ Better architecture (Tauri desktop vs. Streamlit web)
- ✅ Better database (DuckDB vs. SQLite)
- ✅ Better schema (15 tables vs. 7)
- ✅ Better privacy (no API, local-only)
- ✅ **Same analytics power** (ported from gar-mining)
- ✅ Better UX (SvelteKit + dark mode vs. Streamlit)

This positions Foldline as the **next-generation** privacy-first wearable analytics platform, building on years of gar-mining learnings while fixing its architectural limitations.

---

**Next Steps:**
1. Review this integration plan
2. Prioritize phases based on user needs
3. Start with Phase 1 (Analytics Foundation)
4. Ship incrementally with each phase

**Questions? See:**
- FOLDLINE_HANDOFF.md (comprehensive knowledge transfer)
- This document (integration plan)
- Backend code (current implementation)
