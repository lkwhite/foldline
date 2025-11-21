# Foldline: Minimal Testing Strategy

## Executive Summary

This document scopes a **minimal but effective** test suite for Foldline development. The focus is on high-risk data integrity paths while avoiding over-testing.

---

## ✅ What to Test (Priority Order)

### **TIER 1: Data Integrity (Critical)**

These tests protect against data loss and corruption—the highest risk for a health data analyzer.

#### 1. Python Backend - Data Ingestion (`backend/ingestion/`)
**Files: `test_fit_folder.py`, `test_garmin_gdpr.py`**

**Test Coverage:**
- ✅ FIT file scanning: Recursive directory traversal, `.fit` file discovery
- ✅ File hashing: SHA256 computation, deduplication logic
- ✅ FIT parsing: Valid FIT file → structured data (sleep, HRV, activities)
- ✅ Error handling: Corrupted files, missing permissions, invalid zip archives
- ✅ Zip extraction: GDPR export structure, nested folders

**Why:** Data ingestion is the entry point. Bugs here cascade through the entire system.

**Python Version:** **3.11+ only** (skip 3.8/3.9—obsolete per your requirement)

---

#### 2. Python Backend - Database Operations (`backend/db/`)
**Files: `test_database.py`**

**Test Coverage:**
- ✅ Connection management: DuckDB/SQLite initialization, schema loading
- ✅ Schema integrity: 12 tables created, foreign keys enforced, indexes exist
- ✅ Deduplication: `imported_files` hash checking prevents duplicate imports
- ✅ Basic CRUD: Insert sleep record → query by date → verify data
- ✅ Transactions: Rollback on error (atomicity for batch imports)

**Why:** Database bugs cause silent data loss or incorrect aggregations.

---

#### 3. Python Backend - Metrics Calculations (`backend/metrics/`)
**Files: `test_sleep.py`, `test_hrv.py`, `test_stress.py`**

**Test Coverage:**
- ✅ Sleep analysis: Duration, stage percentages, sleep score calculation
- ✅ HRV trends: Daily aggregations, moving averages
- ✅ Stress aggregation: Rest vs. activity stress, daily min/max/avg
- ✅ Edge cases: Missing data, single-day queries, date range boundaries

**Why:** Incorrect health insights undermine trust in the application.

**Note:** Use **synthetic test data** (hardcoded fixtures), not real health data.

---

### **TIER 2: Integration (Important)**

#### 4. Python Backend - FastAPI Endpoints (`backend/`)
**Files: `test_api.py`**

**Test Coverage:**
- ✅ Request validation: Invalid date formats, missing parameters → 422 errors
- ✅ Response serialization: Pydantic models return correct JSON structure
- ✅ CORS: Localhost requests accepted, external origins rejected
- ✅ Health check: `/status` returns available metrics
- ✅ Import endpoints: `/import/fit-folder` validates paths exist

**Testing Approach:** Use **FastAPI TestClient** (no server required)

```python
from fastapi.testclient import TestClient
from backend.main import app

def test_health_check():
    client = TestClient(app)
    response = client.get("/status")
    assert response.status_code == 200
    assert "available_metrics" in response.json()
```

---

#### 5. Tauri - Process Management (`src-tauri/src/`)
**Files: `tests/integration_test.rs`**

**Test Coverage:**
- ✅ Backend startup: `start_backend()` spawns Python, finds available port
- ✅ Health check: `/status` reachable after startup
- ✅ Backend shutdown: `stop_backend()` kills process cleanly
- ✅ Port conflicts: Retry logic when port 8000 occupied

**Testing Approach:** Use **Tauri's test harness** with mocked subprocess

**Why:** Orphaned Python processes or port conflicts break the app.

---

### **TIER 3: Frontend (Nice-to-Have)**

#### 6. SvelteKit - API Client (`frontend/src/lib/`)
**Files: `api.test.ts`**

**Test Coverage:**
- ✅ `initBackend()`: Retry logic on connection failure
- ✅ `apiGet/apiPost()`: Error handling for 4xx/5xx responses
- ✅ File path sanitization: Tauri file dialog integration

**Testing Approach:** Use **Vitest** with mocked `fetch`

```typescript
import { describe, it, expect, vi } from 'vitest';
import { apiGet } from '$lib/api';

describe('API Client', () => {
  it('retries on connection error', async () => {
    global.fetch = vi.fn()
      .mockRejectedValueOnce(new Error('ECONNREFUSED'))
      .mockResolvedValueOnce({ ok: true, json: async () => ({}) });

    await apiGet('/status');
    expect(fetch).toHaveBeenCalledTimes(2);
  });
});
```

---

## ❌ What NOT to Test (Avoid Waste)

### **Skip These:**

1. **❌ Python 3.8, 3.9, 3.10 Compatibility**
   - **Why:** Obsolete. Test **3.11+ only** (current stable).
   - **Savings:** 3x fewer CI jobs, faster test runs.

2. **❌ UI Component Unit Tests (Svelte)**
   - **Why:** Low business logic in UI. Focus on API client instead.
   - **Exception:** Only test if components have complex state logic.

3. **❌ Extensive E2E Tests**
   - **Why:** Expensive, slow, flaky. Defer until core features stabilize.
   - **Alternative:** Manual smoke testing via `npm run dev`.

4. **❌ fitparse Library Internals**
   - **Why:** Third-party library. Trust their tests.
   - **Test only:** Our wrapper functions around fitparse.

5. **❌ DuckDB/SQLite Engine**
   - **Why:** Mature database engines. Test our queries, not their engine.

6. **❌ Tauri Framework Itself**
   - **Why:** Framework handles IPC. Test our command implementations only.

7. **❌ PyInstaller Bundling**
   - **Why:** Manual verification sufficient at this stage. Automate later.

8. **❌ Cross-Platform UI Pixel-Perfect Tests**
   - **Why:** Different OS rendering. Manual QA on each platform.

---

## 🛠️ Test Infrastructure Setup

### **Python (Backend)**

**Install Dependencies:**
```bash
# Add to backend/requirements.txt
pytest==8.0.0
pytest-asyncio==0.23.0  # For async FastAPI tests
httpx==0.26.0           # FastAPI TestClient dependency
pytest-cov==4.1.0       # Coverage reporting (optional)
```

**Configuration: `backend/pytest.ini`**
```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
asyncio_mode = auto
```

**Directory Structure:**
```
backend/
├─ tests/
│  ├─ __init__.py
│  ├─ test_fit_folder.py
│  ├─ test_garmin_gdpr.py
│  ├─ test_database.py
│  ├─ test_sleep.py
│  ├─ test_hrv.py
│  ├─ test_stress.py
│  ├─ test_api.py
│  └─ fixtures/
│     ├─ sample.fit          # Minimal valid FIT file
│     ├─ garmin_export.zip   # Minimal GDPR export
│     └─ test_data.json      # Synthetic health metrics
```

**Run Tests:**
```bash
cd backend
python -m pytest tests/ -v
```

---

### **Rust (Tauri)**

**Configuration: `src-tauri/Cargo.toml`**
```toml
[dev-dependencies]
tauri = { version = "2.0", features = ["test"] }
```

**Directory Structure:**
```
src-tauri/
├─ src/
│  └─ main.rs
└─ tests/
   └─ integration_test.rs
```

**Run Tests:**
```bash
cd src-tauri
cargo test
```

---

### **TypeScript (Frontend)**

**Install Dependencies:**
```bash
# Add to frontend/package.json devDependencies
npm install -D vitest @vitest/ui jsdom
```

**Configuration: `frontend/vitest.config.ts`**
```typescript
import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    environment: 'jsdom',
    globals: true,
  },
});
```

**Directory Structure:**
```
frontend/src/
├─ lib/
│  ├─ api.ts
│  └─ api.test.ts  ← Test next to source file
```

**Run Tests:**
```bash
cd frontend
npm run test
```

---

## 🚀 CI/CD Minimal Requirements

**File: `.github/workflows/test.yml`**

```yaml
name: Tests

on: [push, pull_request]

jobs:
  backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'  # Single version only
      - run: |
          cd backend
          pip install -r requirements.txt
          pytest tests/ -v

  tauri:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: |
          cd src-tauri
          cargo test

  frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
      - run: |
          cd frontend
          npm install
          npm run test
```

**Why Minimal:**
- ✅ Tests run on every push (catch regressions early)
- ✅ Single OS (ubuntu-latest) - defer multi-OS testing
- ✅ Single Python version (3.11) - no matrix builds
- ❌ No deployment, bundling, or release automation yet

---

## 📊 Test Metrics (Success Criteria)

**Coverage Targets (Pragmatic):**
- **Backend ingestion/db/metrics**: **80%+ line coverage**
- **Backend API**: **60%+ line coverage** (validation paths)
- **Tauri commands**: **50%+ line coverage** (happy path + error handling)
- **Frontend API client**: **60%+ line coverage** (retry logic)

**Why Not 100%?**
- Diminishing returns on effort
- Some code paths (e.g., PyInstaller hooks) hard to test in CI
- Focus on high-risk areas, not perfection

---

## 🎯 Testing Principles

1. **Fast Feedback**
   - Unit tests run in `< 5 seconds`
   - Integration tests run in `< 30 seconds`
   - No external services (databases in-memory via `:memory:`)

2. **Isolated Tests**
   - Each test creates its own temp database
   - No shared state between tests
   - Use pytest fixtures for setup/teardown

3. **Readable Assertions**
   ```python
   # Good
   assert sleep_record.duration_minutes == 480

   # Avoid
   assert len(json.loads(response.text)['data']) > 0
   ```

4. **Test Data Discipline**
   - Use **synthetic data** (not real health data)
   - Keep fixtures minimal (1 sleep record, not 365 days)
   - Hardcode expected values (no "test passes if output matches input")

---

## 📝 Implementation Checklist

**Phase 1 (Week 1):**
- [ ] Set up pytest infrastructure (`backend/tests/`, `pytest.ini`)
- [ ] Write `test_fit_folder.py` - file scanning, hashing
- [ ] Write `test_database.py` - schema init, basic CRUD
- [ ] Create sample FIT file fixture

**Phase 2 (Week 2):**
- [ ] Write `test_garmin_gdpr.py` - zip extraction
- [ ] Write `test_sleep.py`, `test_hrv.py` - metrics calculations
- [ ] Write `test_api.py` - FastAPI endpoints

**Phase 3 (Week 3):**
- [ ] Set up Cargo test harness (`src-tauri/tests/`)
- [ ] Write `integration_test.rs` - process management
- [ ] Set up Vitest (`frontend/vitest.config.ts`)
- [ ] Write `api.test.ts` - HTTP client

**Phase 4 (Week 4):**
- [ ] Add GitHub Actions workflow (`.github/workflows/test.yml`)
- [ ] Run full test suite locally
- [ ] Document test commands in README

---

## 🔄 Evolution Strategy

**Start Minimal, Expand Strategically:**

1. **Now (MVP):** Tier 1 tests only (data integrity)
2. **After first release:** Add Tier 2 (integration tests)
3. **After user feedback:** Add E2E smoke tests for top user flows
4. **If needed:** Multi-platform testing (macOS/Windows runners)
5. **If needed:** Performance benchmarks (database query speed)

---

## 🚫 Anti-Patterns to Avoid

1. **Don't test implementation details** - Test behavior, not private methods
2. **Don't mock everything** - Use real database (in-memory) when possible
3. **Don't snapshot test JSON** - Brittle, hard to review changes
4. **Don't skip test cleanup** - Delete temp files, close connections
5. **Don't commit slow tests** - Keep CI under 2 minutes total

---

## Summary

**Test These:**
- ✅ Data ingestion (FIT parsing, deduplication)
- ✅ Database operations (CRUD, schema)
- ✅ Metrics calculations (sleep, HRV, stress)
- ✅ API validation (FastAPI endpoints)
- ✅ Process management (Tauri backend spawning)

**Skip These:**
- ❌ Python 3.8/3.9 (obsolete)
- ❌ UI component unit tests (low value)
- ❌ Third-party library internals
- ❌ Extensive E2E tests (premature)

**Total Effort:** ~3-4 weeks for comprehensive minimal suite, ~1 week for Tier 1 only.
