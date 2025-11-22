# Foldline Project Handoff Documentation

**From:** gar-mining (Streamlit-based Garmin API analytics)
**To:** Foldline (Tauri + SvelteKit + FastAPI local-first wearable analyzer)
**Date:** 2025-11-22
**Purpose:** Complete knowledge transfer for migrating concepts, data models, and analytics logic

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Project Overview](#project-overview)
3. [Data Architecture](#data-architecture)
4. [Garmin API Integration](#garmin-api-integration)
5. [Analytics & Algorithms](#analytics--algorithms)
6. [Visualization Approaches](#visualization-approaches)
7. [Migration Guide](#migration-guide)
8. [Key Learnings & Design Decisions](#key-learnings--design-decisions)
9. [Code Examples](#code-examples)
10. [Future Opportunities](#future-opportunities)

---

## Executive Summary

**gar-mining** is a Streamlit-based personal analytics platform that syncs data from the Garmin Connect API and provides comprehensive health metrics analysis. Over ~4,900 lines of Python code, it implements:

- **Data Collection**: Activities, sleep, daily stats, stress, heart rate time series
- **Smart Sync**: Intelligent initial vs. incremental sync with 90-day health metrics limitation handling
- **Advanced Analytics**: Bidirectional sleep-activity correlation, multi-metric health scoring, recovery detection
- **Interactive Dashboards**: 5-page Streamlit app with Plotly visualizations

**Critical Value for Foldline:**
- ✅ Well-designed data models and database schemas
- ✅ Proven Garmin API integration patterns (with limitations documented)
- ✅ Sophisticated analytics algorithms (correlation analysis, health scoring, recovery detection)
- ✅ Clear understanding of what works and what doesn't in health data visualization

**Key Difference for Foldline:**
- gar-mining: Cloud API → SQLite → Streamlit (online, requires Garmin account)
- Foldline: GDPR exports + FIT files → DuckDB/SQLite → Tauri app (offline, privacy-first)

---

## Project Overview

### What gar-mining Does

1. **Authenticates** with Garmin Connect using OAuth (garth library)
2. **Syncs** fitness and health data via undocumented API endpoints
3. **Stores** data in local SQLite database with raw JSON backup
4. **Analyzes** relationships between sleep, stress, activity, and heart rate
5. **Visualizes** trends, correlations, and patterns through interactive dashboards

### Technology Stack

```
Frontend:     Streamlit (Python web framework)
Backend:      Python 3.9+
Database:     SQLite with manual schema management
API Client:   garth + garminconnect libraries
Analytics:    pandas, numpy, scipy
Visualization: Plotly (interactive charts)
```

### Project Statistics

- **Lines of Code**: ~4,900
- **Data Models**: 6 primary classes (Activity, SleepData, DailyStats, StressData, HeartRateData, SyncStatus)
- **Database Tables**: 7 (activities, sleep_data, daily_stats, stress_data, heart_rate_daily, heart_rate, sync_log)
- **API Endpoints**: 5 verified Garmin endpoints
- **Streamlit Pages**: 5 (Home, Activities, Analytics, Sleep, Health Metrics, Settings)
- **Test Coverage**: Basic test structure (not comprehensive)

---

## Data Architecture

### Data Models

All models use Python `@dataclass` with computed properties for unit conversions. **For Foldline**: Consider migrating to Pydantic models for FastAPI integration.

#### 1. Activity Model

**Purpose:** Represents a single workout/fitness activity

```python
@dataclass
class Activity:
    # Identifiers
    activity_id: int
    activity_name: Optional[str]
    activity_type: Optional[str]  # "running", "cycling", "swimming", etc.
    start_time: datetime

    # Duration & Distance
    duration_seconds: Optional[float]
    distance_meters: Optional[float]

    # Heart Rate
    average_hr: Optional[float]
    max_hr: Optional[float]

    # Performance
    calories: Optional[int]
    average_speed: Optional[float]  # m/s
    max_speed: Optional[float]

    # Elevation
    elevation_gain: Optional[float]  # meters
    elevation_loss: Optional[float]

    # Advanced Metrics
    avg_cadence: Optional[float]  # steps/min or rpm
    max_cadence: Optional[float]
    avg_power: Optional[float]  # watts
    max_power: Optional[float]
    training_effect: Optional[float]  # 0-5 scale

    # Computed Properties
    @property
    def duration_formatted(self) -> str:
        """Returns HH:MM:SS"""

    @property
    def distance_km(self) -> Optional[float]:
        """Meters to kilometers"""

    @property
    def pace_min_per_km(self) -> Optional[float]:
        """Calculated from average_speed"""
```

**Migration Notes:**
- FIT files contain more granular data (GPS tracks, per-second HR)
- Consider separate tables for activity summary vs. time-series data
- GDPR exports use different field names than API

#### 2. SleepData Model

**Purpose:** Nightly sleep summary with stage breakdown

```python
@dataclass
class SleepData:
    sleep_id: int
    calendar_date: str  # YYYY-MM-DD (date sleep ended)

    # Time Window
    sleep_start: Optional[datetime]
    sleep_end: Optional[datetime]

    # Stage Durations (seconds)
    total_sleep_seconds: Optional[int]
    deep_sleep_seconds: Optional[int]
    light_sleep_seconds: Optional[int]
    rem_sleep_seconds: Optional[int]
    awake_seconds: Optional[int]

    # Quality Metric
    sleep_score: Optional[float]  # 0-100 Garmin proprietary score

    # Computed Properties
    @property
    def sleep_efficiency(self) -> Optional[float]:
        """total_sleep / (total_sleep + awake) * 100"""

    @property
    def total_sleep_hours(self) -> Optional[float]:
        """Seconds to hours conversion"""
```

**Migration Notes:**
- GDPR exports may include more detailed sleep movement data
- FIT files have per-minute sleep stage timeline
- Consider storing sleep stage transitions for better visualization

#### 3. DailyStats Model

**Purpose:** Daily activity and wellness summary (non-exercise metrics)

```python
@dataclass
class DailyStats:
    calendar_date: str  # YYYY-MM-DD (Primary Key)

    # Activity
    steps: Optional[int]
    distance_meters: Optional[float]
    floors_climbed: Optional[int]

    # Calories
    active_calories: Optional[int]  # Exercise calories
    total_calories: Optional[int]   # BMR + active

    # Time Breakdown
    highly_active_seconds: Optional[int]  # Vigorous activity
    active_seconds: Optional[int]          # Moderate activity
    sedentary_seconds: Optional[int]

    # Heart Rate (daily aggregates)
    resting_hr: Optional[int]
    min_hr: Optional[int]
    max_hr: Optional[int]
```

**Migration Notes:**
- GDPR exports have this data but may use different field names
- Important for non-athletes (steps more relevant than formal activities)
- Useful for baseline health tracking

#### 4. StressData Model

**Purpose:** Daily stress level tracking (requires compatible Garmin device)

```python
@dataclass
class StressData:
    calendar_date: str  # YYYY-MM-DD

    # Aggregate Metrics
    average_stress_level: Optional[int]  # 0-100 scale
    max_stress_level: Optional[int]

    # Duration Breakdown
    stress_duration_seconds: Optional[int]    # Total stressed time
    rest_duration_seconds: Optional[int]       # Rest/recovery time
    activity_duration_seconds: Optional[int]   # Exercise time

    # Stress Level Categories
    low_stress_duration_seconds: Optional[int]     # 0-25
    medium_stress_duration_seconds: Optional[int]  # 26-50
    high_stress_duration_seconds: Optional[int]    # 51-100

    # Qualitative Assessment
    stress_qualifier: Optional[str]  # "calm", "balanced", "stressful", "very stressful"
```

**Migration Notes:**
- Not all Garmin devices support stress tracking
- Algorithm uses HRV + activity context
- Valuable for recovery and overtraining detection

#### 5. HeartRateData Model

**Purpose:** Daily heart rate time series + aggregates

```python
@dataclass
class HeartRateData:
    calendar_date: str  # YYYY-MM-DD

    # Daily Aggregates
    resting_hr: Optional[int]
    min_hr: Optional[int]
    max_hr: Optional[int]
    average_hr: Optional[float]

    # Time Series
    heart_rate_values: Optional[str]  # JSON: [{"timestamp": "...", "bpm": 72}, ...]

    # Computed Metrics
    @property
    def hr_range(self) -> Optional[int]:
        """max_hr - min_hr"""

    @property
    def hr_variability_indicator(self) -> Optional[float]:
        """Calculated from time series if available"""
```

**Migration Notes:**
- FIT files have much higher resolution (second-by-second during activities)
- GDPR exports may include full-day HR at 5-15 minute intervals
- Consider separate storage for activity HR vs. resting HR

#### 6. SyncStatus Model

**Purpose:** Track sync operations and progress

```python
@dataclass
class SyncStatus:
    sync_type: str  # "initial" or "incremental"
    is_running: bool
    current_operation: Optional[str]  # "Syncing activities (50/100)"

    # Counters
    activities_synced: int
    sleep_records_synced: int
    daily_stats_synced: int
    stress_records_synced: int
    heart_rate_records_synced: int

    # Errors
    error_message: Optional[str]

    # Timing
    start_time: Optional[datetime]
    end_time: Optional[datetime]

    @property
    def total_records_synced(self) -> int:
        """Sum of all counters"""
```

**Migration Notes:**
- Foldline needs similar progress tracking for FIT file parsing
- GDPR import will be one-time bulk operation
- Consider WebSocket for real-time progress updates

### Database Schema

**Technology:** SQLite with manual schema creation

**Design Patterns:**
- `INSERT OR REPLACE` semantics for idempotency
- Separate time-series tables (e.g., `heart_rate` per-activity samples)
- Raw JSON backup in `raw_data` columns
- Indexes on date/time fields for query performance
- No foreign keys (SQLite compatibility)

#### Table: activities

```sql
CREATE TABLE activities (
    activity_id INTEGER PRIMARY KEY,
    activity_name TEXT,
    activity_type TEXT,
    start_time TEXT NOT NULL,  -- ISO 8601 timestamp
    duration_seconds REAL,
    distance_meters REAL,
    average_hr REAL,
    max_hr REAL,
    calories INTEGER,
    average_speed REAL,
    max_speed REAL,
    elevation_gain REAL,
    elevation_loss REAL,
    avg_cadence REAL,
    max_cadence REAL,
    avg_power REAL,
    max_power REAL,
    training_effect REAL,
    raw_data TEXT,  -- JSON backup of full API response
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_activities_start_time ON activities(start_time);
CREATE INDEX idx_activities_type ON activities(activity_type);
```

**Migration Considerations:**
- Add `source` column ("api", "gdpr", "fit_file")
- Add `file_path` for linking back to original FIT file
- Consider PostgreSQL/DuckDB for better JSON support

#### Table: heart_rate (Activity-Level Time Series)

```sql
CREATE TABLE heart_rate (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    activity_id INTEGER NOT NULL,
    timestamp TEXT NOT NULL,  -- ISO 8601
    heart_rate INTEGER NOT NULL
);

CREATE INDEX idx_heart_rate_activity ON heart_rate(activity_id);
```

**Migration Considerations:**
- High volume table (thousands of rows per activity)
- DuckDB would be more efficient for time-series queries
- Consider columnar storage for analytics

#### Table: sleep_data

```sql
CREATE TABLE sleep_data (
    sleep_id INTEGER PRIMARY KEY,
    calendar_date TEXT NOT NULL UNIQUE,  -- YYYY-MM-DD
    sleep_start TEXT,
    sleep_end TEXT,
    total_sleep_seconds INTEGER,
    deep_sleep_seconds INTEGER,
    light_sleep_seconds INTEGER,
    rem_sleep_seconds INTEGER,
    awake_seconds INTEGER,
    sleep_score REAL,
    raw_data TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_sleep_date ON sleep_data(calendar_date);
```

#### Table: daily_stats

```sql
CREATE TABLE daily_stats (
    calendar_date TEXT PRIMARY KEY,  -- YYYY-MM-DD
    steps INTEGER,
    distance_meters REAL,
    active_calories INTEGER,
    total_calories INTEGER,
    floors_climbed INTEGER,
    highly_active_seconds INTEGER,
    active_seconds INTEGER,
    sedentary_seconds INTEGER,
    resting_hr INTEGER,
    min_hr INTEGER,
    max_hr INTEGER,
    raw_data TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### Table: stress_data

```sql
CREATE TABLE stress_data (
    calendar_date TEXT PRIMARY KEY,
    average_stress_level INTEGER,
    max_stress_level INTEGER,
    stress_duration_seconds INTEGER,
    rest_duration_seconds INTEGER,
    activity_duration_seconds INTEGER,
    low_stress_duration_seconds INTEGER,
    medium_stress_duration_seconds INTEGER,
    high_stress_duration_seconds INTEGER,
    stress_qualifier TEXT,
    raw_data TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_stress_date ON stress_data(calendar_date);
```

#### Table: heart_rate_daily

```sql
CREATE TABLE heart_rate_daily (
    calendar_date TEXT PRIMARY KEY,
    resting_hr INTEGER,
    min_hr INTEGER,
    max_hr INTEGER,
    average_hr REAL,
    heart_rate_values TEXT,  -- JSON array of {timestamp, bpm}
    raw_data TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### Table: sync_log

```sql
CREATE TABLE sync_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sync_type TEXT NOT NULL,  -- 'initial' or 'incremental'
    status TEXT NOT NULL,      -- 'success', 'error', 'partial'
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    activities_synced INTEGER DEFAULT 0,
    sleep_records_synced INTEGER DEFAULT 0,
    daily_stats_synced INTEGER DEFAULT 0,
    stress_records_synced INTEGER DEFAULT 0,
    heart_rate_records_synced INTEGER DEFAULT 0,
    error_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**For Foldline:**
- Rename to `import_log` (no "sync" since it's local-only)
- Add `source_type` ("gdpr_zip", "fit_directory", "manual_import")
- Add `file_count` for tracking bulk imports

---

## Garmin API Integration

### Authentication Flow

**Current Implementation (gar-mining):**

```python
# Uses garth library for OAuth
import garth

# Login with credentials
garth.login(email, password)

# Handle MFA if required
if garth.client.oauth2_token is None:
    # Prompt user for MFA code sent to email
    mfa_code = get_user_input()
    garth.login(email, password, mfa_code=mfa_code)

# Session cached in ~/.garth/ or data/.garth/
# Can resume session without re-login
garth.resume()
```

**For Foldline:**
- ❌ **Not applicable** - Foldline uses GDPR exports and FIT files, no API auth needed
- ✅ **Advantage**: No OAuth, no session management, no rate limits, truly offline

### Verified API Endpoints

**IMPORTANT**: These endpoints are **undocumented** and discovered via reverse engineering. Field names may change without notice.

#### 1. Activities List

```
GET /activitylist-service/activities/search/activities
```

**Parameters:**
- `start` (int): Pagination offset (0-based)
- `limit` (int): Results per page (max 100)

**Response:** Array of activity objects

**Rate Limit:** Unknown, but conservative pagination recommended

**Data Availability:** ✅ **Complete history** (no time limit)

**Field Name Variations:**
- `activityId` vs `activity_id`
- `activityType.typeKey` (nested) vs `activityType` (string)

**Sample Response:**
```json
{
  "activityId": 12345678,
  "activityName": "Morning Run",
  "activityType": {
    "typeKey": "running"
  },
  "startTimeLocal": "2025-11-22T07:30:00",
  "duration": 3600.0,
  "distance": 10000.0,
  "averageHR": 145.2,
  "maxHR": 172,
  "calories": 650
}
```

#### 2. Sleep Data

```
GET /wellness-service/wellness/dailySleepData/{username}
```

**Parameters:**
- `date` (YYYY-MM-DD): Date to retrieve
- `nonSleepBufferMinutes` (optional): Buffer around sleep window (default 60)

**Response:** Nested object with `dailySleepDTO`

**Data Availability:** ⚠️ **Last 90 days only**

**Critical Limitation:** Historical sleep data older than 90 days is **not accessible** via API. Users must have been syncing regularly or will lose data.

**Sample Response:**
```json
{
  "dailySleepDTO": {
    "id": 87654321,
    "sleepStartTimestampLocal": "2025-11-21T22:30:00",
    "sleepEndTimestampLocal": "2025-11-22T06:45:00",
    "sleepTimeSeconds": 28800,
    "deepSleepSeconds": 7200,
    "lightSleepSeconds": 18000,
    "remSleepSeconds": 3600,
    "awakeSleepSeconds": 1200,
    "sleepScores": {
      "overall": {
        "value": 78
      }
    }
  }
}
```

**Additional Fields Available:**
- `sleepMovement`: Movement intensity array
- `wellnessSpO2SleepSummaryDTO`: Blood oxygen during sleep
- `wellnessEpochRespirationDataDTOList`: Breathing rate time series
- `sleepStress`: Stress levels during sleep

#### 3. Daily Stats (User Summary)

```
GET /usersummary-service/usersummary/daily/{username}
```

**Parameters:**
- `calendarDate` (YYYY-MM-DD): Date to retrieve

**Data Availability:** ⚠️ **Last 90 days only**

**Field Name Variations:** API returns different field names across versions. Both must be handled:

| Canonical          | Alternative        |
|--------------------|--------------------|
| `steps`            | `totalSteps`       |
| `distanceMeters`   | `totalDistanceMeters` |
| `activeCalories`   | `activeKilocalories` |
| `totalCalories`    | `totalKilocalories` |
| `floorsClimbed`    | `floorsAscended`   |
| `restingHr`        | `restingHeartRate` |

**Parsing Strategy:**
```python
steps = stats.get("steps") or stats.get("totalSteps")
resting_hr = stats.get("restingHr") or stats.get("restingHeartRate")
```

#### 4. Stress Data

```
GET /usersummary-service/stats/stress/weekly/{date}/{weeks}
```

**Parameters:**
- `date` (YYYY-MM-DD): Start date
- `weeks` (int): Number of weeks to retrieve (use 1 for single day)

**Data Availability:** ⚠️ **Last 90 days only**

**Device Requirement:** Not all Garmin devices support stress tracking. Check for null response.

**Response:** Array in `stressValuesArray` or `values`

**Sample Response:**
```json
{
  "values": [
    {
      "calendarDate": "2025-11-22",
      "avgStressLevel": 45,
      "maxStressLevel": 78,
      "stressDuration": 14400,
      "restStressDuration": 28800,
      "lowStressDuration": 10800,
      "mediumStressDuration": 3600,
      "highStressDuration": 0,
      "stressQualifier": "BALANCED"
    }
  ]
}
```

#### 5. Heart Rate Time Series

```
GET /wellness-service/wellness/dailyHeartRate/{username}
```

**Parameters:**
- `date` (YYYY-MM-DD): Date to retrieve

**Data Availability:** ⚠️ **Last 90 days only**

**Sampling Rate:** 5-15 minute intervals (device-dependent)

**Sample Response:**
```json
{
  "heartRateValues": [
    {"timestamp": 1700640000000, "heartRate": 58},
    {"timestamp": 1700640900000, "heartRate": 62},
    {"timestamp": 1700641800000, "heartRate": 65}
  ],
  "restingHeartRate": 56
}
```

### Sync Strategy

**Initial Sync:**
1. Fetch **all activities** (paginated, 100 per request, unlimited history)
2. Fetch **90 days of health metrics** (sleep, stats, stress, HR)
   - ~180 API calls (90 days × 2 endpoints)
   - Sequential to avoid rate limiting

**Incremental Sync:**
1. Query database for last synced date per data type
2. Fetch only new data since last sync
3. Much lighter (typically 1-5 API calls per day)

**Error Handling:**
```python
# Per-item resilience
for date in date_range:
    try:
        data = fetch_sleep(date)
        database.insert(data)
    except APIError as e:
        log_error(date, e)
        continue  # Don't stop entire sync
```

**Rate Limiting:**
- No official limits documented
- Observed: ~200 requests/hour safe
- Recommendation: 1-2 second delay between requests for large syncs

### Migration to GDPR Exports

**For Foldline**, Garmin GDPR exports provide similar data but in bulk:

**GDPR Export Structure:**
```
garmin_export.zip
├── DI_CONNECT/
│   ├── DI-Connect-Fitness/
│   │   ├── <timestamp>_ACTIVITY.fit
│   │   └── ...
│   ├── DI-Connect-Wellness/
│   │   ├── <date>_SLEEP.json
│   │   ├── <date>_DAILYSUMMARY.json
│   │   └── ...
│   └── DI-Connect-User/
│       └── user_profile.json
```

**Advantages over API:**
- ✅ Complete historical data (no 90-day limit)
- ✅ Higher resolution (FIT files have second-by-second data)
- ✅ No authentication required
- ✅ No rate limits
- ✅ Privacy-first (data never leaves user's machine)

**Challenges:**
- ⚠️ One-time export (user must request from Garmin)
- ⚠️ Different schema than API (requires separate parsers)
- ⚠️ FIT file format requires specialized library (fitparse, garmin-fit-sdk)

---

## Analytics & Algorithms

### 1. Sleep-Activity Correlation Analysis

**Purpose:** Understand bidirectional relationship between sleep and activity

**Implementation:** `src/analysis.py` → `SleepActivityAnalyzer` class

**Algorithm:**

```python
def analyze_sleep_to_activity(self, date_range):
    """How does sleep quality affect next-day activity?"""

    # 1. Join sleep data with next-day activities
    df = pd.merge(
        sleep_df,
        activity_df,
        left_on=sleep_df['date'] + 1 day,
        right_on=activity_df['date']
    )

    # 2. Add lagged features
    df['prev_sleep_score'] = df['sleep_score'].shift(1)
    df['rolling_7d_sleep'] = df['sleep_score'].rolling(7).mean()

    # 3. Calculate correlations
    correlations = {
        'sleep_to_distance': pearsonr(df['sleep_score'], df['distance']),
        'sleep_to_duration': pearsonr(df['sleep_score'], df['duration']),
        'sleep_to_intensity': pearsonr(df['sleep_score'], df['avg_hr'])
    }

    # 4. Statistical significance testing
    for metric, (r, p_value) in correlations.items():
        if p_value < 0.05:
            print(f"Significant correlation: {metric} (r={r:.3f}, p={p_value:.4f})")

    return correlations
```

**Key Findings from Implementation:**
- Sleep score positively correlated with next-day activity distance (r=0.3-0.5 typical)
- Deep sleep % more predictive than total duration
- 7-day rolling average better than single-night for prediction

**For Foldline:**
- Preserve this algorithm (valuable insight)
- Add confidence intervals to visualizations
- Consider causality tests (Granger causality)

### 2. Health Metrics Analyzer

**Purpose:** Multi-metric health dashboard with comprehensive correlations

**Implementation:** `src/analysis.py` → `HealthMetricsAnalyzer` class

**Core Query:**
```python
def get_daily_health_metrics(self, start_date, end_date):
    """Join all health data sources"""

    query = """
    SELECT
        d.calendar_date,
        -- Daily Stats
        d.steps,
        d.active_calories,
        d.resting_hr,
        -- Sleep
        s.total_sleep_seconds,
        s.sleep_score,
        s.deep_sleep_seconds,
        -- Stress
        st.average_stress_level,
        st.stress_qualifier,
        -- Heart Rate
        hr.resting_hr as hr_daily,
        hr.heart_rate_values
    FROM daily_stats d
    LEFT JOIN sleep_data s ON d.calendar_date = s.calendar_date
    LEFT JOIN stress_data st ON d.calendar_date = st.calendar_date
    LEFT JOIN heart_rate_daily hr ON d.calendar_date = hr.calendar_date
    WHERE d.calendar_date BETWEEN ? AND ?
    ORDER BY d.calendar_date
    """

    return pd.read_sql(query, connection, params=[start_date, end_date])
```

**Derived Metrics:**
```python
def _add_derived_metrics(self, df):
    """Compute additional metrics from raw data"""

    # Sleep efficiency
    df['sleep_efficiency'] = (
        df['total_sleep_seconds'] /
        (df['total_sleep_seconds'] + df['awake_seconds']) * 100
    )

    # Heart rate range
    df['hr_range'] = df['max_hr'] - df['min_hr']

    # Stress-rest ratio
    df['stress_rest_ratio'] = (
        df['stress_duration_seconds'] /
        df['rest_duration_seconds']
    )

    # Deep sleep percentage
    df['deep_sleep_pct'] = (
        df['deep_sleep_seconds'] /
        df['total_sleep_seconds'] * 100
    )

    return df
```

**Correlation Matrix:**
```python
def calculate_correlations(self, df):
    """Full correlation matrix for all metrics"""

    metrics = [
        'steps', 'resting_hr', 'sleep_score',
        'stress_level', 'active_calories'
    ]

    corr_matrix = df[metrics].corr(method='pearson')

    # Identify strong correlations (|r| > 0.5)
    strong_correlations = []
    for i in range(len(metrics)):
        for j in range(i+1, len(metrics)):
            r = corr_matrix.iloc[i, j]
            if abs(r) > 0.5:
                strong_correlations.append({
                    'metric1': metrics[i],
                    'metric2': metrics[j],
                    'correlation': r
                })

    return corr_matrix, strong_correlations
```

### 3. Recovery Day Detection

**Purpose:** Identify days when body is in recovery mode (need rest)

**Algorithm:**
```python
def identify_recovery_days(self, df, threshold=60):
    """
    Composite recovery score based on multiple signals:
    - Elevated resting HR (+10% over baseline)
    - Poor sleep score (<70)
    - High stress (>60)
    - Low HRV (if available)
    """

    # Calculate baselines (30-day rolling average)
    df['baseline_resting_hr'] = df['resting_hr'].rolling(30, min_periods=14).mean()
    df['baseline_sleep'] = df['sleep_score'].rolling(30, min_periods=14).mean()

    # Recovery signals (0-100, lower = more recovery needed)
    df['hr_recovery_score'] = 100 - (
        (df['resting_hr'] - df['baseline_resting_hr']) /
        df['baseline_resting_hr'] * 100
    ).clip(0, 100)

    df['sleep_recovery_score'] = df['sleep_score']

    df['stress_recovery_score'] = 100 - df['average_stress_level']

    # Composite score (weighted average)
    df['recovery_score'] = (
        df['hr_recovery_score'] * 0.4 +
        df['sleep_recovery_score'] * 0.3 +
        df['stress_recovery_score'] * 0.3
    )

    # Flag recovery days
    df['needs_recovery'] = df['recovery_score'] < threshold

    return df
```

**Use Cases:**
- Training load management
- Injury prevention
- Optimize workout timing

### 4. Health Score Generation

**Purpose:** Single composite score (0-100) for overall health

**Algorithm:**
```python
def generate_health_score(self, df):
    """
    Multi-component wellness scoring:
    - Sleep: 30%
    - Activity: 25%
    - Stress: 25%
    - Heart Rate: 20%
    """

    # Normalize each component to 0-100
    sleep_score = df['sleep_score']  # Already 0-100

    # Activity: Steps vs. 10k goal
    activity_score = (df['steps'] / 10000 * 100).clip(0, 100)

    # Stress: Invert (lower is better)
    stress_score = 100 - df['average_stress_level']

    # Heart Rate: Based on deviation from baseline
    hr_score = 100 - abs(
        (df['resting_hr'] - df['baseline_resting_hr']) /
        df['baseline_resting_hr'] * 100
    ).clip(0, 100)

    # Weighted composite
    df['health_score'] = (
        sleep_score * 0.30 +
        activity_score * 0.25 +
        stress_score * 0.25 +
        hr_score * 0.20
    )

    return df
```

**For Foldline:**
- Make weights user-configurable
- Add more components (HRV, body battery, weight)
- Provide explanations for score changes

### 5. Stress Pattern Analysis

**Purpose:** Understand stress distribution and trends

**Implementation:**

```python
def analyze_stress_patterns(self, df):
    """Comprehensive stress analysis"""

    # Distribution
    stress_distribution = {
        'calm': len(df[df['stress_qualifier'] == 'calm']),
        'balanced': len(df[df['stress_qualifier'] == 'balanced']),
        'stressful': len(df[df['stress_qualifier'] == 'stressful']),
        'very_stressful': len(df[df['stress_qualifier'] == 'very_stressful'])
    }

    # Day of week patterns
    df['day_of_week'] = pd.to_datetime(df['calendar_date']).dt.day_name()
    stress_by_dow = df.groupby('day_of_week')['average_stress_level'].agg([
        'mean', 'median', 'std'
    ])

    # Chronic stress detection (7+ consecutive days >55)
    df['high_stress'] = df['average_stress_level'] > 55
    df['stress_streak'] = df['high_stress'].rolling(7).sum()
    chronic_stress_periods = df[df['stress_streak'] >= 7]

    # Correlation with other metrics
    stress_correlations = {
        'sleep': df[['average_stress_level', 'sleep_score']].corr().iloc[0,1],
        'steps': df[['average_stress_level', 'steps']].corr().iloc[0,1],
        'resting_hr': df[['average_stress_level', 'resting_hr']].corr().iloc[0,1]
    }

    return {
        'distribution': stress_distribution,
        'day_of_week': stress_by_dow,
        'chronic_periods': chronic_stress_periods,
        'correlations': stress_correlations
    }
```

### 6. Optimal Activity Range Analysis

**Purpose:** Find "sweet spot" for activity level (not too little, not too much)

**Algorithm:**

```python
def get_optimal_activity_range(self, df, metric='steps'):
    """
    Quartile analysis to find optimal activity level
    based on next-day recovery metrics
    """

    # Add next-day metrics
    df['next_day_sleep_score'] = df['sleep_score'].shift(-1)
    df['next_day_resting_hr'] = df['resting_hr'].shift(-1)
    df['next_day_stress'] = df['average_stress_level'].shift(-1)

    # Quartile-based grouping
    df['activity_quartile'] = pd.qcut(
        df[metric],
        q=4,
        labels=['Low', 'Medium', 'High', 'Very High']
    )

    # Analyze recovery by quartile
    recovery_by_quartile = df.groupby('activity_quartile').agg({
        'next_day_sleep_score': 'mean',
        'next_day_resting_hr': 'mean',
        'next_day_stress': 'mean'
    })

    # Find optimal (best next-day metrics)
    optimal_quartile = recovery_by_quartile['next_day_sleep_score'].idxmax()

    # Get range for optimal quartile
    optimal_range = df[df['activity_quartile'] == optimal_quartile][metric].agg([
        'min', 'max', 'mean'
    ])

    return {
        'optimal_quartile': optimal_quartile,
        'range': optimal_range,
        'by_quartile': recovery_by_quartile
    }
```

**Example Output:**
```
Optimal activity range: 8000-12000 steps
- Next-day sleep score: 82 (best)
- Next-day resting HR: 58 (lowest)
- Next-day stress: 38 (lowest)

Too low (<5000 steps):
- Sleep score: 75
- Resting HR: 60
- Stress: 45

Too high (>15000 steps):
- Sleep score: 72
- Resting HR: 62
- Stress: 52
```

---

## Visualization Approaches

### Technology: Plotly

**Why Plotly:**
- ✅ Interactive (zoom, pan, hover tooltips)
- ✅ Works in both Streamlit and SvelteKit (plotly.js)
- ✅ High-quality charts out of the box
- ✅ Supports complex layouts (subplots, dual axes)

**For Foldline:** Continue using Plotly (no migration needed)

### Visualization Patterns

#### 1. Time Series with Multiple Metrics

**Use Case:** Show stress, HR, and steps on same timeline

**Implementation:**
```python
from plotly.subplots import make_subplots
import plotly.graph_objects as go

fig = make_subplots(
    rows=3, cols=1,
    shared_xaxes=True,
    subplot_titles=("Stress Level", "Resting HR", "Daily Steps")
)

# Stress
fig.add_trace(
    go.Scatter(
        x=df['date'],
        y=df['average_stress_level'],
        name='Stress',
        line=dict(color='red')
    ),
    row=1, col=1
)

# 7-day rolling average
fig.add_trace(
    go.Scatter(
        x=df['date'],
        y=df['stress_7d_avg'],
        name='7-day avg',
        line=dict(color='red', dash='dash')
    ),
    row=1, col=1
)

# Resting HR
fig.add_trace(
    go.Scatter(
        x=df['date'],
        y=df['resting_hr'],
        name='Resting HR',
        line=dict(color='blue')
    ),
    row=2, col=1
)

# Steps with goal line
fig.add_trace(
    go.Scatter(
        x=df['date'],
        y=df['steps'],
        name='Steps',
        fill='tozeroy',
        line=dict(color='green')
    ),
    row=3, col=1
)

fig.add_hline(y=10000, line_dash="dot", row=3, col=1, annotation_text="Goal")

fig.update_layout(height=800, showlegend=False)
```

#### 2. Calendar Heatmap (Sleep Duration)

**Use Case:** Visualize daily sleep in calendar format

**Implementation:**
```python
import plotly.express as px

# Prepare data
df['year'] = pd.to_datetime(df['date']).dt.year
df['week'] = pd.to_datetime(df['date']).dt.isocalendar().week
df['day_of_week'] = pd.to_datetime(df['date']).dt.dayofweek

fig = px.density_heatmap(
    df,
    x='week',
    y='day_of_week',
    z='total_sleep_hours',
    facet_col='year',
    color_continuous_scale='Blues',
    labels={'week': 'Week of Year', 'day_of_week': 'Day', 'z': 'Hours'}
)

fig.update_yaxes(
    ticktext=['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
    tickvals=list(range(7))
)
```

#### 3. Correlation Heatmap

**Use Case:** Show relationships between all metrics

**Implementation:**
```python
import plotly.graph_objects as go

# Calculate correlation matrix
corr_matrix = df[metrics].corr()

fig = go.Figure(data=go.Heatmap(
    z=corr_matrix.values,
    x=corr_matrix.columns,
    y=corr_matrix.columns,
    colorscale='RdBu',
    zmid=0,
    text=corr_matrix.values.round(2),
    texttemplate='%{text}',
    textfont={"size": 10},
    colorbar=dict(title="Correlation")
))

fig.update_layout(
    title="Metric Correlations",
    width=600,
    height=600
)
```

#### 4. Sleep Quality Zones

**Use Case:** Visualize sleep score with quality bands

**Implementation:**
```python
import plotly.graph_objects as go

fig = go.Figure()

# Sleep score line
fig.add_trace(go.Scatter(
    x=df['date'],
    y=df['sleep_score'],
    mode='lines+markers',
    name='Sleep Score',
    line=dict(color='purple', width=2)
))

# Quality zones (background)
fig.add_hrect(
    y0=80, y1=100,
    fillcolor="green", opacity=0.1,
    annotation_text="Excellent", annotation_position="top left"
)
fig.add_hrect(
    y0=60, y1=80,
    fillcolor="yellow", opacity=0.1,
    annotation_text="Good"
)
fig.add_hrect(
    y0=0, y1=60,
    fillcolor="red", opacity=0.1,
    annotation_text="Poor"
)

fig.update_layout(
    title="Sleep Quality Trends",
    yaxis_title="Sleep Score",
    yaxis_range=[0, 100]
)
```

#### 5. Distribution Pie Chart (Stress Levels)

**Use Case:** Show proportion of days in each stress category

**Implementation:**
```python
import plotly.express as px

stress_dist = df['stress_qualifier'].value_counts()

fig = px.pie(
    values=stress_dist.values,
    names=stress_dist.index,
    title='Stress Distribution',
    color=stress_dist.index,
    color_discrete_map={
        'calm': '#2ecc71',
        'balanced': '#3498db',
        'stressful': '#f39c12',
        'very stressful': '#e74c3c'
    }
)
```

#### 6. Scatter with Trend Line (Sleep vs. Activity)

**Use Case:** Explore correlation between two metrics

**Implementation:**
```python
import plotly.express as px
from scipy.stats import linregress

# Calculate trend line
slope, intercept, r_value, p_value, std_err = linregress(
    df['sleep_score'],
    df['next_day_distance']
)

fig = px.scatter(
    df,
    x='sleep_score',
    y='next_day_distance',
    color='activity_type',
    size='duration',
    hover_data=['date'],
    title=f'Sleep Quality vs. Next-Day Activity (r={r_value:.2f}, p={p_value:.4f})'
)

# Add trend line
fig.add_trace(go.Scatter(
    x=df['sleep_score'],
    y=slope * df['sleep_score'] + intercept,
    mode='lines',
    name='Trend',
    line=dict(color='black', dash='dash')
))
```

### Dashboard Layout Patterns

**Streamlit Pattern:**
```python
import streamlit as st

# Metrics row
col1, col2, col3, col4 = st.columns(4)
col1.metric("Avg Sleep", "7.2 hrs", delta="+ 0.3")
col2.metric("Avg Stress", "42", delta="- 5")
col3.metric("Avg Steps", "9,500", delta="+ 1,200")
col4.metric("Health Score", "78", delta="+ 4")

# Main chart
st.plotly_chart(time_series_fig, use_container_width=True)

# Side-by-side analysis
col_left, col_right = st.columns(2)
with col_left:
    st.plotly_chart(correlation_heatmap)
with col_right:
    st.plotly_chart(stress_distribution_pie)

# Expandable details
with st.expander("See detailed breakdown"):
    st.dataframe(df)
```

**For Foldline (SvelteKit equivalent):**
```svelte
<!-- components/HealthDashboard.svelte -->
<div class="metrics-grid">
  <MetricCard title="Avg Sleep" value="7.2 hrs" delta="+0.3" />
  <MetricCard title="Avg Stress" value="42" delta="-5" />
  <MetricCard title="Avg Steps" value="9,500" delta="+1,200" />
  <MetricCard title="Health Score" value="78" delta="+4" />
</div>

<div class="chart-container">
  <Plotly data={timeSeriesData} layout={timeSeriesLayout} />
</div>

<div class="two-column">
  <Plotly data={correlationData} />
  <Plotly data={distributionData} />
</div>
```

---

## Migration Guide

### From gar-mining (Streamlit + Garmin API) to Foldline (Tauri + FIT files)

#### 1. Data Ingestion Layer

**Current (gar-mining):**
```
garth.login() → Garmin API → JSON responses → SQLite
```

**Foldline Target:**
```
User selects GDPR zip → Extract → Parse FIT/JSON → DuckDB/SQLite
```

**Migration Tasks:**

**A. FIT File Parsing**

Replace `src/garmin_client.py` with FIT parser:

```python
# New: src/fit_parser.py
from fitparse import FitFile
from datetime import datetime

class FitFileParser:
    """Parse Garmin FIT files from GDPR export or local directory"""

    def parse_activity(self, fit_path: str) -> Activity:
        """Extract activity summary from FIT file"""
        fitfile = FitFile(fit_path)

        # Get session summary (aggregate metrics)
        session = fitfile.get_messages('session')[0]

        activity = Activity(
            activity_id=self._generate_id(fit_path),
            activity_name=session.get_value('sport'),
            activity_type=session.get_value('sport'),
            start_time=session.get_value('start_time'),
            duration_seconds=session.get_value('total_elapsed_time'),
            distance_meters=session.get_value('total_distance'),
            average_hr=session.get_value('avg_heart_rate'),
            max_hr=session.get_value('max_heart_rate'),
            calories=session.get_value('total_calories'),
            # ... map other fields
        )

        return activity

    def parse_activity_timeseries(self, fit_path: str) -> List[Dict]:
        """Extract second-by-second data (GPS, HR, power, etc.)"""
        fitfile = FitFile(fit_path)

        records = []
        for record in fitfile.get_messages('record'):
            records.append({
                'timestamp': record.get_value('timestamp'),
                'latitude': record.get_value('position_lat'),
                'longitude': record.get_value('position_long'),
                'heart_rate': record.get_value('heart_rate'),
                'altitude': record.get_value('altitude'),
                'speed': record.get_value('speed'),
                'cadence': record.get_value('cadence'),
                'power': record.get_value('power')
            })

        return records
```

**B. GDPR Export Handling**

```python
# New: src/gdpr_importer.py
import zipfile
import json
from pathlib import Path

class GDPRImporter:
    """Import complete GDPR export from Garmin"""

    def __init__(self, zip_path: str, db: Database):
        self.zip_path = zip_path
        self.db = db

    def import_all(self, progress_callback=None):
        """
        Extract and import all data from GDPR zip

        Structure:
        - DI_CONNECT/DI-Connect-Fitness/*.fit (activities)
        - DI_CONNECT/DI-Connect-Wellness/*SLEEP.json
        - DI_CONNECT/DI-Connect-Wellness/*DAILYSUMMARY.json
        """

        with zipfile.ZipFile(self.zip_path, 'r') as zf:
            # Count files for progress
            fit_files = [f for f in zf.namelist() if f.endswith('.fit')]
            sleep_files = [f for f in zf.namelist() if 'SLEEP' in f]

            total = len(fit_files) + len(sleep_files)

            # Import activities
            for i, fit_file in enumerate(fit_files):
                with zf.open(fit_file) as f:
                    activity = self.fit_parser.parse_activity(f)
                    self.db.insert_activity(activity)

                if progress_callback:
                    progress_callback(f"Importing activities", i, len(fit_files))

            # Import sleep data
            for i, sleep_file in enumerate(sleep_files):
                with zf.open(sleep_file) as f:
                    sleep_data = json.load(f)
                    parsed = self._parse_gdpr_sleep(sleep_data)
                    self.db.insert_sleep_data(parsed)

                if progress_callback:
                    progress_callback(f"Importing sleep", i, len(sleep_files))

    def _parse_gdpr_sleep(self, sleep_json: dict) -> SleepData:
        """
        Parse GDPR sleep JSON (different schema than API)

        GDPR uses different field names:
        - "sleepStartTimestampGMT" instead of "sleepStartTimestampLocal"
        - "totalSleepTime" instead of "sleepTimeSeconds"
        """
        # Map GDPR fields to standard model
        return SleepData(
            sleep_id=sleep_json['id'],
            calendar_date=sleep_json['calendarDate'],
            total_sleep_seconds=sleep_json.get('totalSleepTime', 0) * 60,  # minutes to seconds
            # ... map other fields
        )
```

**C. Local FIT File Monitoring**

```python
# New: src/fit_watcher.py
import os
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class FitFileWatcher(FileSystemEventHandler):
    """Monitor directory for new FIT files (e.g., ~/Garmin/)"""

    def __init__(self, watch_dir: str, db: Database, parser: FitFileParser):
        self.watch_dir = watch_dir
        self.db = db
        self.parser = parser

    def on_created(self, event):
        """Auto-import when new FIT file appears"""
        if event.src_path.endswith('.fit'):
            try:
                activity = self.parser.parse_activity(event.src_path)
                self.db.insert_activity(activity)
                print(f"Auto-imported: {activity.activity_name}")
            except Exception as e:
                print(f"Failed to import {event.src_path}: {e}")

    def start(self):
        """Start monitoring directory"""
        observer = Observer()
        observer.schedule(self, self.watch_dir, recursive=False)
        observer.start()
        return observer
```

#### 2. Backend API Layer (FastAPI)

**Create:** `backend/main.py`

```python
from fastapi import FastAPI, BackgroundTasks, UploadFile
from fastapi.responses import StreamingResponse
from typing import List, Optional
import asyncio

app = FastAPI(title="Foldline API")

# Progress tracking
import_progress = {"status": "idle", "current": 0, "total": 0}

@app.post("/import/gdpr")
async def import_gdpr_export(
    file: UploadFile,
    background_tasks: BackgroundTasks
):
    """
    Import GDPR export zip file
    Returns immediately, runs import in background
    """
    # Save uploaded zip
    zip_path = f"/tmp/{file.filename}"
    with open(zip_path, 'wb') as f:
        f.write(await file.read())

    # Start background import
    background_tasks.add_task(run_gdpr_import, zip_path)

    return {"status": "started", "message": "Import started in background"}

@app.get("/import/progress")
async def get_import_progress():
    """Poll import progress"""
    return import_progress

@app.websocket("/import/progress/ws")
async def import_progress_websocket(websocket: WebSocket):
    """Real-time progress updates via WebSocket"""
    await websocket.accept()

    while import_progress['status'] == 'running':
        await websocket.send_json(import_progress)
        await asyncio.sleep(0.5)

    await websocket.send_json(import_progress)
    await websocket.close()

@app.get("/metrics/health")
async def get_health_metrics(
    start_date: str,
    end_date: str,
    metrics: Optional[List[str]] = None
):
    """
    Get health metrics for date range

    Parameters:
    - start_date: YYYY-MM-DD
    - end_date: YYYY-MM-DD
    - metrics: ["sleep", "stress", "hr", "steps"] or None for all
    """
    analyzer = HealthMetricsAnalyzer(db)
    data = analyzer.get_daily_health_metrics(start_date, end_date)

    if metrics:
        # Filter to requested metrics
        data = data[['calendar_date'] + metrics]

    return data.to_dict(orient='records')

@app.get("/analytics/correlations")
async def get_correlations(start_date: str, end_date: str):
    """Get correlation matrix for date range"""
    analyzer = HealthMetricsAnalyzer(db)
    df = analyzer.get_daily_health_metrics(start_date, end_date)
    corr_matrix, strong_corr = analyzer.calculate_correlations(df)

    return {
        "matrix": corr_matrix.to_dict(),
        "strong_correlations": strong_corr
    }

@app.get("/activities")
async def get_activities(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    activity_type: Optional[str] = None,
    limit: int = 100,
    offset: int = 0
):
    """Query activities with filters"""
    # Build SQL query dynamically
    # ... implementation
    pass

@app.get("/export/csv/{data_type}")
async def export_csv(data_type: str, start_date: str, end_date: str):
    """
    Export data as CSV

    data_type: "activities", "sleep", "daily_stats", etc.
    """
    df = db.get_data(data_type, start_date, end_date)

    # Stream CSV response
    def generate_csv():
        yield df.to_csv(index=False)

    return StreamingResponse(
        generate_csv(),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={data_type}.csv"}
    )

async def run_gdpr_import(zip_path: str):
    """Background task for GDPR import"""
    global import_progress

    import_progress['status'] = 'running'

    def progress_callback(operation, current, total):
        import_progress.update({
            'operation': operation,
            'current': current,
            'total': total
        })

    try:
        importer = GDPRImporter(zip_path, db)
        importer.import_all(progress_callback)

        import_progress['status'] = 'complete'
    except Exception as e:
        import_progress['status'] = 'error'
        import_progress['error'] = str(e)
```

#### 3. Frontend (SvelteKit)

**Create:** `frontend/src/routes/dashboard/+page.svelte`

```svelte
<script lang="ts">
  import { onMount } from 'svelte';
  import Plotly from 'plotly.js-dist';

  let healthData = [];
  let correlationMatrix = null;
  let dateRange = {
    start: '2024-01-01',
    end: '2024-12-31'
  };

  async function fetchHealthMetrics() {
    const response = await fetch(
      `/api/metrics/health?start_date=${dateRange.start}&end_date=${dateRange.end}`
    );
    healthData = await response.json();
    renderCharts();
  }

  async function fetchCorrelations() {
    const response = await fetch(
      `/api/analytics/correlations?start_date=${dateRange.start}&end_date=${dateRange.end}`
    );
    const data = await response.json();
    correlationMatrix = data.matrix;
    renderCorrelationHeatmap();
  }

  function renderCharts() {
    // Time series chart (same as Streamlit version, but using plotly.js)
    const trace1 = {
      x: healthData.map(d => d.calendar_date),
      y: healthData.map(d => d.average_stress_level),
      type: 'scatter',
      name: 'Stress'
    };

    const layout = {
      title: 'Health Metrics Over Time',
      xaxis: { title: 'Date' },
      yaxis: { title: 'Stress Level' }
    };

    Plotly.newPlot('chart-container', [trace1], layout);
  }

  onMount(() => {
    fetchHealthMetrics();
    fetchCorrelations();
  });
</script>

<div class="dashboard">
  <div class="controls">
    <input type="date" bind:value={dateRange.start} />
    <input type="date" bind:value={dateRange.end} />
    <button on:click={fetchHealthMetrics}>Update</button>
  </div>

  <div id="chart-container"></div>
  <div id="correlation-heatmap"></div>
</div>
```

**Create:** `frontend/src/routes/import/+page.svelte`

```svelte
<script lang="ts">
  let importProgress = { status: 'idle', current: 0, total: 0 };
  let ws: WebSocket | null = null;

  async function handleFileUpload(event) {
    const file = event.target.files[0];
    const formData = new FormData();
    formData.append('file', file);

    // Start import
    await fetch('/api/import/gdpr', {
      method: 'POST',
      body: formData
    });

    // Connect to WebSocket for progress
    ws = new WebSocket('ws://localhost:8000/import/progress/ws');
    ws.onmessage = (event) => {
      importProgress = JSON.parse(event.data);
    };
  }
</script>

<div class="import-page">
  <h1>Import GDPR Export</h1>

  <input
    type="file"
    accept=".zip"
    on:change={handleFileUpload}
  />

  {#if importProgress.status === 'running'}
    <div class="progress-bar">
      <div class="progress-fill" style="width: {(importProgress.current / importProgress.total) * 100}%"></div>
    </div>
    <p>{importProgress.operation}: {importProgress.current} / {importProgress.total}</p>
  {/if}

  {#if importProgress.status === 'complete'}
    <p class="success">Import complete!</p>
  {/if}
</div>
```

#### 4. Tauri Integration

**Create:** `src-tauri/src/main.rs`

```rust
use tauri::Manager;
use std::process::{Command, Stdio};

#[tauri::command]
fn start_backend() -> Result<String, String> {
    // Start Python FastAPI backend on localhost:8000
    Command::new("python")
        .arg("backend/main.py")
        .stdout(Stdio::null())
        .spawn()
        .map_err(|e| e.to_string())?;

    Ok("Backend started".to_string())
}

#[tauri::command]
fn select_gdpr_export() -> Result<String, String> {
    // Native file picker for GDPR zip
    use tauri::api::dialog::blocking::FileDialogBuilder;

    let file_path = FileDialogBuilder::new()
        .add_filter("ZIP files", &["zip"])
        .pick_file();

    match file_path {
        Some(path) => Ok(path.to_string_lossy().to_string()),
        None => Err("No file selected".to_string())
    }
}

#[tauri::command]
fn select_fit_directory() -> Result<String, String> {
    // Select directory to monitor for FIT files
    use tauri::api::dialog::blocking::FileDialogBuilder;

    let dir_path = FileDialogBuilder::new().pick_folder();

    match dir_path {
        Some(path) => Ok(path.to_string_lossy().to_string()),
        None => Err("No directory selected".to_string())
    }
}

fn main() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![
            start_backend,
            select_gdpr_export,
            select_fit_directory
        ])
        .setup(|app| {
            // Auto-start Python backend when app launches
            tauri::async_runtime::spawn(async move {
                // Start backend server
            });
            Ok(())
        })
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
```

#### 5. Database Migration

**Current (gar-mining):** SQLite with manual schema

**Foldline Option A:** Keep SQLite, add migrations

```python
# backend/db/migrations/001_initial_schema.py
def upgrade(conn):
    """Create initial tables"""
    conn.executescript("""
        CREATE TABLE activities (...);
        CREATE TABLE sleep_data (...);
        -- ... same schema as gar-mining
    """)

def downgrade(conn):
    """Rollback"""
    conn.executescript("""
        DROP TABLE activities;
        DROP TABLE sleep_data;
    """)
```

**Foldline Option B:** Migrate to DuckDB (recommended)

Benefits:
- ✅ Better analytics performance (columnar storage)
- ✅ Native JSON support
- ✅ Window functions for time-series
- ✅ Parquet export for data portability

```python
# backend/db/connection.py
import duckdb

def get_connection():
    conn = duckdb.connect('foldline.duckdb')

    # Enable JSON extension
    conn.execute("INSTALL json; LOAD json;")

    return conn

# Example analytical query (much faster in DuckDB)
conn.execute("""
    SELECT
        calendar_date,
        AVG(resting_hr) OVER (
            ORDER BY calendar_date
            ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
        ) as hr_7d_avg
    FROM daily_stats
    ORDER BY calendar_date
""")
```

---

## Key Learnings & Design Decisions

### 1. API Limitations Are Critical

**Learning:** Garmin's 90-day limitation on health metrics is a **major** constraint

**Impact on gar-mining:**
- Users who don't sync regularly lose historical data forever
- Initial sync cannot capture full history
- Workaround: Frequent incremental syncs (daily is ideal)

**Foldline Advantage:**
- ✅ GDPR exports have complete history
- ✅ No risk of data loss
- ✅ No dependency on regular syncing

### 2. Field Name Variations Are Everywhere

**Learning:** Garmin API responses use inconsistent field names across endpoints and versions

**Examples:**
- `steps` vs. `totalSteps`
- `restingHr` vs. `restingHeartRate`
- `sleepTimeSeconds` vs. `totalSleepTime`

**Solution Pattern:**
```python
# Always check multiple field name variants
steps = data.get("steps") or data.get("totalSteps") or 0
```

**For Foldline:**
- GDPR exports have yet another schema
- FIT files have standardized field IDs (more consistent)
- Create mapping layer for all data sources

### 3. Raw Data Backup Is Essential

**Learning:** Store complete API responses as JSON backup

**Why:**
```sql
ALTER TABLE activities ADD COLUMN raw_data TEXT;
```

**Benefits:**
- ✅ Can extract new fields later without re-syncing
- ✅ Debugging API changes
- ✅ Data archaeology (find undocumented fields)

**Real Example:**
- Initially didn't capture `training_effect`
- Found it in `raw_data` JSON 6 months later
- Re-parsed without re-syncing

### 4. Incremental Sync Is Non-Negotiable

**Learning:** Full re-sync is expensive and slow

**Initial Sync Cost:**
- Activities: 10-50 API calls (depending on history)
- Health metrics: ~180 API calls (90 days × 2 endpoints)
- Time: 5-10 minutes

**Incremental Sync:**
- 1-5 API calls per day
- Time: 10-30 seconds

**Implementation:**
```python
last_activity_date = db.get_last_activity_date()
last_sleep_date = db.get_last_sleep_date()

# Only fetch new data
activities = fetch_activities_since(last_activity_date)
sleep_data = fetch_sleep_since(last_sleep_date)
```

**For Foldline:**
- Similar pattern for FIT file monitoring
- Track last imported file by timestamp
- Only process new files

### 5. MFA Handling Requires User Interaction

**Learning:** Can't fully automate login with 2FA enabled

**Current Approach:**
```python
# Streamlit callback for MFA code
def get_mfa_code():
    return st.text_input("Enter email verification code:")

sync_manager.sync(mfa_callback=get_mfa_code)
```

**For Foldline:**
- Not applicable (no authentication)
- Local-only = better UX

### 6. Error Resilience Is Critical

**Learning:** Individual data points failing shouldn't stop entire sync

**Bad Pattern:**
```python
# This fails entire sync if one day is missing
for date in date_range:
    data = fetch_sleep(date)  # Raises exception
    db.insert(data)
```

**Good Pattern:**
```python
# Continue sync even if individual days fail
for date in date_range:
    try:
        data = fetch_sleep(date)
        db.insert(data)
    except APIError as e:
        log_error(f"Failed to fetch {date}: {e}")
        continue  # Keep going
```

**Result:**
- 95% sync success rate vs. 0% (all-or-nothing)

### 7. Correlation Without Causation

**Learning:** Strong correlations don't mean causation

**Example Finding:**
```
Sleep score vs. next-day distance: r=0.42, p<0.01
```

**Possible Interpretations:**
1. Good sleep → enables longer runs ✅ (likely)
2. Planning long run → sleep better before ✅ (also likely)
3. Third factor (e.g., stress) affects both ✅ (confounding)

**UI Guidance:**
- Use neutral language: "associated with" not "causes"
- Show bidirectional analysis
- Acknowledge confounders

### 8. User Context Matters

**Learning:** Same metric means different things for different people

**Example: Steps**
- Office worker: 10k steps = very active day
- Warehouse worker: 10k steps = slow day
- Marathon runner: 10k steps = recovery day

**Solution:**
- Personal baselines (30-day rolling average)
- Percentile-based insights ("top 10% for you")
- User-configurable goals

### 9. Date Handling Is Tricky

**Learning:** Sleep data attribution is ambiguous

**Question:** If you sleep 11pm Nov 21 → 7am Nov 22, which date?

**Garmin's Choice:** Date sleep **ended** (Nov 22)
**Alternative:** Date sleep **started** (Nov 21)

**Impact on Analysis:**
```python
# When correlating sleep → next-day activity
# Must offset by 1 day if using "end date" attribution
df['next_day_distance'] = df['distance'].shift(-1)
```

**For Foldline:**
- Document attribution clearly
- Make it configurable if possible
- Validate correlation direction

### 10. Visualization Performance Matters

**Learning:** Plotly gets slow with >10k points

**Solutions:**
- Downsample for display (every Nth point)
- Aggregate to higher granularity (hourly → daily)
- Use WebGL mode: `fig.update_traces(mode='lines', line={'width': 1}, hoverinfo='skip')`

**Example:**
```python
# For 1-year view, show daily aggregates
if date_range_days > 365:
    df = df.resample('D').mean()
# For 1-month view, show hourly
elif date_range_days > 30:
    df = df.resample('H').mean()
# For 1-week view, show all points
else:
    pass  # No aggregation
```

---

## Code Examples

### Example 1: Complete Sync Flow

```python
# src/sync_manager.py (simplified)
from typing import Callable, Optional
from src.garmin_client import GarminClient
from src.database import Database
from src.data_models import SyncStatus
from datetime import datetime, timedelta

class SyncManager:
    def __init__(self, email: str, password: str, db: Database):
        self.client = GarminClient(email, password)
        self.db = db
        self.status = SyncStatus(sync_type="incremental", is_running=False)

    def sync(
        self,
        progress_callback: Optional[Callable] = None,
        mfa_callback: Optional[Callable] = None
    ) -> SyncStatus:
        """Main sync orchestration"""

        self.status.is_running = True
        self.status.start_time = datetime.now()

        try:
            # Step 1: Authenticate
            success, error = self.client.login()
            if not success:
                # Try MFA
                if mfa_callback:
                    code = mfa_callback()
                    success, error = self.client.login(mfa_code=code)

                if not success:
                    raise Exception(f"Auth failed: {error}")

            # Step 2: Determine sync type
            if self.db.get_activity_count() == 0:
                self.status.sync_type = "initial"

            # Step 3: Sync activities
            self._sync_activities(progress_callback)

            # Step 4: Sync health metrics
            self._sync_sleep_data(progress_callback)
            self._sync_daily_stats(progress_callback)
            self._sync_stress_data(progress_callback)
            self._sync_heart_rate_data(progress_callback)

            # Step 5: Log success
            self.status.end_time = datetime.now()
            self.db.log_sync(
                sync_type=self.status.sync_type,
                status="success",
                **self.status.__dict__
            )

        except Exception as e:
            self.status.error_message = str(e)
            self.db.log_sync(
                sync_type=self.status.sync_type,
                status="error",
                error_message=str(e)
            )

        finally:
            self.status.is_running = False

        return self.status

    def _sync_activities(self, progress_callback):
        """Paginated activity sync"""

        offset = 0
        limit = 100
        new_activities = 0

        while True:
            if progress_callback:
                progress_callback(f"Syncing activities", offset, offset + limit)

            # Fetch page
            activities_data = self.client.get_activities(start=offset, limit=limit)

            if not activities_data:
                break

            # Parse and insert
            for activity_data in activities_data:
                activity = self._parse_activity(activity_data)
                self.db.insert_activity(activity)
                new_activities += 1

            # Next page
            offset += limit

            # Stop if we got less than full page (end of data)
            if len(activities_data) < limit:
                break

        self.status.activities_synced = new_activities

    def _sync_sleep_data(self, progress_callback):
        """Day-by-day sleep sync (90-day window)"""

        # Get last synced date or default to 90 days ago
        last_date = self.db.get_last_sleep_date()
        if not last_date:
            last_date = datetime.now() - timedelta(days=90)

        # Sync from last date to today
        current_date = last_date
        today = datetime.now()
        new_records = 0

        while current_date <= today:
            date_str = current_date.strftime("%Y-%m-%d")

            if progress_callback:
                days_total = (today - last_date).days
                days_done = (current_date - last_date).days
                progress_callback(f"Syncing sleep data", days_done, days_total)

            try:
                sleep_data = self.client.get_sleep_data(date_str)
                if sleep_data:
                    parsed = self._parse_sleep_data(sleep_data)
                    self.db.insert_sleep_data(parsed)
                    new_records += 1
            except Exception as e:
                # Log but continue
                print(f"Failed to sync sleep for {date_str}: {e}")

            current_date += timedelta(days=1)

        self.status.sleep_records_synced = new_records

    def _parse_activity(self, data: dict) -> Activity:
        """Parse API response to Activity model"""

        return Activity(
            activity_id=data["activityId"],
            activity_name=data.get("activityName"),
            activity_type=data.get("activityType", {}).get("typeKey"),
            start_time=datetime.fromisoformat(data["startTimeLocal"]),
            duration_seconds=data.get("duration"),
            distance_meters=data.get("distance"),
            average_hr=data.get("averageHR"),
            max_hr=data.get("maxHR"),
            calories=data.get("calories"),
            # ... parse other fields
        )
```

### Example 2: Health Metrics Analyzer

```python
# src/analysis.py (complete analyzer)
import pandas as pd
import numpy as np
from scipy.stats import pearsonr
from src.database import Database
from typing import Dict, List, Tuple

class HealthMetricsAnalyzer:
    """Comprehensive health metrics analysis engine"""

    def __init__(self, db: Database):
        self.db = db

    def get_daily_health_metrics(
        self,
        start_date: str,
        end_date: str
    ) -> pd.DataFrame:
        """
        Unified query joining all health data sources

        Returns DataFrame with columns:
        - calendar_date
        - steps, active_calories, resting_hr (from daily_stats)
        - total_sleep_seconds, sleep_score (from sleep_data)
        - average_stress_level (from stress_data)
        - heart_rate_values (from heart_rate_daily)
        """

        query = """
        SELECT
            ds.calendar_date,
            -- Daily Stats
            ds.steps,
            ds.distance_meters,
            ds.active_calories,
            ds.total_calories,
            ds.floors_climbed,
            ds.resting_hr,
            ds.min_hr,
            ds.max_hr,
            -- Sleep
            s.total_sleep_seconds,
            s.deep_sleep_seconds,
            s.light_sleep_seconds,
            s.rem_sleep_seconds,
            s.awake_seconds,
            s.sleep_score,
            -- Stress
            st.average_stress_level,
            st.max_stress_level,
            st.stress_qualifier,
            st.rest_duration_seconds,
            -- Heart Rate
            hr.average_hr,
            hr.heart_rate_values
        FROM daily_stats ds
        LEFT JOIN sleep_data s ON ds.calendar_date = s.calendar_date
        LEFT JOIN stress_data st ON ds.calendar_date = st.calendar_date
        LEFT JOIN heart_rate_daily hr ON ds.calendar_date = hr.calendar_date
        WHERE ds.calendar_date BETWEEN ? AND ?
        ORDER BY ds.calendar_date
        """

        df = pd.read_sql(
            query,
            self.db.get_connection(),
            params=[start_date, end_date]
        )

        # Add derived metrics
        df = self._add_derived_metrics(df)

        # Add lagged features
        df = self._add_lagged_features(df)

        return df

    def _add_derived_metrics(self, df: pd.DataFrame) -> pd.DataFrame:
        """Compute derived metrics from raw data"""

        # Sleep efficiency
        df['sleep_efficiency'] = (
            df['total_sleep_seconds'] /
            (df['total_sleep_seconds'] + df['awake_seconds']) * 100
        ).fillna(0)

        # Deep sleep percentage
        df['deep_sleep_pct'] = (
            df['deep_sleep_seconds'] /
            df['total_sleep_seconds'] * 100
        ).fillna(0)

        # Heart rate range
        df['hr_range'] = df['max_hr'] - df['min_hr']

        # Stress-rest ratio
        df['stress_rest_ratio'] = (
            df['average_stress_level'] /
            df['rest_duration_seconds'] * 1000
        ).fillna(0)

        # Convert seconds to hours for readability
        df['total_sleep_hours'] = df['total_sleep_seconds'] / 3600

        return df

    def _add_lagged_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add previous-day and rolling average features"""

        # Previous day metrics
        df['prev_sleep_score'] = df['sleep_score'].shift(1)
        df['prev_stress_level'] = df['average_stress_level'].shift(1)
        df['prev_resting_hr'] = df['resting_hr'].shift(1)

        # 7-day rolling averages
        df['sleep_7d_avg'] = df['sleep_score'].rolling(7, min_periods=4).mean()
        df['stress_7d_avg'] = df['average_stress_level'].rolling(7, min_periods=4).mean()
        df['hr_7d_avg'] = df['resting_hr'].rolling(7, min_periods=4).mean()
        df['steps_7d_avg'] = df['steps'].rolling(7, min_periods=4).mean()

        # 30-day baselines
        df['baseline_resting_hr'] = df['resting_hr'].rolling(30, min_periods=14).mean()
        df['baseline_sleep'] = df['sleep_score'].rolling(30, min_periods=14).mean()

        return df

    def calculate_correlations(
        self,
        df: pd.DataFrame
    ) -> Tuple[pd.DataFrame, List[Dict]]:
        """
        Calculate correlation matrix for all metrics

        Returns:
        - Full correlation matrix (DataFrame)
        - List of strong correlations (|r| > 0.5)
        """

        # Select numeric metrics only
        metrics = [
            'steps', 'resting_hr', 'sleep_score', 'sleep_efficiency',
            'average_stress_level', 'active_calories', 'deep_sleep_pct'
        ]

        # Drop rows with NaN in any metric
        df_clean = df[metrics].dropna()

        # Calculate correlation matrix
        corr_matrix = df_clean.corr(method='pearson')

        # Find strong correlations
        strong_correlations = []
        for i, metric1 in enumerate(metrics):
            for j, metric2 in enumerate(metrics):
                if i < j:  # Upper triangle only
                    r = corr_matrix.loc[metric1, metric2]
                    if abs(r) > 0.5:
                        # Calculate p-value
                        _, p_value = pearsonr(df_clean[metric1], df_clean[metric2])

                        strong_correlations.append({
                            'metric1': metric1,
                            'metric2': metric2,
                            'correlation': round(r, 3),
                            'p_value': round(p_value, 4),
                            'significant': p_value < 0.05
                        })

        return corr_matrix, strong_correlations

    def analyze_stress_patterns(self, df: pd.DataFrame) -> Dict:
        """Comprehensive stress analysis"""

        # Distribution by qualifier
        stress_dist = df['stress_qualifier'].value_counts().to_dict()

        # Day of week patterns
        df['day_of_week'] = pd.to_datetime(df['calendar_date']).dt.day_name()
        stress_by_dow = df.groupby('day_of_week')['average_stress_level'].agg([
            'mean', 'median', 'std', 'count'
        ]).to_dict()

        # Weekend vs weekday
        df['is_weekend'] = pd.to_datetime(df['calendar_date']).dt.dayofweek >= 5
        weekend_stress = df[df['is_weekend']]['average_stress_level'].mean()
        weekday_stress = df[~df['is_weekend']]['average_stress_level'].mean()

        # Chronic stress detection (7+ consecutive days >55)
        df['high_stress'] = df['average_stress_level'] > 55
        df['stress_streak'] = (
            df['high_stress']
            .groupby((df['high_stress'] != df['high_stress'].shift()).cumsum())
            .cumsum()
        )
        chronic_periods = df[df['stress_streak'] >= 7][['calendar_date', 'average_stress_level', 'stress_streak']]

        # Correlations
        correlations = {}
        for metric in ['sleep_score', 'steps', 'resting_hr']:
            if metric in df.columns:
                clean = df[['average_stress_level', metric]].dropna()
                if len(clean) > 2:
                    r, p = pearsonr(clean['average_stress_level'], clean[metric])
                    correlations[metric] = {'r': round(r, 3), 'p': round(p, 4)}

        return {
            'summary': {
                'mean': df['average_stress_level'].mean(),
                'median': df['average_stress_level'].median(),
                'std': df['average_stress_level'].std(),
                'min': df['average_stress_level'].min(),
                'max': df['average_stress_level'].max()
            },
            'distribution': stress_dist,
            'day_of_week': stress_by_dow,
            'weekend_vs_weekday': {
                'weekend': round(weekend_stress, 1),
                'weekday': round(weekday_stress, 1),
                'difference': round(weekend_stress - weekday_stress, 1)
            },
            'chronic_stress_periods': chronic_periods.to_dict(orient='records'),
            'correlations': correlations
        }

    def identify_recovery_days(
        self,
        df: pd.DataFrame,
        threshold: int = 60
    ) -> pd.DataFrame:
        """
        Identify days needing recovery

        Composite score based on:
        - Elevated resting HR
        - Poor sleep
        - High stress
        """

        # Ensure baselines exist
        if 'baseline_resting_hr' not in df.columns:
            df = self._add_lagged_features(df)

        # HR recovery score (100 = perfect, 0 = very elevated)
        df['hr_recovery_score'] = (
            100 - ((df['resting_hr'] - df['baseline_resting_hr']) /
                   df['baseline_resting_hr'] * 100).clip(-100, 100)
        ).fillna(100)

        # Sleep recovery score (already 0-100)
        df['sleep_recovery_score'] = df['sleep_score'].fillna(70)

        # Stress recovery score (inverted)
        df['stress_recovery_score'] = (100 - df['average_stress_level']).fillna(70)

        # Composite recovery score
        df['recovery_score'] = (
            df['hr_recovery_score'] * 0.4 +
            df['sleep_recovery_score'] * 0.3 +
            df['stress_recovery_score'] * 0.3
        )

        # Flag recovery days
        df['needs_recovery'] = df['recovery_score'] < threshold

        return df

    def generate_health_score(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Generate composite health score (0-100)

        Components:
        - Sleep: 30%
        - Activity: 25%
        - Stress: 25%
        - Heart Rate: 20%
        """

        # Sleep score (already 0-100)
        sleep_component = df['sleep_score'].fillna(70)

        # Activity score (steps vs 10k goal)
        activity_component = (df['steps'] / 10000 * 100).clip(0, 100).fillna(50)

        # Stress score (inverted)
        stress_component = (100 - df['average_stress_level']).fillna(70)

        # HR score (based on deviation from baseline)
        hr_deviation = abs(
            (df['resting_hr'] - df['baseline_resting_hr']) /
            df['baseline_resting_hr'] * 100
        ).fillna(0)
        hr_component = (100 - hr_deviation).clip(0, 100)

        # Weighted composite
        df['health_score'] = (
            sleep_component * 0.30 +
            activity_component * 0.25 +
            stress_component * 0.25 +
            hr_component * 0.20
        )

        return df
```

---

## Future Opportunities

### Features Not Yet Implemented (But Designed)

From `DASHBOARD_REDESIGN_PROPOSAL.md`:

#### 1. Flexible Time Window Analysis

**Concept:** User defines both date range AND grouping level

**UI:**
```
Date Range: [2024-01-01] to [2024-12-31]
Group By: ( ) Day  ( ) Week  (•) Month  ( ) Year
Compare: [√] Year-over-year  [ ] Seasonal
```

**Use Cases:**
- "Show all Januaries across years" (seasonal patterns)
- "Compare spring 2023 vs spring 2024"
- "Week-by-week view of last 90 days"

**Implementation Hints:**
```python
class TimeWindowConfig:
    start_date: date
    end_date: date
    grouping: Literal["day", "week", "month", "year"]
    comparison_mode: Optional[Literal["yoy", "seasonal"]]

def aggregate_by_window(df, config):
    if config.grouping == "month":
        return df.groupby(df['date'].dt.month).mean()
    elif config.grouping == "week":
        return df.resample('W').mean()
    # ...
```

#### 2. Relationship Explorer

**Concept:** Interactive scatter plot with dynamic axis selection

**UI:**
```
X-Axis: [Sleep Score ▼]
Y-Axis: [Next-Day Distance ▼]
Color: [Stress Level ▼]
Size: [Duration ▼]
```

**Value:** Enables hypothesis testing
- "Does sleep affect activity?" → X=sleep, Y=distance
- "What's the optimal stress level?" → X=stress, Y=performance

#### 3. Annotation System

**Concept:** User marks significant events for context

**Schema:**
```sql
CREATE TABLE annotations (
    id INTEGER PRIMARY KEY,
    calendar_date TEXT NOT NULL,
    label TEXT NOT NULL,
    category TEXT,  -- 'life_event', 'illness', 'travel'
    description TEXT
);
```

**Visualization:** Vertical lines on charts with hover labels

**Use Case:** Explain metric anomalies
- "Why was stress high on March 15?" → annotation shows "Started new job"

#### 4. Menstrual Cycle Integration

**Concept:** Overlay metrics onto cycle phases

**Requirements:**
- Garmin API support (or manual input)
- Phase normalization (variable cycle lengths)

**Schema:**
```sql
CREATE TABLE menstrual_cycles (
    cycle_id INTEGER PRIMARY KEY,
    cycle_start_date TEXT NOT NULL,
    follicular_phase_end TEXT,
    ovulatory_phase_end TEXT,
    luteal_phase_end TEXT
);
```

**Analysis:**
```python
def analyze_by_cycle_phase(df, cycles_df):
    """
    Group metrics by cycle phase across multiple cycles

    Handles variable cycle lengths by normalizing to % of phase
    """
    # ... implementation
```

#### 5. Predictive Models

**Concept:** Predict tomorrow's metrics based on today's data

**Simple Approach (Linear Regression):**
```python
from sklearn.linear_model import LinearRegression

def predict_stress(df):
    """Predict tomorrow's stress from today's features"""

    features = ['prev_sleep_score', 'prev_steps', 'prev_resting_hr', 'day_of_week']
    target = 'average_stress_level'

    X = df[features].dropna()
    y = df[target].dropna()

    model = LinearRegression()
    model.fit(X, y)

    # Predict next day
    tomorrow_features = [today_sleep, today_steps, today_hr, tomorrow_dow]
    predicted_stress = model.predict([tomorrow_features])[0]

    return predicted_stress
```

**Advanced Approach (XGBoost for better accuracy):**
```python
import xgboost as xgb

model = xgb.XGBRegressor(
    objective='reg:squarederror',
    n_estimators=100,
    max_depth=5
)
model.fit(X_train, y_train)
```

#### 6. Body Battery & HRV

**Concept:** Additional Garmin metrics (if available)

**Body Battery:**
- 0-100 energy level
- Drained by stress/activity
- Recharged by sleep/rest

**HRV (Heart Rate Variability):**
- Higher = better recovery
- Key metric for overtraining detection

**API Endpoints (not yet implemented in gar-mining):**
```
GET /wellness-service/wellness/bodyBattery/reports/daily?startDate={start}&endDate={end}
GET /hrv-service/hrv/daily?date={date}
```

---

## Appendix: File Reference

### Core Files to Study

**Most Valuable for Migration:**

1. `src/data_models.py` (281 lines)
   - Clean dataclass definitions
   - Computed properties pattern
   - **Migrate to:** Pydantic models for FastAPI

2. `src/database.py` (498 lines)
   - SQLite schema and CRUD operations
   - **Study for:** Table structure, indexes, query patterns

3. `src/sync_manager.py` (706 lines)
   - Complex orchestration logic
   - Progress tracking
   - Error resilience
   - **Adapt for:** GDPR import and FIT file parsing

4. `src/analysis.py` (811 lines)
   - Core analytics algorithms
   - **Preserve:** Correlation analysis, health scoring, recovery detection

5. `API_ENDPOINTS.md`
   - Garmin API documentation
   - Field name variations
   - **Reference for:** GDPR export schema mapping

6. `DASHBOARD_REDESIGN_PROPOSAL.md`
   - Advanced features roadmap
   - **Ideas for:** Foldline feature planning

### Less Critical (Streamlit-Specific)

- `app.py` - Streamlit main page (replace with SvelteKit)
- `pages/*.py` - Streamlit multi-page (replace with SvelteKit routes)
- `.streamlit/` - Streamlit config (not applicable)

---

## Questions for Foldline Team

1. **Database Choice:** SQLite (simple) or DuckDB (faster analytics)?

2. **FIT Parsing Library:** fitparse (Python) or garmin-fit-sdk (official)?

3. **Real-time Sync:** Should Foldline auto-import FIT files from watched directory?

4. **GDPR Export Frequency:** One-time import or support repeated imports?

5. **Migration Path:** Should we support importing from gar-mining SQLite databases?

6. **Feature Priorities:** Which analytics features are must-have vs. nice-to-have?

7. **Visualization Approach:** Continue with Plotly or consider alternatives (Chart.js, D3)?

8. **Multi-user Support:** Single user per app instance or multi-user with separate profiles?

---

## Conclusion

gar-mining provides a solid foundation for Foldline's development:

**Preserve:**
- ✅ Data models and schemas (proven structure)
- ✅ Analytics algorithms (valuable insights)
- ✅ Visualization patterns (Plotly works everywhere)
- ✅ Error handling patterns (resilience is critical)

**Discard:**
- ❌ Garmin API client (replaced by FIT parsers)
- ❌ Streamlit UI code (replaced by SvelteKit)
- ❌ OAuth/session management (not needed)

**Enhance:**
- 🔄 Add FIT file support (richer data than API)
- 🔄 Implement GDPR import (complete history)
- 🔄 Add local file monitoring (real-time updates)
- 🔄 Improve performance with DuckDB (optional)

**Key Advantage of Foldline:**
By moving to GDPR exports and FIT files, Foldline eliminates the biggest pain points of gar-mining (90-day limitation, API rate limits, auth complexity) while gaining access to higher-resolution data and complete historical records.

This is a strong technical foundation for a privacy-first, local-only wearable analytics platform.

---

**Document Version:** 1.0
**Last Updated:** 2025-11-22
**Contact:** See gar-mining GitHub repository for questions
