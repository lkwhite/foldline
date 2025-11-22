# Foldline Integration Roadmap

**Visual guide for integrating INTEGRATION_PLAN.md with current codebase**

---

## 🎯 MVP Roadmap (4-6 Weeks to Launch)

```
Week 1-2: PAYMENT FOUNDATION
├─ 📄 Read design/FOLDLINE_DESIGN_SPEC.md
├─ 📝 Create PAYMENT_ARCHITECTURE.md
├─ 🔧 Update .env.example (Lemon Squeezy vars)
├─ 🌐 Marketing site "Buy Foldline" button
│   └─ Link to LS hosted checkout
├─ 🖥️  App license activation UI
│   ├─ Simple text input
│   ├─ Local storage
│   └─ Basic validation (trust model)
└─ ✅ Test end-to-end purchase flow

Week 2-3: DATA IMPORT
├─ 📦 Complete backend/ingestion/garmin_gdpr.py
│   ├─ ZIP extraction
│   ├─ File categorization (FIT/JSON/TCX)
│   ├─ GDPR field mappings
│   └─ Progress tracking
├─ 🔧 Enhance backend/ingestion/fit_folder.py
│   └─ Add field mappings from handoff
├─ 🧪 Test with real GDPR exports
└─ ✅ Import success rate >95%

Week 3-4: VISUALIZATION
├─ 📦 npm install plotly.js-dist
├─ 🎨 Create chart components
│   ├─ frontend/src/lib/components/TimeSeriesChart.svelte
│   │   └─ Port from handoff lines 1108-1171
│   ├─ frontend/src/lib/components/HeatmapChart.svelte
│   │   └─ Port from handoff lines 1173-1200
│   └─ frontend/src/lib/components/CorrelationScatter.svelte
│       └─ Port from handoff lines 1299-1332
├─ 🔗 Integrate into pages
│   ├─ routes/heatmaps/+page.svelte
│   ├─ routes/trends/+page.svelte
│   └─ routes/correlation/+page.svelte
└─ ✅ Charts render in <1 second

Week 4-6: BASIC ANALYTICS
├─ 📂 Create backend/analytics/ directory
├─ 📝 Implement metric queries in backend/metrics/
│   ├─ sleep.py::get_sleep_heatmap()
│   │   └─ Query sleep_records, return {date, duration_hours}
│   ├─ sleep.py::get_sleep_timeseries()
│   │   └─ With 7-day rolling average
│   ├─ hrv.py::get_hrv_heatmap()
│   │   └─ Query hrv_records, return {date, hrv_value}
│   ├─ stress.py::get_stress_heatmap()
│   │   └─ Query stress_records, return {date, avg_stress}
│   └─ steps.py::get_steps_heatmap()
│       └─ Query daily_steps, return {date, steps}
├─ 📊 Create basic dashboard endpoint
│   └─ GET /analytics/dashboard
│       ├─ Date range summary
│       ├─ Metric averages
│       └─ Data completeness stats
└─ ✅ All metric queries working

Week 6: POLISH & LAUNCH
├─ 🐛 Bug fixes from testing
├─ 📖 Update README with actual usage
├─ 🎨 Marketing site screenshots
├─ 🚀 Soft launch to beta users
└─ ✅ First 10 paying customers
```

---

## 📊 Current vs. Target State

### Database Schema

```
Current State (✅ DONE):
├─ 15 tables defined in backend/db/schema.sql
│   ├─ sleep_records
│   ├─ sleep_detailed
│   ├─ resting_hr
│   ├─ hrv_records
│   ├─ stress_records (realtime)
│   ├─ daily_stress
│   ├─ daily_summaries
│   ├─ daily_steps
│   ├─ activities
│   ├─ menstrual_cycles
│   ├─ hydration_logs
│   ├─ body_composition
│   ├─ fitness_assessments
│   ├─ imported_files
│   └─ data_sources
└─ DuckDB connection with SQLite fallback

MVP Additions (Week 4-6):
└─ (None - current schema sufficient for MVP)

Post-MVP Additions:
├─ raw_data TEXT columns on all tables
├─ heart_rate_timeseries table (intra-day HR)
├─ import_log table (tracking)
└─ annotations table (user notes)
```

### Data Import Pipeline

```
Current State:
├─ ✅ backend/ingestion/fit_folder.py (WORKS)
│   ├─ Recursive directory scan
│   ├─ SHA256 deduplication
│   └─ FIT message parsing
├─ 🟨 backend/ingestion/json_parser.py (PARTIAL)
│   ├─ Sleep JSON parsing
│   └─ Daily summary parsing (needs field mappings)
└─ ❌ backend/ingestion/garmin_gdpr.py (STUBBED)
    └─ All functions return empty dicts

MVP Target (Week 2-3):
└─ ✅ backend/ingestion/garmin_gdpr.py (COMPLETE)
    ├─ extract_garmin_export() - ZIP extraction
    ├─ process_gdpr_export() - Full pipeline
    └─ GDPR-specific field mappings
```

### Analytics Modules

```
Current State:
├─ ❌ backend/analytics/ (DOESN'T EXIST)
└─ ❌ backend/metrics/*.py (ALL STUBBED)
    ├─ sleep.py - returns []
    ├─ hrv.py - returns []
    ├─ stress.py - returns []
    └─ steps.py - returns []

MVP Target (Week 4-6):
├─ ✅ backend/metrics/*.py (BASIC QUERIES)
│   ├─ get_sleep_heatmap() → [{date, value}, ...]
│   ├─ get_sleep_timeseries() → [{date, value, avg_7d}, ...]
│   ├─ get_hrv_heatmap() → [{date, value}, ...]
│   ├─ get_stress_heatmap() → [{date, value}, ...]
│   └─ get_steps_heatmap() → [{date, value}, ...]
└─ ✅ GET /analytics/dashboard endpoint

Post-MVP Target:
└─ ✅ backend/analytics/ (ADVANCED)
    ├─ health_metrics.py - Multi-metric analyzer
    ├─ health_score.py - 0-100 wellness score
    ├─ recovery.py - Recovery day detection
    ├─ correlation.py - Pearson/Spearman analysis
    ├─ stress_analysis.py - Pattern detection
    ├─ sleep_activity.py - Bidirectional correlation
    └─ activity_optimization.py - Optimal range finder
```

### Visualization

```
Current State:
├─ ❌ No charting library
└─ ❌ All route pages show stub text

MVP Target (Week 3-4):
├─ ✅ plotly.js-dist installed
├─ ✅ frontend/src/lib/components/TimeSeriesChart.svelte
├─ ✅ frontend/src/lib/components/HeatmapChart.svelte
└─ ✅ Pages render actual charts
    ├─ routes/heatmaps/+page.svelte
    ├─ routes/trends/+page.svelte
    └─ routes/correlation/+page.svelte

Post-MVP:
├─ CorrelationHeatmap.svelte (matrix)
├─ HealthScoreGauge.svelte (0-100 dial)
└─ Multi-panel time series (4+ metrics)
```

### Payment System

```
Current State:
└─ ❌ Not implemented

MVP Target (Week 1-2):
├─ ✅ PAYMENT_ARCHITECTURE.md
├─ ✅ .env.example (LS variables)
├─ ✅ marketing/src/routes/buy/+page.svelte
│   └─ Link to Lemon Squeezy checkout
└─ ✅ frontend/src/routes/license/+page.svelte
    ├─ License key input
    ├─ Local storage (Tauri secure)
    └─ Basic validation (trust model)

Post-MVP:
├─ Real LS API validation
├─ License expiry checks
└─ Upgrade path (if needed)
```

---

## 🔄 Integration Flow

### From INTEGRATION_PLAN.md → Actual Code

#### Phase 1: Analytics Foundation (INTEGRATION_PLAN.md lines 583-616)

**What INTEGRATION_PLAN.md Says:**
```
Tasks:
1. Create backend/analytics/
2. Port Health Metrics Analyzer
3. Implement actual metric queries
4. Port Health Score algorithm
5. Port Recovery Detection
6. Port Correlation Analysis
```

**What We're Actually Doing:**

**MVP (Week 4-6):**
- ✅ Create backend/analytics/ (for future)
- ⏭️  Skip Health Metrics Analyzer (not needed for MVP)
- ✅ Implement basic metric queries ONLY
- ⏭️  Skip Health Score (post-MVP)
- ⏭️  Skip Recovery Detection (post-MVP)
- ⏭️  Skip Correlation Analysis (post-MVP)

**Rationale:**
- Users need to see their data first (heatmaps/trends)
- Advanced analytics can come after launch
- Simplifies MVP scope

---

#### Phase 2: Visualization (INTEGRATION_PLAN.md lines 618-648)

**What INTEGRATION_PLAN.md Says:**
```
Tasks:
1. Install Plotly
2. Create TimeSeriesChart.svelte
3. Create HeatmapChart.svelte
4. Create CorrelationScatter.svelte
5. Create HealthScoreGauge.svelte
6. Port all visualization patterns
```

**What We're Actually Doing:**

**MVP (Week 3-4):**
- ✅ Install Plotly
- ✅ Create TimeSeriesChart.svelte
- ✅ Create HeatmapChart.svelte
- ⏭️  Skip CorrelationScatter (post-MVP)
- ⏭️  Skip HealthScoreGauge (post-MVP)
- ✅ Port basic patterns (time series, heatmap)

**Rationale:**
- Two chart types sufficient for MVP
- Can add more chart types based on feedback

---

#### Phase 3: Complete GDPR Import (INTEGRATION_PLAN.md lines 650-677)

**What INTEGRATION_PLAN.md Says:**
```
Tasks:
1. Implement extract_garmin_export()
2. Implement process_gdpr_export()
3. Update POST /import/garmin-export
4. Test with real GDPR export
```

**What We're Actually Doing:**

**MVP (Week 2-3):**
- ✅ Implement extract_garmin_export()
- ✅ Implement process_gdpr_export()
- ✅ Update POST /import/garmin-export
- ✅ Test with real GDPR export

**Rationale:**
- Critical for user onboarding
- Can't use app without data import
- Must be in MVP

---

#### Phase 4: Schema Enhancements (INTEGRATION_PLAN.md lines 679-715)

**What INTEGRATION_PLAN.md Says:**
```
Tasks:
1. Add raw_data columns
2. Add source tracking to activities
3. Create import_log table
4. Create heart_rate_timeseries table
5. Update parsers
6. Migration script
```

**What We're Actually Doing:**

**MVP:**
- ⏭️  Skip all of Phase 4

**Post-MVP Phase 1:**
- ✅ Add raw_data columns
- ✅ Add source tracking
- ✅ Create import_log table
- ✅ Create heart_rate_timeseries table

**Rationale:**
- Schema enhancements are nice-to-have
- Current schema works for MVP
- Can add later without breaking changes

---

#### Phase 5: Advanced Analytics (INTEGRATION_PLAN.md lines 717-753)

**What INTEGRATION_PLAN.md Says:**
```
Tasks:
1. Port Stress Pattern Analysis
2. Port Sleep-Activity Correlation
3. Port Optimal Activity Range
4. Create comprehensive dashboard endpoint
```

**What We're Actually Doing:**

**MVP:**
- ⏭️  Skip all of Phase 5

**Post-MVP Phase 2:**
- ✅ Port Stress Pattern Analysis
- ✅ Port Sleep-Activity Correlation
- ✅ Port Optimal Activity Range
- ✅ Create comprehensive dashboard

**Rationale:**
- Advanced analytics are differentiators
- But not critical for initial validation
- Can add based on user requests

---

#### Phase 6: Future Features (INTEGRATION_PLAN.md lines 755-793)

**What INTEGRATION_PLAN.md Says:**
```
Tasks:
1. Annotations System
2. Flexible Time Windows
3. Relationship Explorer
4. Predictive Models
5. FIT Directory Watcher
6. Data Export
```

**What We're Actually Doing:**

**MVP:**
- ⏭️  Skip all of Phase 6

**Post-MVP (Ongoing):**
- Evaluate based on user feedback
- Prioritize most-requested features
- Keep backlog

**Rationale:**
- These are nice-to-have enhancements
- Not needed to validate product-market fit
- May never build some of these

---

## 📋 MVP Scope Definition

### What's IN the MVP

```
✅ MUST HAVE (Blocks Launch):
├─ Payment system (Lemon Squeezy)
├─ License activation UI
├─ GDPR import (complete)
├─ FIT import (enhance existing)
├─ Plotly charts (basic)
├─ Metric queries (sleep, HRV, stress, steps)
├─ Heatmap view (working)
├─ Trends view (working)
├─ Dashboard (basic stats)
└─ Offline capability

✅ SHOULD HAVE (Enhances Value):
├─ Dark/light theme (already exists)
├─ Settings page (already exists)
├─ Data export (CSV)
├─ Error handling
├─ Loading states
└─ Help/documentation

❌ WON'T HAVE (Post-MVP):
├─ Advanced analytics (health score, recovery)
├─ Correlation analysis
├─ Predictive models
├─ Annotations system
├─ FIT directory watcher
├─ WebSocket progress updates
└─ Migration from gar-mining
```

### What's OUT of MVP (Post-Launch)

```
Post-MVP Phase 1 (Weeks 7-9):
├─ Health Score algorithm
├─ Recovery Detection
├─ Correlation Analysis endpoint
├─ CorrelationScatter component
├─ HealthScoreGauge component
└─ Comprehensive dashboard

Post-MVP Phase 2 (Weeks 10-12):
├─ Stress Pattern Analysis
├─ Sleep-Activity Correlation
├─ Optimal Activity Range
└─ Advanced visualizations

Post-MVP Phase 3 (Ongoing):
├─ Schema enhancements (raw_data, HR timeseries)
├─ Annotations system
├─ Predictive models
├─ FIT directory watcher
└─ Power user features
```

---

## 🛠️ Implementation Checklist

### Week 1: Payment Foundation Part 1

- [ ] Read design/FOLDLINE_DESIGN_SPEC.md
- [ ] Document findings in PAYMENT_ARCHITECTURE.md
- [ ] Update .env.example with Lemon Squeezy variables
  - [ ] LEMONSQUEEZY_STORE_ID
  - [ ] LEMONSQUEEZY_PRODUCT_ID
  - [ ] LEMONSQUEEZY_API_KEY
  - [ ] LEMONSQUEEZY_WEBHOOK_SECRET (optional)

### Week 2: Payment Foundation Part 2

- [ ] Create marketing/src/routes/buy/+page.svelte
  - [ ] Explain PWYW model
  - [ ] Privacy-first messaging
  - [ ] 10% EFF donation mention
  - [ ] "Continue to checkout" button → LS hosted URL
- [ ] Create frontend/src/routes/license/+page.svelte
  - [ ] License key input field
  - [ ] "Activate" button
  - [ ] Store in Tauri secure storage
  - [ ] Simple validation (non-empty)
  - [ ] "About your license" panel
- [ ] Test end-to-end purchase flow

### Week 3: Data Import Part 1

- [ ] Implement backend/ingestion/garmin_gdpr.py::extract_garmin_export()
  - [ ] ZIP extraction using zipfile
  - [ ] Find DI_CONNECT/ directory structure
  - [ ] Categorize files (FIT, JSON, TCX)
  - [ ] Return file inventory
- [ ] Implement GDPR field mappings
  - [ ] Create backend/ingestion/field_mappings.py
  - [ ] Map GDPR JSON fields → Foldline schema
  - [ ] sleepStartTimestampGMT → start_time
  - [ ] sleepEndTimestampGMT → end_time
  - [ ] totalSleepTime → duration_minutes
  - [ ] etc. (see INTEGRATION_PLAN.md lines 224-237)

### Week 4: Data Import Part 2

- [ ] Implement backend/ingestion/garmin_gdpr.py::process_gdpr_export()
  - [ ] Extract ZIP to temp directory
  - [ ] Process all FIT files (use existing fit_folder.py)
  - [ ] Process all JSON files (use existing json_parser.py)
  - [ ] Return comprehensive summary
- [ ] Update POST /import/garmin-export endpoint
  - [ ] Accept ZIP file upload
  - [ ] Call process_gdpr_export()
  - [ ] Return detailed import summary
- [ ] Test with real GDPR exports
  - [ ] Get test files from various users/dates
  - [ ] Verify >95% import success rate

### Week 5: Visualization Part 1

- [ ] Install Plotly
  ```bash
  cd frontend
  npm install plotly.js-dist
  ```
- [ ] Create frontend/src/lib/components/TimeSeriesChart.svelte
  - [ ] Accept data: [{date, value}, ...]
  - [ ] Render line chart
  - [ ] Add 7-day rolling average (dashed line)
  - [ ] Interactive (zoom, pan, hover)
  - [ ] Port pattern from FOLDLINE_HANDOFF.md lines 1108-1171

### Week 6: Visualization Part 2

- [ ] Create frontend/src/lib/components/HeatmapChart.svelte
  - [ ] Accept data: [{date, value}, ...]
  - [ ] Render calendar heatmap
  - [ ] Color intensity by value
  - [ ] Port pattern from FOLDLINE_HANDOFF.md lines 1173-1200
- [ ] Integrate charts into pages
  - [ ] Update routes/heatmaps/+page.svelte
  - [ ] Update routes/trends/+page.svelte
  - [ ] Remove stub text
  - [ ] Add chart containers

### Week 7: Analytics Part 1

- [ ] Create backend/analytics/ directory
- [ ] Implement backend/metrics/sleep.py::get_sleep_heatmap()
  ```python
  def get_sleep_heatmap(db_connection, start_date, end_date):
      query = """
          SELECT date, duration_minutes / 60.0 as value
          FROM sleep_records
          WHERE date BETWEEN ? AND ?
          ORDER BY date
      """
      return execute_query(query, [start_date, end_date])
  ```
- [ ] Implement backend/metrics/sleep.py::get_sleep_timeseries()
  ```python
  def get_sleep_timeseries(db_connection, start_date, end_date, smoothing_window=7):
      query = """
          SELECT
              date,
              duration_minutes / 60.0 as value,
              AVG(duration_minutes / 60.0) OVER (
                  ORDER BY date
                  ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
              ) as avg_7d
          FROM sleep_records
          WHERE date BETWEEN ? AND ?
          ORDER BY date
      """
      return execute_query(query, [start_date, end_date])
  ```

### Week 8: Analytics Part 2

- [ ] Implement backend/metrics/hrv.py::get_hrv_heatmap()
- [ ] Implement backend/metrics/stress.py::get_stress_heatmap()
- [ ] Implement backend/metrics/steps.py::get_steps_heatmap()
- [ ] Test all queries with real data

### Week 9: Dashboard & Polish

- [ ] Create GET /analytics/dashboard endpoint
  ```python
  {
    "date_range": {"start": "2024-01-01", "end": "2024-12-31"},
    "total_days": 365,
    "sleep_avg_hours": 7.2,
    "hrv_avg": 45,
    "stress_avg": 35,
    "steps_avg": 8500,
    "data_completeness": {
      "sleep": 98,  # % of days with data
      "hrv": 95,
      "stress": 92,
      "steps": 97
    }
  }
  ```
- [ ] Update routes/dashboard/+page.svelte to use real data
- [ ] Bug fixes from testing
- [ ] Update README with actual usage instructions

### Week 10: Launch Prep

- [ ] Create marketing site screenshots
- [ ] Write launch blog post
- [ ] Set up support email
- [ ] Soft launch to beta users (friends, family)
- [ ] Collect feedback
- [ ] Fix critical bugs
- [ ] Public launch!

---

## 📊 Success Criteria

### MVP Launch Checklist

**Before announcing publicly:**

- [ ] Payment system works end-to-end
  - [ ] User can purchase license
  - [ ] User receives license key via email
  - [ ] User can activate in app
  - [ ] App works offline after activation
- [ ] Data import works reliably
  - [ ] GDPR import success rate >95%
  - [ ] FIT import success rate >98%
  - [ ] Deduplication prevents double-imports
  - [ ] Progress feedback during import
- [ ] Visualizations are functional
  - [ ] Heatmaps render correctly
  - [ ] Trends show time series
  - [ ] Charts are interactive
  - [ ] Load time <1 second
- [ ] Analytics provide value
  - [ ] All metric queries return real data
  - [ ] Dashboard shows summary stats
  - [ ] Data is accurate (spot-check)
- [ ] Quality standards met
  - [ ] All tests passing
  - [ ] No critical bugs
  - [ ] Works on Windows, macOS, Linux
  - [ ] Offline mode works
  - [ ] No data leaves user's machine

---

## 🎉 Post-Launch Roadmap

### Months 2-3: Advanced Analytics

Based on INTEGRATION_PLAN.md Phases 1 & 5:

- [ ] Port Health Metrics Analyzer
- [ ] Implement Health Score algorithm
- [ ] Add Recovery Detection
- [ ] Build Correlation Analysis
- [ ] Create advanced dashboard

### Months 4-6: Power User Features

Based on INTEGRATION_PLAN.md Phases 4 & 6:

- [ ] Add raw_data columns (re-parsing capability)
- [ ] Create annotations system
- [ ] Build relationship explorer
- [ ] Add FIT directory watcher
- [ ] Implement data export

### Months 7-12: Advanced Features

Based on user feedback and INTEGRATION_PLAN.md Phase 6:

- [ ] Predictive models (ML-based)
- [ ] Flexible time windows
- [ ] Migration from gar-mining
- [ ] Support for other devices (Whoop, Oura, etc.)

---

## 📝 Key Takeaways

1. **INTEGRATION_PLAN.md is excellent** but represents 3-4 months of work
2. **MVP can launch in 4-6 weeks** with focused scope
3. **Payment system is critical** - blocks revenue
4. **GDPR import is critical** - blocks user onboarding
5. **Basic viz + analytics** - provides user value
6. **Advanced analytics** - can wait until post-MVP
7. **Schema enhancements** - nice-to-have, not critical
8. **Future features** - evaluate based on feedback

**The goal is to launch, learn, and iterate - not to build everything before validating product-market fit.**
