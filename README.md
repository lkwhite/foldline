# Foldline

**Privacy-first, local-only wearable data analyzer for Garmin devices**

Foldline is a cross-platform desktop application that analyzes wearable data from Garmin GDPR exports and local FIT files. All data processing happens entirely on your machine—no cloud APIs, no OAuth, no external servers.

## Features

- 🔒 **100% Local**: All data stays on your machine
- 🔄 **Garmin Express Auto-Sync**: Automatically detects and syncs from Garmin Express (macOS/Windows)
- 💾 **GDPR Export Support**: Import your complete Garmin data archive
- 📊 **Rich Visualizations**: Heatmaps, trends, and correlation analysis (coming soon)
- 📈 **Multiple Metrics**: Sleep, HRV, resting HR, stress, steps, and more
- 🚫 **No External APIs**: Works completely offline
- 🔐 **Privacy-First**: No telemetry, no cloud uploads, no OAuth required

## Architecture

```
[ Tauri Shell (Rust) ]
        ↓
[ SvelteKit Frontend ]
        ↓ (HTTP on localhost)
[ Python Backend (FastAPI) ]
        ↓
[ DuckDB/SQLite + FIT Parser ]
```

## Project Structure

```
foldline/
├─ src-tauri/           # Tauri (Rust) shell
│   ├─ src/
│   │   └─ main.rs      # Process management, file dialogs
│   └─ tauri.conf.json
│
├─ frontend/            # SvelteKit UI
│   ├─ src/
│   │   ├─ routes/      # Pages: setup, dashboard, heatmaps, etc.
│   │   └─ lib/         # API client, utilities
│   └─ package.json
│
├─ backend/             # Python FastAPI backend
│   ├─ main.py          # API endpoints
│   ├─ ingestion/       # GDPR & FIT file parsers
│   ├─ db/              # Database schema & connection
│   ├─ metrics/         # Metrics analysis (sleep, HRV, etc.)
│   ├─ models/          # Data models
│   └─ utils/           # Utilities
│
└─ scripts/             # Build & dev scripts
```

## Prerequisites

- **Node.js** 18+ (for frontend)
- **Python** 3.9+ (for backend)
- **Rust** 1.70+ (for Tauri, install via [rustup](https://rustup.rs/))
- **Tauri Dependencies**: See [Tauri prerequisites](https://tauri.app/v2/guides/getting-started/prerequisites/)

### Platform-Specific Requirements

**macOS:**
```bash
xcode-select --install
```

**Windows:**
- Visual Studio 2022 with C++ tools
- WebView2 (usually pre-installed on Windows 11)

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install libwebkit2gtk-4.1-dev \
  build-essential \
  curl \
  wget \
  file \
  libssl-dev \
  libayatana-appindicator3-dev \
  librsvg2-dev
```

## Quick Start

### 1. Clone and Setup

```bash
git clone https://github.com/yourusername/foldline.git
cd foldline
```

Run the setup script:

```bash
# Make scripts executable
chmod +x scripts/*.sh

# Run setup
./scripts/setup.sh
```

Or manually install dependencies:

```bash
# Install frontend dependencies
cd frontend
npm install
cd ..

# Install backend dependencies
cd backend
pip install -r requirements.txt
cd ..
```

### 2. Development

**Option A: Use the dev script (recommended)**

```bash
./scripts/dev.sh
```

This will:
1. Start the Python backend on port 8000
2. Start Tauri in dev mode (which starts the frontend)
3. Open the app window

**Option B: Manual start**

Terminal 1 (Backend):
```bash
cd backend
python3 main.py --port 8000
```

Terminal 2 (Tauri + Frontend):
```bash
cd src-tauri
cargo tauri dev
```

### 3. Building for Production

```bash
./scripts/build.sh
```

This will:
1. Build the frontend (SvelteKit)
2. Package the Python backend with PyInstaller
3. Build the Tauri app with bundled installers

Output locations:
- **macOS**: `src-tauri/target/release/bundle/dmg/`
- **Windows**: `src-tauri/target/release/bundle/msi/`
- **Linux**: `src-tauri/target/release/bundle/appimage/` or `.deb`

## Usage

### First-Time Setup

**Step 1: Import Historical Data (GDPR Export)**

1. Request your data from [Garmin](https://www.garmin.com/en-US/account/datamanagement/exportdata/)
2. Wait for the export email (can take a few days)
3. Download the ZIP file
4. In Foldline: **Settings** → **Import Historical Data** → **Upload GDPR Export**
5. Wait for import to complete (progress bar shows status)

**Step 2: Enable Garmin Express Auto-Sync** (Recommended)

1. Install [Garmin Express](https://www.garmin.com/en-US/software/express/) if not already installed
2. Connect your Garmin device via USB and sync at least once
3. In Foldline: **Settings** → **Garmin Express Devices** → **Detect Devices**
4. Enable sync for your device(s)
5. Click **Sync Now** to import recent data

Garmin Express folders are located at:
- **macOS**: `~/Library/Application Support/Garmin/Devices/<device-id>/`
- **Windows**: `%APPDATA%\Garmin\Devices\<device-id>\`

### Daily Use

**Keeping Data Fresh:**
1. Connect your Garmin device to Garmin Express (via USB)
2. Open Foldline and click **Sync Now** in Settings
3. Or: Enable **Sync on Startup** for automatic updates

**Manual Sync:**
- Settings → Garmin Express Devices → Device Name → **Sync Now**

**Viewing Your Data** (Coming Soon in Week 4-5):
- **Dashboard**: Overview of your data range and metrics
- **Heatmaps**: Year-at-a-glance visualizations
- **Trends**: Time series charts with smoothing options
- **Correlation**: Analyze relationships between metrics

## Development Guide

### Backend (Python)

The backend is a FastAPI app in `backend/main.py` with stub endpoints.

**Key endpoints:**
- `GET /status` - System status and data summary
- `POST /import/garmin-export` - Import GDPR zip
- `POST /import/fit-folder` - Import FIT directory
- `GET /metrics/heatmap` - Get heatmap data
- `GET /metrics/timeseries` - Get time series data
- `GET /metrics/correlation` - Correlation analysis

**TODO: Implement actual logic in:**
- `backend/ingestion/garmin_gdpr.py` - GDPR zip extraction
- `backend/ingestion/fit_folder.py` - FIT file scanning
- `backend/db/schema.sql` - Database schema (included)
- `backend/db/connection.py` - DB initialization
- `backend/metrics/*.py` - Metric calculations

### Frontend (SvelteKit)

The UI is built with SvelteKit in `frontend/src/`.

**Key files:**
- `routes/+page.svelte` - Setup/import page
- `routes/dashboard/+page.svelte` - Dashboard
- `routes/heatmaps/+page.svelte` - Heatmap view
- `routes/trends/+page.svelte` - Time series view
- `routes/correlation/+page.svelte` - Correlation analysis
- `lib/api.ts` - Backend API client
- `lib/fileDialog.ts` - Tauri file pickers

**TODO: Add visualization libraries:**
- Chart.js, D3.js, or Plotly for charts
- Calendar heatmap library for year views

### Tauri (Rust)

The Rust shell in `src-tauri/src/main.rs` handles:
- Starting/stopping the Python backend process
- File/folder picker dialogs
- Window management

**Key commands:**
- `start_backend()` - Spawn Python process
- `stop_backend()` - Kill Python process
- `get_backend_port()` - Get backend URL
- `check_backend_health()` - Ping backend

## Testing

Foldline has a comprehensive test suite covering the backend, frontend, and Tauri shell.

### Running Tests

**Python Backend Tests:**
```bash
cd backend
pytest tests/ -v
```

Run with coverage:
```bash
cd backend
pytest tests/ -v --cov=. --cov-report=html --cov-report=term-missing
```

**Rust/Tauri Tests:**
```bash
cd src-tauri
cargo test --verbose
```

**Frontend Tests:**
```bash
cd frontend
npm run test
```

Run in watch mode:
```bash
cd frontend
npm run test:watch
```

Run with UI:
```bash
cd frontend
npm run test:ui
```

### Test Structure

**Backend Tests** (`backend/tests/`):
- `test_fit_folder.py` - FIT file scanning and deduplication
- `test_garmin_gdpr.py` - GDPR export parsing
- `test_database.py` - Database operations and schema
- `test_sleep.py` - Sleep metrics calculations
- `test_hrv.py` - HRV analysis
- `test_stress.py` - Stress aggregation
- `test_api.py` - FastAPI endpoint validation

**Tauri Tests** (`src-tauri/tests/`):
- `integration_test.rs` - Process management and health checks

**Frontend Tests** (`frontend/src/lib/`):
- `api.test.ts` - API client and error handling

### CI/CD

Tests run automatically on every push and pull request via GitHub Actions.

**Workflow:** `.github/workflows/test.yml`

The CI pipeline runs:
1. Python backend tests (pytest)
2. Rust/Tauri tests (cargo test)
3. Frontend tests (vitest)

All tests must pass before merging.

### Test Coverage

Current focus areas:
- ✅ Data integrity (FIT parsing, deduplication)
- ✅ Database operations (CRUD, schema validation)
- ✅ Metrics calculations (sleep, HRV, stress)
- ✅ API validation (request/response contracts)
- ✅ Process management (backend spawning, cleanup)

See `docs/TESTING_PLAN.md` for detailed testing strategy.

## Packaging Python Backend

For production builds, the Python backend is compiled into a standalone binary using PyInstaller:

```bash
cd backend
pyinstaller --name python_backend --onefile main.py
```

The binary is placed in `src-tauri/bin/` and bundled with the Tauri app.

**Platform-specific binary names:**
- Windows: `python_backend.exe`
- macOS (ARM): `python_backend-aarch64-apple-darwin`
- macOS (x86): `python_backend-x86_64-apple-darwin`
- Linux: `python_backend-x86_64-unknown-linux-gnu`

## Database

Foldline uses DuckDB (or SQLite) for local data storage.

**Schema:** See `backend/db/schema.sql`

**Tables:**
- `sleep_records` - Sleep data
- `resting_hr` - Resting heart rate
- `hrv_records` - HRV measurements
- `stress_records` - Stress scores
- `daily_steps` - Step counts
- `activities` - Workouts and training load
- `imported_files` - File deduplication tracking

**Default location:** `~/.foldline/data/foldline.db`

## Security & Privacy

- ✅ Backend only listens on `127.0.0.1` (localhost)
- ✅ No external network calls
- ✅ No OAuth or API keys
- ✅ No telemetry or analytics
- ✅ All data stored locally
- ✅ Works completely offline

## Troubleshooting

**Backend won't start:**
- Check that Python 3.9+ is installed: `python3 --version`
- Install dependencies: `pip install -r backend/requirements.txt`
- Check port 8000 isn't in use: `lsof -i :8000` (macOS/Linux)

**Tauri build fails:**
- Update Rust: `rustup update`
- Install Tauri prerequisites: [Tauri docs](https://tauri.app/v2/guides/getting-started/prerequisites/)
- Clear cache: `cd src-tauri && cargo clean`

**PyInstaller issues:**
- Ensure PyInstaller is installed: `pip install pyinstaller`
- Try a clean build: `pyinstaller --clean --onefile main.py`
- Check for hidden imports (may need to add to `.spec` file)

**Frontend not loading:**
- Check that the backend is running
- Verify CORS settings in `backend/main.py`
- Check browser console for errors

## Development Status

**Current Phase:** Pre-Commercial MVP (5-6 weeks)

### ✅ Completed
- [x] Database schema with continual sync support
- [x] Garmin Express device detection (macOS/Windows)
- [x] Incremental sync engine (file change detection)
- [x] FIT file parsing (basic implementation)
- [x] File deduplication (SHA256 hashing)

### 🚧 In Progress (Week 1)
- [ ] GDPR export extraction and parsing
- [ ] GDPR JSON field mappings
- [ ] Enhanced FIT parsing with GDPR knowledge

### 📋 Next Up
- [ ] Garmin Express sync UI (Settings page)
- [ ] Visualization (Plotly integration)
- [ ] Basic analytics (sleep, HRV, stress, steps heatmaps/trends)
- [ ] Beta testing with real users

### 🔮 Post-MVP (Commercial Launch)
- [ ] Payment system (Lemon Squeezy)
- [ ] Advanced analytics (health score, recovery, correlations)
- [ ] Power user features (annotations, predictions)
- [ ] Multi-vendor support (Whoop, Oura, Apple Watch)

**For detailed planning:** See [PRE_COMMERCIAL_MVP_PLAN.md](docs/PRE_COMMERCIAL_MVP_PLAN.md)

## Documentation

📚 **[DOCUMENTATION_INDEX.md](docs/DOCUMENTATION_INDEX.md)** - Complete guide to all project documentation

**Key docs:**
- **[PRE_COMMERCIAL_MVP_PLAN.md](docs/PRE_COMMERCIAL_MVP_PLAN.md)** - Current 5-6 week roadmap
- **[CONTINUAL_SYNC_SPEC.md](docs/CONTINUAL_SYNC_SPEC.md)** - Sync architecture and UX
- **[TESTING_PLAN.md](docs/TESTING_PLAN.md)** - Testing strategy
- **[FOLDLINE_HANDOFF.md](docs/FOLDLINE_HANDOFF.md)** - Algorithm reference (from gar-mining)

## Contributing

Contributions are welcome! Since this is a privacy-focused tool:

1. Never add external API calls or telemetry
2. Keep all processing local
3. No cloud services or OAuth
4. Follow existing code structure

## License

MIT License - see LICENSE file for details

## Acknowledgments

- Built with [Tauri](https://tauri.app/)
- Uses [FastAPI](https://fastapi.tiangolo.com/) for the backend
- Frontend powered by [SvelteKit](https://kit.svelte.dev/)
- FIT file parsing with [fitparse](https://github.com/dtcooper/python-fitparse)

---

**Made with ❤️ for privacy-conscious athletes**