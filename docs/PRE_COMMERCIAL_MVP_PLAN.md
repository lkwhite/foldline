# Foldline Pre-Commercial MVP Plan

**Date:** 2025-11-22
**Target:** Beta-ready product for user validation (pre-revenue)
**Timeline:** 5-6 weeks
**Integrated from:** CONTINUAL_SYNC_SPEC.md + INTEGRATION_ROADMAP.md + INTEGRATION_ANALYSIS.md

---

## Executive Summary

### What Changed from Original Integration Plan

**Original Plan:** Payment system → GDPR import → Visualization → Analytics → Launch for revenue

**Pre-Commercial MVP:** GDPR import → Garmin Express Auto-Sync → Visualization → Basic Analytics → Beta testing

**Key Differences:**
- ⏭️ **Skip payment system** (not needed for beta)
- ✅ **Add Garmin Express auto-sync** (critical UX differentiator)
- ✅ **Focus on data freshness** (ongoing sync, not just one-time import)
- 🎯 **Goal:** Validate product-market fit before commercializing

---

## Pre-Commercial MVP Scope

### What Users Can Do

**Initial Setup:**
1. Import historical data from Garmin GDPR export
2. Configure Garmin Express device(s) for auto-sync
3. View data visualizations (heatmaps, trends)
4. See basic health metrics

**Ongoing Use:**
1. Click "Sync Now" to update from Garmin Express
2. Optionally enable "sync on startup"
3. Browse updated visualizations
4. Track metrics over time

**What's NOT Included (Post-Commercial):**
- Payment/licensing system
- Advanced analytics (health score, recovery detection, correlations)
- Marketing site polish
- Watched folders or manual folder re-import
- Annotations, predictions, relationship explorer

---

## Implementation Timeline

### Week 1: Foundation & GDPR Import

**Database Schema Enhancement**
- [ ] Enhance `imported_files` table with sync fields
  - `file_size BIGINT`
  - `modified_time TIMESTAMP`
  - `first_seen_at TIMESTAMP`
  - `source TEXT` (gdpr, garmin_express, manual)
  - `last_error TEXT`
- [ ] Create migration script (if needed)
- [ ] Update tests

**GDPR Import Implementation**
- [ ] `backend/ingestion/garmin_gdpr.py::extract_garmin_export()`
  - ZIP extraction with `zipfile`
  - Find DI_CONNECT/ directory structure
  - Categorize files (FIT, JSON, TCX)
  - Return file inventory
- [ ] `backend/ingestion/field_mappings.py`
  - GDPR JSON field mappings from CONTINUAL_SYNC_SPEC
  - Sleep: sleepStartTimestampGMT → start_time
  - Sleep: sleepEndTimestampGMT → end_time
  - Sleep: totalSleepTime → duration_minutes
  - Daily: totalSteps → step_count
  - etc.
- [ ] `backend/ingestion/garmin_gdpr.py::process_gdpr_export()`
  - Extract ZIP to temp directory
  - Process all FIT files (use existing fit_folder.py)
  - Process all JSON files (use existing json_parser.py)
  - Comprehensive progress tracking
  - Error resilience (per-file try/catch)
  - Return summary
- [ ] Update `POST /import/garmin-export` endpoint
  - Accept ZIP file upload
  - Call process_gdpr_export()
  - Return detailed import summary with errors
- [ ] Test with real GDPR exports (multiple users/dates)

**Acceptance Criteria:**
- [ ] GDPR import success rate >95%
- [ ] Handles malformed files gracefully
- [ ] Deduplication prevents double-imports
- [ ] Returns actionable error messages

---

### Week 2: Garmin Express Detection (macOS)

**Device Detection Module**
- [ ] Create `backend/sync/garmin_express.py`
- [ ] `detect_garmin_devices()` for macOS
  - Search: `~/Library/Application Support/Garmin/Devices/`
  - For each `<DEVICE-ID>` folder:
    - Scan for subdirectories (Activities/, Monitor/, Sleep/, Stress/, Daily/)
    - Count .fit files
    - Get most recent modified timestamp
    - Extract device name (if available from device.fit or folder metadata)
  - Return device list with metadata:
    ```python
    {
        "device_id": "1234567890",
        "name": "Garmin Forerunner 945",  # or device_id if name unavailable
        "path": "/Users/foo/Library/.../Devices/1234567890",
        "file_count": 1243,
        "last_sync": "2025-11-20T14:32:00Z",
        "subfolders": ["Activities", "Monitor", "Sleep"]
    }
    ```
- [ ] `GET /sync/garmin-express/devices` API endpoint
- [ ] Store device config in database
  - Create `garmin_express_devices` table
  - Columns: device_id, device_path, enabled, last_sync_at, created_at
- [ ] Test with real Garmin Express installation

**Acceptance Criteria:**
- [ ] Detects all connected Garmin devices
- [ ] Handles missing Garmin Express gracefully
- [ ] Provides clear error messages if Express not installed
- [ ] Works on macOS (primary target)

---

### Week 3: Garmin Express Sync Implementation + Windows Support

**Incremental Sync Algorithm**
- [ ] Enhance `backend/ingestion/fit_folder.py::scan_fit_directory()`
  - Add `last_sync_time` parameter
  - Filter files by modified_time > last_sync_time
  - Return only new/changed files
- [ ] Create `backend/sync/sync_engine.py`
  - `sync_garmin_express_device(device_id, db_connection)`
    - Get device path from config
    - Get last_sync_at timestamp
    - Recursively walk device subdirectories
    - For each .fit file:
      - Check if file_hash exists in imported_files
      - If new: ingest via existing fit_folder.parse_fit_file()
      - If changed (size or modified_time differs): re-ingest
      - If unchanged: skip
    - Track: files_scanned, files_new, files_updated, files_skipped, errors
    - Update device last_sync_at timestamp
    - Return sync summary
- [ ] `POST /sync/garmin-express/{device_id}/sync` endpoint
  - Trigger manual sync
  - Return progress summary
- [ ] Error handling
  - Store errors in imported_files.last_error
  - Continue processing other files
  - Return error summary to user

**Windows Support**
- [ ] Add Windows path detection to `detect_garmin_devices()`
  - Search: `%APPDATA%\Garmin\Devices\`
  - Same logic as macOS
- [ ] Test on Windows machine (or VM)

**Acceptance Criteria:**
- [ ] Sync only processes new/changed files
- [ ] Deduplication works correctly
- [ ] Sync completes in <10 seconds for typical device (100-200 new files)
- [ ] Errors don't block entire sync
- [ ] Works on both macOS and Windows

---

### Week 4: Visualization

**Plotly Integration**
- [ ] Install plotly.js-dist
  ```bash
  cd frontend
  npm install plotly.js-dist
  ```

**Chart Components**
- [ ] `frontend/src/lib/components/TimeSeriesChart.svelte`
  - Props: `data: {date: string, value: number}[]`, `title: string`, `yAxisLabel: string`
  - Render line chart with Plotly
  - Add 7-day rolling average (dashed line)
  - Interactive (zoom, pan, hover)
  - Port pattern from FOLDLINE_HANDOFF.md lines 1108-1171
  - Dark/light theme support

- [ ] `frontend/src/lib/components/HeatmapChart.svelte`
  - Props: `data: {date: string, value: number}[]`, `title: string`, `colorScale: string`
  - Render calendar heatmap
  - Color intensity by value
  - Hover shows exact value
  - Port pattern from FOLDLINE_HANDOFF.md lines 1173-1200
  - Dark/light theme support

**Page Integration**
- [ ] Update `frontend/src/routes/heatmaps/+page.svelte`
  - Remove stub text
  - Add metric selector (sleep, HRV, stress, steps)
  - Fetch data from `/metrics/heatmap`
  - Render HeatmapChart component
  - Add date range picker

- [ ] Update `frontend/src/routes/trends/+page.svelte`
  - Remove stub text
  - Add metric selector
  - Fetch data from `/metrics/timeseries`
  - Render TimeSeriesChart component
  - Add date range picker

**Acceptance Criteria:**
- [ ] Charts render in <1 second
- [ ] Charts are interactive (zoom, pan, hover)
- [ ] Dark/light theme toggle works
- [ ] Date range filtering works
- [ ] Empty state handled gracefully

---

### Week 5: Basic Analytics

**Metric Query Implementation**

- [ ] `backend/metrics/sleep.py::get_sleep_heatmap()`
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

- [ ] `backend/metrics/sleep.py::get_sleep_timeseries()`
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

- [ ] `backend/metrics/hrv.py::get_hrv_heatmap()`
  ```python
  def get_hrv_heatmap(db_connection, start_date, end_date):
      query = """
          SELECT date, hrv_value as value
          FROM hrv_records
          WHERE date BETWEEN ? AND ?
          ORDER BY date
      """
      return execute_query(query, [start_date, end_date])
  ```

- [ ] `backend/metrics/stress.py::get_stress_heatmap()`
  ```python
  def get_stress_heatmap(db_connection, start_date, end_date):
      query = """
          SELECT date, avg_stress as value
          FROM daily_stress
          WHERE date BETWEEN ? AND ?
          ORDER BY date
      """
      return execute_query(query, [start_date, end_date])
  ```

- [ ] `backend/metrics/steps.py::get_steps_heatmap()`
  ```python
  def get_steps_heatmap(db_connection, start_date, end_date):
      query = """
          SELECT date, step_count as value
          FROM daily_steps
          WHERE date BETWEEN ? AND ?
          ORDER BY date
      """
      return execute_query(query, [start_date, end_date])
  ```

**Dashboard Endpoint**
- [ ] Create `GET /analytics/dashboard` endpoint
  ```python
  {
      "date_range": {"start": "2024-01-01", "end": "2024-12-31"},
      "total_days": 365,
      "metrics": {
          "sleep": {
              "avg_hours": 7.2,
              "data_completeness": 98  # % of days with data
          },
          "hrv": {
              "avg_value": 45,
              "data_completeness": 95
          },
          "stress": {
              "avg_value": 35,
              "data_completeness": 92
          },
          "steps": {
              "avg_count": 8500,
              "data_completeness": 97
          }
      }
  }
  ```

- [ ] Update `frontend/src/routes/dashboard/+page.svelte`
  - Fetch dashboard data
  - Display metric cards with averages
  - Show data completeness indicators
  - Add "Last Synced" timestamp

**Acceptance Criteria:**
- [ ] All metric queries return real data (not [])
- [ ] Queries complete in <500ms
- [ ] Dashboard loads in <1 second
- [ ] Empty states handled gracefully

---

### Week 5-6: Settings UI & Sync Controls

**Settings Page Enhancement**
- [ ] Update `frontend/src/routes/settings/+page.svelte`

**Garmin Express Device Management**
- [ ] Add "Garmin Express Devices" section
  - List detected devices
  - Device name, last sync time, file count
  - Enable/disable toggle per device
  - "Detect Devices" button (re-scan)
  - "Sync Now" button per device
  - Status indicator (syncing, success, error)

**Sync Settings**
- [ ] Add "Sync Settings" section
  - "Sync on startup" toggle (store in config table)
  - "Last sync" timestamp display
  - Link to sync error logs (if any)

**GDPR Import UI**
- [ ] Add "Import Historical Data" section
  - "Upload GDPR Export" button
  - File picker (ZIP only)
  - Progress bar during import
  - Summary of imported records
  - Error display if import fails

**Acceptance Criteria:**
- [ ] Users can enable/disable devices
- [ ] "Sync Now" button triggers sync and shows progress
- [ ] Sync errors displayed clearly
- [ ] GDPR import progress visible
- [ ] Settings persist across app restarts

---

### Week 6: Polish & Beta Testing

**Error Handling**
- [ ] Add loading states to all API calls
- [ ] Add error boundaries to Svelte components
- [ ] Display user-friendly error messages
- [ ] Add retry logic for failed syncs

**Performance Optimization**
- [ ] Add database indexes if queries slow
- [ ] Implement query result caching (if needed)
- [ ] Optimize FIT parsing for large files

**Documentation**
- [ ] Update README with:
  - Pre-commercial MVP status
  - Setup instructions
  - Garmin Express requirement
  - GDPR export instructions
  - Known limitations
- [ ] Create BETA_TESTING.md
  - How to become a beta tester
  - What to test
  - How to report bugs
  - What's coming in commercial launch

**Beta Testing**
- [ ] Deploy to test users (3-5 people)
- [ ] Collect feedback
- [ ] Fix critical bugs
- [ ] Iterate on UX issues

**Acceptance Criteria:**
- [ ] App starts successfully on fresh install
- [ ] GDPR import works for beta testers
- [ ] Garmin Express sync works for beta testers
- [ ] Visualizations render correctly
- [ ] No critical bugs reported
- [ ] Users understand how to use the app

---

## Technical Architecture Decisions

### 1. Database Schema: Enhanced `imported_files`

**Decision:** Enhance existing table rather than create new `file_registry`

**Implementation:**
```sql
-- Run migration
ALTER TABLE imported_files ADD COLUMN file_size BIGINT;
ALTER TABLE imported_files ADD COLUMN modified_time TIMESTAMP;
ALTER TABLE imported_files ADD COLUMN first_seen_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;
ALTER TABLE imported_files ADD COLUMN source TEXT DEFAULT 'manual';
ALTER TABLE imported_files ADD COLUMN last_error TEXT;

-- Update existing records
UPDATE imported_files SET source = 'manual' WHERE source IS NULL;
```

**Rationale:**
- Simpler than creating new table + migration
- Existing deduplication logic works
- Can add indexes as needed

### 2. Garmin Express Platform Priority

**Decision:** Implement macOS first (Week 2), Windows second (Week 3)

**Rationale:**
- Faster to validate on single platform
- Can test on developer machine
- Windows support follows same pattern

**Paths:**
- macOS: `~/Library/Application Support/Garmin/Devices/<DEVICE-ID>/`
- Windows: `%APPDATA%\Garmin\Devices\<DEVICE-ID>\`

### 3. Sync Triggering

**Decision:** Manual "Sync Now" + Optional "Sync on Startup"

**Implementation:**
- Settings page has "Sync on Startup" toggle
- Stored in `config` table
- On app launch, check config and sync if enabled
- Settings page has "Sync Now" button per device
- Sync button shows progress indicator

**Rationale:**
- User control (manual sync)
- Convenience (optional automatic)
- No background processes (privacy-preserving)

### 4. GDPR Import Priority

**Decision:** Keep GDPR import, implement first (Week 1)

**Rationale:**
- Users need historical data (Garmin Express only keeps recent months)
- One-time bulk import vs. ongoing incremental sync
- Different use cases, both needed

### 5. Visualization Library

**Decision:** Use Plotly (as recommended by INTEGRATION_PLAN.md)

**Rationale:**
- Battle-tested in gar-mining (4,900 lines of code)
- Copy-paste examples from FOLDLINE_HANDOFF.md
- Interactive by default
- Works in both web and desktop

### 6. Analytics Scope

**Decision:** Basic metric queries only (no advanced analytics)

**What's Included:**
- Sleep heatmap/timeseries
- HRV heatmap
- Stress heatmap
- Steps heatmap
- Basic dashboard summary

**What's Deferred (Post-Commercial):**
- Health Score algorithm
- Recovery Detection
- Correlation Analysis
- Stress Pattern Analysis
- Sleep-Activity Correlation
- Optimal Activity Range

**Rationale:**
- Users need to see their data first
- Advanced analytics can wait until post-commercial
- Simpler MVP = faster validation

---

## Privacy & Security Guarantees

Per CONTINUAL_SYNC_SPEC.md §10:

- ✅ Foldline **never touches the cloud**
- ✅ Foldline **never uses Garmin APIs**
- ✅ No telemetry
- ✅ No analytics
- ✅ No data leaves the machine
- ✅ All sync paths are **read-only** (never write to Garmin Express folders)
- ✅ All ingestion is local

---

## Post-Pre-Commercial Roadmap

### Commercial Launch Preparation (Weeks 7-10)

**Payment System** (from payment_planning.md)
- [ ] Lemon Squeezy integration
- [ ] License activation UI
- [ ] EFF donation tracking (10% net revenue)
- [ ] Marketing site "Buy Foldline" flow
- [ ] Download hosting

**Marketing Site Polish**
- [ ] Screenshots from beta testing
- [ ] User testimonials
- [ ] Privacy-first messaging
- [ ] Clear value proposition

**Commercial Launch Checklist**
- [ ] Payment flow tested end-to-end
- [ ] License activation works offline
- [ ] Marketing site live
- [ ] Support email set up
- [ ] First 10 paying customers

### Post-Launch Iterations (Months 2-6)

**Phase 1: Advanced Analytics** (Months 2-3)
- Port Health Score algorithm
- Implement Recovery Detection
- Add Correlation Analysis
- Create advanced dashboard

**Phase 2: Power User Features** (Months 4-6)
- Stress Pattern Analysis
- Sleep-Activity Correlation
- Optimal Activity Range
- Schema enhancements (raw_data, HR timeseries)

**Phase 3: Advanced Features** (Months 7-12)
- Annotations system
- Predictive models
- Watched folders sync mode
- Manual folder re-import mode
- Flexible time windows
- Relationship explorer

---

## Success Metrics

### Pre-Commercial MVP Goals

**Technical:**
- [ ] GDPR import success rate >95%
- [ ] Garmin Express sync works on macOS and Windows
- [ ] App startup time <3 seconds
- [ ] All tests passing
- [ ] Works completely offline

**User Experience:**
- [ ] Users can complete setup in <10 minutes
- [ ] Sync completes in <30 seconds for typical device
- [ ] Visualizations render in <1 second
- [ ] Clear error messages for all failure modes
- [ ] No data leaves user's machine (validated)

**Beta Testing:**
- [ ] 5+ beta testers using app daily
- [ ] Positive feedback on core UX
- [ ] <3 critical bugs reported
- [ ] Users understand sync workflow
- [ ] Clear path to commercial launch

### Commercial Launch Goals

**Technical:**
- [ ] Payment system works end-to-end
- [ ] License activation <5 seconds
- [ ] Works on Windows, macOS, Linux

**Business:**
- [ ] Checkout conversion rate >50%
- [ ] First 10 paying customers
- [ ] Zero refund requests due to bugs
- [ ] Positive user feedback

---

## Key Files to Implement

### Backend (Python/FastAPI)

**New Files:**
```
backend/sync/
├── __init__.py
├── garmin_express.py         # Device detection
├── sync_engine.py             # Incremental sync logic
└── config.py                  # Sync configuration

backend/ingestion/
├── field_mappings.py          # GDPR → Foldline schema mappings
└── garmin_gdpr.py             # Complete implementation (currently stubbed)

backend/analytics/
└── (future - post-commercial)
```

**Enhanced Files:**
```
backend/ingestion/fit_folder.py   # Add incremental sync support
backend/ingestion/json_parser.py  # Add GDPR JSON parsing
backend/metrics/sleep.py          # Implement get_sleep_heatmap/timeseries
backend/metrics/hrv.py            # Implement get_hrv_heatmap
backend/metrics/stress.py         # Implement get_stress_heatmap
backend/metrics/steps.py          # Implement get_steps_heatmap
backend/main.py                   # Add sync endpoints
```

### Frontend (SvelteKit)

**New Files:**
```
frontend/src/lib/components/
├── TimeSeriesChart.svelte
├── HeatmapChart.svelte
└── SyncStatus.svelte           # Sync progress indicator

frontend/src/lib/stores/
└── syncStore.ts                 # Sync state management
```

**Enhanced Files:**
```
frontend/src/routes/settings/+page.svelte    # Add Garmin Express device management
frontend/src/routes/heatmaps/+page.svelte    # Add chart components
frontend/src/routes/trends/+page.svelte      # Add chart components
frontend/src/routes/dashboard/+page.svelte   # Add metric cards
```

### Database

**Migration:**
```
backend/db/migrations/
└── 001_add_sync_fields.sql      # ALTER TABLE imported_files...
```

**New Tables:**
```sql
CREATE TABLE IF NOT EXISTS garmin_express_devices (
    device_id TEXT PRIMARY KEY,
    device_path TEXT NOT NULL,
    device_name TEXT,
    enabled BOOLEAN DEFAULT TRUE,
    last_sync_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## Risk Assessment

### High Risk Items

**1. Garmin Express Compatibility**
- **Risk:** Garmin Express folder structure varies by version, OS, device
- **Mitigation:**
  - Test with multiple Garmin devices
  - Handle missing folders gracefully
  - Fallback to manual import if Express not found
  - Document known limitations

**2. GDPR Export Variability**
- **Risk:** GDPR exports vary by user, device, export date
- **Mitigation:**
  - Test with multiple real exports (from beta testers)
  - Robust error handling per CONTINUAL_SYNC_SPEC §7.2
  - Field name fallback patterns
  - Display clear import summary with errors

**3. Cross-Platform File Path Handling**
- **Risk:** Platform-specific path differences (macOS vs. Windows)
- **Mitigation:**
  - Use `pathlib` for cross-platform paths
  - Test on both platforms
  - Handle edge cases (network drives, symlinks)

### Medium Risk Items

**1. Sync Performance**
- **Risk:** Large device folders (10,000+ files) slow to scan
- **Mitigation:**
  - Use file modified_time filtering
  - Index database queries
  - Show progress indicator
  - Allow cancellation

**2. Database Migration**
- **Risk:** Altering production schema breaks existing installs
- **Mitigation:**
  - Test migration on copy of database first
  - Add columns with defaults (no data loss)
  - Version check before migration
  - Backup before migration

### Low Risk Items

**1. Visualization Performance**
- Easy to optimize with downsampling
- Plotly handles large datasets well

**2. Settings Persistence**
- `config` table already exists
- Simple key-value storage

---

## Integration with Existing Docs

### How This Relates to Other Planning Docs

**CONTINUAL_SYNC_SPEC.md**
- ✅ **Implemented:** Sections 2-10 (Garmin Express sync, deduplication, ingestion pipeline, UX requirements, privacy guarantees)
- ⏭️ **Deferred:** Mode 3 (Watched Folders) - post-commercial
- ⏭️ **Deferred:** Section 11 (Future Extensions) - post-commercial

**INTEGRATION_ROADMAP.md**
- ✅ **Implemented:** Weeks 2-6 (Data Import, Visualization, Analytics)
- ⏭️ **Deferred:** Week 1-2 (Payment) - moved to post-pre-commercial
- ⏭️ **Deferred:** Post-MVP phases - moved to post-commercial

**INTEGRATION_PLAN.md**
- ✅ **Implemented:** Phase 2 (Visualization - basic)
- ✅ **Implemented:** Phase 3 (GDPR Import)
- 🟨 **Partially Implemented:** Phase 1 (Analytics - basic queries only)
- ⏭️ **Deferred:** Phase 1 (Advanced analytics) - post-commercial
- ⏭️ **Deferred:** Phase 4 (Schema Enhancements) - raw_data columns deferred
- ⏭️ **Deferred:** Phase 5 (Advanced Analytics) - post-commercial
- ⏭️ **Deferred:** Phase 6 (Future Features) - post-commercial

**payment_planning.md**
- ⏭️ **Deferred:** All tasks 1-8 - moved to commercial launch preparation

---

## Next Actions

### This Week (Week 1)

**Monday-Tuesday:**
- [ ] Create database migration script
- [ ] Run migration on dev database
- [ ] Update tests to handle new schema

**Wednesday-Thursday:**
- [ ] Implement `extract_garmin_export()` in garmin_gdpr.py
- [ ] Implement field mappings in field_mappings.py
- [ ] Test ZIP extraction with sample export

**Friday:**
- [ ] Implement `process_gdpr_export()` pipeline
- [ ] Test with real GDPR export
- [ ] Fix any parsing errors

### Next Week (Week 2)

**Focus:** Garmin Express detection (macOS)

### Following Weeks

**Week 3:** Garmin Express sync + Windows support
**Week 4:** Visualization
**Week 5:** Basic Analytics
**Week 6:** Polish & Beta Testing

---

**Status:** Ready to begin implementation
**First Task:** Database schema migration
**First Deliverable:** GDPR import working end-to-end
