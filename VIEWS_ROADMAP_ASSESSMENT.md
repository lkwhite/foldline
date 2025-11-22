# Software and Data Views Assessment

**Date:** 2025-11-22
**Status:** Pre-Commercial MVP Development (Week 1 of 5-6)
**Assessment By:** Claude Code

---

## Executive Summary

Foldline has a **solid architectural foundation** for data visualization views, with clear planning and well-defined scope. However, the visualization layer is currently **incomplete** - the UI framework exists but lacks actual chart rendering. The roadmap prioritizes completing this in Week 4 of the pre-commercial MVP timeline.

### Current State: 🟨 **Foundation Complete, Visualization Pending**

- ✅ **Database schema**: Fully implemented with comprehensive health metrics tables
- ✅ **Frontend routing**: All 5 view pages exist with functional UI controls
- ✅ **API endpoints**: Created but return stub data
- ✅ **Backend logic**: Module structure exists but queries are not implemented
- ❌ **Visualization**: No chart libraries integrated (planned for Week 4)
- ❌ **Real data queries**: All metric functions return empty arrays (planned for Week 5)

---

## 1. View Inventory & Feature Set

### 1.1 Implemented Views

Foldline provides **four primary data visualization views** and one settings view:

| View | Route | Purpose | UI Status | Data Status | Visualization Status |
|------|-------|---------|-----------|-------------|---------------------|
| **Dashboard** | `/dashboard` | Overview & summary stats | ✅ Complete | ✅ Working | ✅ Complete |
| **Heatmaps** | `/heatmaps` | Calendar-style year view | ✅ Complete | 🟨 Stub API | ❌ No charts |
| **Trends** | `/trends` | Time series line charts | ✅ Complete | 🟨 Stub API | ❌ No charts |
| **Correlation** | `/correlation` | Scatter plots & statistics | ✅ Complete | 🟨 Stub API | ❌ No charts |
| **Settings** | `/settings` | Data source management | 🟨 Partial | ✅ Working | N/A |

### 1.2 Supported Metrics

The system supports **6 core health metrics** from Garmin devices:

1. **Sleep Duration** - Hours of sleep per night (`sleep_records` table)
2. **Resting Heart Rate** - Daily resting HR (`resting_hr` table)
3. **Heart Rate Variability (HRV)** - Daily HRV values (`hrv_records` table)
4. **Stress** - Average daily stress (0-100 scale, `daily_stress` table)
5. **Steps** - Daily step count (`daily_steps` table)
6. **Training Load** - Activity-based metric (`activities` table)

### 1.3 Additional Data Available (Not Yet Visualized)

The database schema includes **extensive additional metrics** not yet exposed in views:

- Sleep stages breakdown (deep/light/REM/awake)
- Respiration rate, SpO2, body battery
- Activity details (type, duration, average HR, calories)
- Fitness assessments (VO2 max, fitness age)
- Intensity minutes, floors climbed, hydration
- Body composition, menstrual cycles

**Opportunity:** These metrics can be added to views post-MVP without database changes.

---

## 2. Current Implementation Status

### 2.1 What's Working ✅

**Dashboard View** (`/dashboard`)
- Displays database status and initialization state
- Shows date range of available data
- Counts: sleep records, activities, days with data
- Lists available metrics
- **File:** `frontend/src/routes/dashboard/+page.svelte:1-119`

**Database Schema**
- 15+ tables covering all major Garmin health metrics
- SQL view `daily_metrics` aggregating core metrics
- Proper indexing on date fields
- **File:** `backend/db/schema.sql:1-340`

**API Infrastructure**
- FastAPI backend with CORS enabled
- Endpoint structure defined for all metric types
- Error handling framework in place
- **File:** `backend/main.py:1-200`

### 2.2 What's Stubbed 🟨

**Heatmap View** (`/heatmaps`)
- ✅ UI controls: metric selector (5 metrics), date range picker, load button
- ✅ API integration: `GET /metrics/heatmap` endpoint called successfully
- ❌ Visualization: Shows "TODO: Add actual heatmap visualization"
- ❌ Returns JSON preview instead of chart
- **File:** `frontend/src/routes/heatmaps/+page.svelte:69`

**Trends View** (`/trends`)
- ✅ UI controls: metric selector, date range picker
- ✅ API integration: `GET /metrics/timeseries` endpoint
- ❌ Visualization: No line chart component
- ❌ Rolling average calculation not implemented
- **File:** `frontend/src/routes/trends/+page.svelte:1-100`

**Correlation View** (`/correlation`)
- ✅ UI controls: X/Y metric selectors, lag days parameter
- ✅ Statistics display: Pearson & Spearman correlation placeholders
- ❌ Visualization: No scatter plot
- ❌ Correlation algorithm returns hardcoded values
- **File:** `frontend/src/routes/correlation/+page.svelte:1-150`

**Backend Metric Queries**
- All functions in `backend/metrics/` return empty arrays:
  - `sleep.py::get_sleep_heatmap()` → `return []` (line 31)
  - `sleep.py::get_sleep_timeseries()` → `return []` (line 55)
  - `hrv.py::get_hrv_heatmap()` → `return []`
  - `stress.py::get_stress_heatmap()` → `return []`
  - `steps.py::get_steps_heatmap()` → `return []`

**Settings View** (`/settings`)
- ✅ Data root directory selector
- ✅ Database status display
- ❌ Garmin Express device management (planned Week 5-6)
- ❌ GDPR import UI (planned Week 5-6)
- ❌ Sync controls (planned Week 5-6)

### 2.3 What's Missing ❌

**Critical for MVP:**
1. **Plotly.js integration** - No visualization library installed
2. **Chart components** - `TimeSeriesChart.svelte` and `HeatmapChart.svelte` don't exist
3. **Real data queries** - All metric functions need SQL implementation
4. **Rolling averages** - Time series smoothing not implemented
5. **Correlation algorithms** - Pearson/Spearman calculations missing

**Post-MVP (Advanced Analytics):**
6. Health Score composite metric
7. Recovery detection algorithm
8. Stress pattern analysis
9. Sleep-activity correlation analysis
10. Optimal activity range detection

---

## 3. Roadmap & Timeline

### 3.1 Pre-Commercial MVP Plan (5-6 Weeks)

Based on `PRE_COMMERCIAL_MVP_PLAN.md`, views are addressed in **Weeks 4-5**:

#### **Week 1: Foundation & GDPR Import** (Current Week)
- ✅ Database schema complete
- 🟨 GDPR import implementation in progress
- Focus: Data ingestion, not visualization

#### **Week 2: Garmin Express Detection (macOS)**
- Detect Garmin devices on macOS
- Create device registry
- Foundation for auto-sync

#### **Week 3: Garmin Express Sync + Windows**
- Incremental sync algorithm
- Windows platform support
- Deduplication logic

#### **Week 4: Visualization** 🎯 **← VIEWS IMPLEMENTATION**
**Tasks:**
- [ ] Install `plotly.js-dist` package
- [ ] Create `TimeSeriesChart.svelte` component
  - Line chart with 7-day rolling average
  - Interactive (zoom, pan, hover)
  - Dark/light theme support
- [ ] Create `HeatmapChart.svelte` component
  - Calendar heatmap layout
  - Color intensity by value
  - Hover tooltips
- [ ] Update `/heatmaps` page to use HeatmapChart
- [ ] Update `/trends` page to use TimeSeriesChart
- [ ] Add date range filtering with URL persistence
- [ ] Implement theme toggle

**Acceptance Criteria:**
- Charts render in <1 second
- Interactive features work (zoom, pan, hover)
- Theme switching functional
- Empty states handled gracefully

**Reference:** Copy-paste Plotly examples from `FOLDLINE_HANDOFF.md:1095-1380`

#### **Week 5: Basic Analytics** 🎯 **← DATA QUERIES**
**Tasks:**
- [ ] Implement `get_sleep_heatmap()` with SQL query (lines 233-242)
- [ ] Implement `get_sleep_timeseries()` with 7-day rolling average (lines 244-260)
- [ ] Implement `get_hrv_heatmap()` (lines 262-272)
- [ ] Implement `get_stress_heatmap()` (lines 274-284)
- [ ] Implement `get_steps_heatmap()` (lines 286-296)
- [ ] Create `GET /analytics/dashboard` endpoint with aggregate stats
- [ ] Update dashboard with metric cards and data completeness indicators

**Acceptance Criteria:**
- All queries return real data (not empty arrays)
- Query performance <500ms
- Dashboard loads in <1 second

#### **Week 5-6: Settings UI & Sync Controls**
- Garmin Express device management UI
- "Sync Now" button per device
- GDPR import file upload interface
- Sync error displays

#### **Week 6: Polish & Beta Testing**
- Error handling and loading states
- Performance optimization
- Beta user deployment
- Bug fixes

### 3.2 Post-MVP Roadmap (Months 2-12)

**Phase 1: Advanced Analytics** (Months 2-3)
- Health Score algorithm (weighted: sleep + stress + HR recovery)
- Recovery Detection (composite scoring)
- Correlation Analysis (Pearson + Spearman)
- Advanced dashboard enhancements

**Phase 2: Power User Features** (Months 4-6)
- Stress Pattern Analysis (day-of-week patterns)
- Sleep-Activity Correlation (bidirectional with lags)
- Optimal Activity Range (quartile analysis)
- Schema enhancements (raw_data columns, HR timeseries table)

**Phase 3: Advanced Features** (Months 7-12)
- Annotations system (manual notes on dates)
- Predictive models (forecast sleep quality)
- Watched folders sync mode
- Relationship explorer (multi-metric analysis)

---

## 4. Gap Analysis

### 4.1 Critical Gaps (Blocking MVP Launch)

| Gap | Impact | Planned Fix | Timeline |
|-----|--------|-------------|----------|
| **No visualization library** | Users can't see charts | Install Plotly.js | Week 4, Day 1 |
| **No chart components** | No reusable visualization | Create Svelte components | Week 4, Days 2-3 |
| **Stub data queries** | Charts would be empty | Implement SQL queries | Week 5 |
| **No rolling averages** | Trends less useful | SQL window functions | Week 5 |
| **No Garmin Express sync UI** | Poor UX for ongoing use | Settings page enhancement | Week 5-6 |

### 4.2 High-Value Enhancements (Post-MVP)

| Enhancement | Value | Complexity | Priority |
|-------------|-------|------------|----------|
| **Health Score** | Unified metric, easy to track | Medium | High |
| **Recovery Detection** | Actionable insights | Medium | High |
| **Correlation Analysis** | Discover patterns | Low-Medium | High |
| **Sleep stage visualization** | Richer sleep insights | Low | Medium |
| **Activity type breakdown** | Better activity tracking | Low | Medium |
| **Annotations** | User context on data | Medium | Medium |
| **Predictive models** | Future-looking insights | High | Low |

### 4.3 Technical Debt

1. **Test coverage**: Visualization components will need integration tests
2. **Performance**: Large datasets (5+ years) may need downsampling
3. **Mobile responsiveness**: Charts may not be optimized for small screens
4. **Accessibility**: Chart components need ARIA labels and keyboard navigation

---

## 5. Architecture & Design Decisions

### 5.1 Visualization Library: Plotly.js

**Decision:** Use Plotly.js for all charts
**Rationale:**
- Battle-tested in gar-mining project (4,900 lines of production code)
- Interactive by default (zoom, pan, hover)
- Works in both web and desktop (Tauri)
- Copy-paste examples available in `FOLDLINE_HANDOFF.md`

**Alternatives Considered:**
- D3.js: Too low-level, requires custom code
- Chart.js: Less interactive features
- Recharts: React-specific (project uses Svelte)

### 5.2 Data Query Strategy

**Decision:** Simple SQL queries first, advanced algorithms later
**Week 5 Approach:**
```sql
-- Example: Sleep heatmap (simple)
SELECT date, duration_minutes / 60.0 as value
FROM sleep_records
WHERE date BETWEEN ? AND ?
ORDER BY date
```

**Post-MVP Approach:**
```python
# Example: Health Score (complex)
health_score = (
    0.3 * sleep_quality_normalized +
    0.3 * (100 - stress_normalized) +
    0.2 * hrv_normalized +
    0.2 * recovery_index
)
```

**Rationale:**
- Users need to see their data first
- Advanced analytics can wait until post-MVP
- Simpler implementation = faster validation

### 5.3 Frontend State Management

**Current:** Local component state
**Planned:** Svelte stores for sync status (Week 5-6)
**Future:** Consider context API for theme management

### 5.4 Performance Considerations

**Date Range Filtering:**
- Default to last 365 days
- URL parameters for persistence
- Backend pagination for large datasets

**Chart Rendering:**
- Plotly built-in downsampling for >10,000 points
- Lazy loading for dashboard cards
- Debounced date range updates

---

## 6. Key Files Reference

### 6.1 Frontend Views

| File | Lines | Status | Next Action |
|------|-------|--------|-------------|
| `frontend/src/routes/dashboard/+page.svelte` | 119 | ✅ Complete | Enhance with metric cards (Week 5) |
| `frontend/src/routes/heatmaps/+page.svelte` | 123 | 🟨 UI only | Add HeatmapChart component (Week 4) |
| `frontend/src/routes/trends/+page.svelte` | 100 | 🟨 UI only | Add TimeSeriesChart component (Week 4) |
| `frontend/src/routes/correlation/+page.svelte` | 150 | 🟨 UI only | Add scatter plot (Week 4) |
| `frontend/src/routes/settings/+page.svelte` | 80 | 🟨 Partial | Add device management (Week 5-6) |

### 6.2 Backend Metrics

| File | Functions | Status | Next Action |
|------|-----------|--------|-------------|
| `backend/metrics/sleep.py` | 3 | ❌ Stubbed | Implement SQL queries (Week 5) |
| `backend/metrics/hrv.py` | 2 | ❌ Stubbed | Implement SQL queries (Week 5) |
| `backend/metrics/stress.py` | 1 | ❌ Stubbed | Implement SQL queries (Week 5) |
| `backend/metrics/steps.py` | 1 | ❌ Stubbed | Implement SQL queries (Week 5) |

### 6.3 API Endpoints

| Endpoint | File | Line | Status |
|----------|------|------|--------|
| `GET /metrics/heatmap` | `backend/main.py` | ~150 | 🟨 Returns stub data |
| `GET /metrics/timeseries` | `backend/main.py` | ~165 | 🟨 Returns stub data |
| `GET /metrics/correlation` | `backend/main.py` | ~180 | 🟨 Returns stub data |
| `GET /status` | `backend/main.py` | ~50 | ✅ Working |

### 6.4 Database Schema

| Table/View | Rows | Purpose | Status |
|------------|------|---------|--------|
| `sleep_records` | Schema | Sleep duration and quality | ✅ Complete |
| `resting_hr` | Schema | Daily resting heart rate | ✅ Complete |
| `hrv_records` | Schema | Heart rate variability | ✅ Complete |
| `daily_stress` | Schema | Stress levels | ✅ Complete |
| `daily_steps` | Schema | Step count | ✅ Complete |
| `daily_metrics` (view) | Schema | Aggregated metrics | ✅ Complete |

**File:** `backend/db/schema.sql:322-340` (SQL view definition)

### 6.5 Planning Documents

| Document | Purpose | Status |
|----------|---------|--------|
| `PRE_COMMERCIAL_MVP_PLAN.md` | 5-6 week roadmap | 🟢 Active |
| `CONTINUAL_SYNC_SPEC.md` | Sync architecture | 🟢 Active |
| `FOLDLINE_HANDOFF.md` | Algorithm & viz examples | 🟢 Reference |
| `TESTING_PLAN.md` | Testing strategy | 🟢 Active |
| `docs/archive/INTEGRATION_PLAN.md` | Original roadmap | 🔴 Archived |

---

## 7. Risk Assessment

### 7.1 Visualization Implementation Risks

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| **Plotly.js bundle size too large** | Low | Medium | Use `plotly.js-dist-min` for production |
| **Chart performance on large datasets** | Medium | High | Implement downsampling, date range limits |
| **Theme switching breaks charts** | Low | Low | Test both themes in Week 4 |
| **Mobile responsiveness issues** | Medium | Medium | Defer mobile optimization to post-MVP |

### 7.2 Data Query Risks

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| **Slow queries on 5+ years of data** | Medium | High | Add database indexes, limit default range |
| **Missing data causes chart gaps** | High | Low | Handle nulls gracefully, show empty state |
| **Correlation calculations timeout** | Low | Medium | Limit to 1-year max for correlations |

### 7.3 Schedule Risks

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| **Week 4 visualization delayed** | Medium | High | Start Plotly integration early, use simple examples first |
| **Complex analytics slip to Week 6** | High | Low | Keep Week 5 scope minimal (basic queries only) |
| **Beta testing finds critical bugs** | Medium | Medium | Week 6 buffer for fixes, limit beta user count |

---

## 8. Recommendations

### 8.1 Immediate Actions (Week 1)

1. **Validate Plotly.js integration** (1-2 hours)
   - Install `plotly.js-dist` in a branch
   - Create minimal proof-of-concept chart
   - Test theme switching and responsiveness
   - **Why:** De-risk Week 4 implementation

2. **Review FOLDLINE_HANDOFF.md visualization examples** (1 hour)
   - Identify copy-paste candidates
   - Note any missing dependencies
   - **Why:** Reduce Week 4 development time

3. **Prioritize SQL query implementation order** (30 minutes)
   - Start with sleep (most important metric)
   - Then HRV, stress, steps
   - Save correlations for last
   - **Why:** Ensure most valuable views work first

### 8.2 Week 4 Success Factors

1. **Start with simplest chart type first**
   - Implement TimeSeriesChart before HeatmapChart
   - Single metric, single color, no interactivity
   - Add features incrementally

2. **Use real (but limited) data for testing**
   - Query 30 days max during development
   - Expand to full range after performance validation

3. **Create reusable chart wrapper component**
   - Handles loading states
   - Displays errors gracefully
   - Consistent theme application

### 8.3 Week 5 Success Factors

1. **Use SQL window functions for rolling averages**
   ```sql
   AVG(value) OVER (ORDER BY date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW)
   ```
   - Built into SQLite 3.25+ (verify version)
   - Faster than application-layer calculation

2. **Add query result caching**
   - Cache common date ranges (last 30/90/365 days)
   - Invalidate on new data sync
   - **Benefit:** Dashboard loads faster

3. **Monitor query performance from day 1**
   - Log slow queries (>500ms)
   - Add indexes proactively
   - **Tools:** SQLite EXPLAIN QUERY PLAN

### 8.4 Post-MVP Enhancements (Priority Order)

1. **Health Score** (Months 2-3)
   - High user value (single number to track)
   - Medium complexity (weighted average)
   - Algorithm exists in `FOLDLINE_HANDOFF.md:744-2612`

2. **Recovery Detection** (Months 2-3)
   - Actionable insights (when to rest)
   - Uses existing metrics (HR, sleep, stress)
   - No new data collection needed

3. **Sleep Stage Visualization** (Months 3-4)
   - Data already in database (`sleep_detailed` table)
   - Low complexity (stacked area chart)
   - Richer sleep insights

4. **Correlation Analysis** (Months 3-4)
   - Discover patterns (sleep vs. stress)
   - UI already built, needs backend logic
   - Pearson/Spearman straightforward

### 8.5 Long-Term Considerations

1. **Mobile app** (6-12 months post-launch)
   - Consider responsive charts from day 1
   - Test on mobile browsers during Week 6

2. **Data export** (Post-MVP)
   - Allow users to download chart data (CSV)
   - Useful for power users and data portability

3. **Custom metrics** (12+ months)
   - User-defined calculated metrics
   - Requires schema changes and UI builder

---

## 9. Success Metrics

### 9.1 Week 4 Goals (Visualization)

- [ ] Plotly.js integrated and rendering charts in <1 second
- [ ] Heatmap view shows calendar-style visualization for all 5 metrics
- [ ] Trends view shows line charts with 7-day rolling average
- [ ] Theme switching works without page reload
- [ ] Date range filtering updates charts dynamically
- [ ] Empty states displayed when no data available

### 9.2 Week 5 Goals (Analytics)

- [ ] All metric queries return real data from database
- [ ] Query performance <500ms for 1-year date range
- [ ] Dashboard displays accurate aggregate statistics
- [ ] Data completeness indicators show % of days with data
- [ ] Rolling averages calculated correctly (verified against sample data)

### 9.3 Beta Testing Goals (Week 6)

- [ ] 5+ beta users successfully load visualizations
- [ ] Average chart render time <1 second (measured)
- [ ] Zero "unable to display data" errors for users with data
- [ ] <3 critical bugs reported related to views
- [ ] Positive feedback on visualization clarity and usefulness

### 9.4 Commercial Launch Goals

- [ ] All 4 visualization views production-ready
- [ ] Performance acceptable on 5+ years of data
- [ ] Mobile browser experience functional (not necessarily optimal)
- [ ] Analytics queries optimized with appropriate indexes
- [ ] User documentation covers all view features

---

## 10. Conclusion

### Current State Summary

Foldline's views architecture is **well-designed and properly scoped**, with a clear separation between pre-commercial MVP (basic visualization) and post-launch advanced analytics. The **foundation is solid** - database schema, API structure, and UI controls are all in place.

The **primary gap** is the lack of actual chart rendering and data queries, both intentionally deferred to Weeks 4-5 of the MVP plan. This is a **reasonable prioritization**, as data ingestion (Weeks 1-3) must work before visualization is useful.

### Readiness Assessment

**For Week 4 (Visualization):**
- 🟢 **Ready:** Database schema, API endpoints, UI controls
- 🟨 **Needs attention:** Plotly.js integration plan, component design
- 🔴 **Blocker:** None identified

**For Week 5 (Analytics):**
- 🟢 **Ready:** SQL queries well-scoped, examples in planning docs
- 🟨 **Needs attention:** Database indexing strategy
- 🔴 **Blocker:** Week 4 visualization must complete first

**For Beta Launch (Week 6):**
- 🟢 **Ready:** Core views functional, basic analytics working
- 🟨 **Needs attention:** Error handling, loading states, performance testing
- 🟡 **Deferred:** Advanced analytics (correctly scoped to post-MVP)

### Key Takeaway

**The views roadmap is well-planned and achievable.** Success depends on:
1. Starting Week 4 with a working Plotly.js integration
2. Keeping Week 5 scope minimal (basic queries only)
3. Resisting feature creep (advanced analytics can wait)

The team should feel confident proceeding with the current plan.

---

**Assessment Complete**
**Next Review:** End of Week 3 (before visualization implementation begins)
**Questions?** Refer to `PRE_COMMERCIAL_MVP_PLAN.md` or `CONTINUAL_SYNC_SPEC.md`
