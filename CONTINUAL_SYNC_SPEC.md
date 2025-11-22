# CONTINUAL_SYNC_SPEC.md
Foldline – Continual Sync Specification (Revised)
================================================

## 1. Purpose

This document defines the architecture, requirements, and UX flows for **continual, privacy‑preserving, local-only synchronization** of Garmin data using FIT files. Foldline must remain functional without cloud access, without Garmin APIs, and without background daemons.

Sync must feel:
- predictable  
- manual-when-you-want-it  
- optionally automatic when Garmin Express is present  
- 100% offline  
- non-destructive  

This spec is suitable for direct handoff to engineering (Tauri + Python backend + Svelte UI).

---

## 2. Sync Modes Overview

Foldline supports **three** ingest/update modes:

### 1. Automatic Sync (via Garmin Express) — Recommended
- Uses Garmin’s official desktop sync tool.
- Requires a physical USB cable connection.
- Automatically places FIT files into device-specific local folders.
- Foldline reads and ingests new files whenever sync is triggered.

### 2. Manual FIT Folder Import
- User manually selects any folder containing `.fit` or `.FIT` files.
- Foldline performs one-time or repeat ingestion.

### 3. Watched Folder Sync (Advanced)
- User selects arbitrary folders (local, cloud, network, Syncthing, etc.)
- Foldline re-imports new files whenever sync is triggered.

All paths end in:

`FIT files → parsing → deduplication → unified DuckDB → visualizations`

---

## 3. Mode 1 — Automatic Sync via Garmin Express

### 3.1 Garmin Express Summary
Garmin Express is Garmin’s official desktop companion app:
- Syncs devices via the USB charging cable.
- Creates private local backups of all FIT files.
- Updates firmware, maps, and device settings.

Garmin Express maintains internal folders such as:

**macOS**
```
~/Library/Application Support/Garmin/Devices/<DEVICE-ID>/
```

**Windows**
```
%APPDATA%\Garmin\Devices\<DEVICE-ID>\
```

Subfolders may include:
- `Activities/`
- `Monitor/`
- `Sleep/`
- `Stress/`
- `Daily/`

Foldline must not assume exact folder presence—must scan dynamically.

---

### 3.2 Device Detection Logic

1. Search known platform-specific Garmin Express roots.
2. For each `<DEVICE-ID>` folder:
   - Look for subfolders containing `.fit` files.
   - Record count of files + most recent modification time.
3. Present each device as:
   - Name (folder ID)
   - Last sync timestamp (most recent FIT timestamp)
   - File count

If no devices detected:
- Offer guidance for installing Garmin Express.
- Provide manual folder selection as fallback.

---

### 3.3 Sync Triggering

Sync is **pull-triggered**, never background-driven.

Triggers:
- App startup (if enabled)
- User clicks **Sync Now**
- User performs an action requiring updated data (lightweight refresh)

No background processes.  
No OS-level services.  
Sync only runs when Foldline is open.

---

### 3.4 Folder Scanning Algorithm

For each configured Garmin Express device folder:
1. Recursively walk subdirectories.
2. Identify files where:
   - extension matches `.fit` or `.FIT`
   - file has not been ingested (checked via dedup registry)
   - or file has changed size/timestamp/hash
3. Pass new/updated files to FIT parser.

Avoid any writes to device folders.

---

## 4. Mode 2 — Manual FIT Folder Import

### 4.1 UX Flow
1. User opens **Import FIT Folder**.
2. Tauri file picker allows selecting any folder.
3. Foldline recursively scans inside for `.fit` files.
4. Deduplicate and ingest.

### 4.2 Behavior
Supports:
- Initial bulk import
- Historical import
- Manual periodic updates

User can store multiple manual imports; no overwriting.

---

## 5. Mode 3 — Watched Folder Sync (Advanced)

### 5.1 Use Cases
- Dropbox / OneDrive backup folders
- Syncthing automations
- Power users managing their own FIT archives
- Third-party tool exports

### 5.2 Behavior
- User adds one or more watched folders.
- On sync trigger, Foldline scans these folders for new files.
- Optionally enable continuous watching (v1.1+) using OS-level watchers.

---

## 6. Deduplication & File Registry

A robust deduplication registry ensures files are never double-ingested.

### 6.1 Table Schema (DuckDB)

```sql
CREATE TABLE IF NOT EXISTS file_registry (
    file_id INTEGER PRIMARY KEY AUTOINCREMENT,
    file_path TEXT NOT NULL,
    file_hash TEXT,
    file_size BIGINT NOT NULL,
    modified_time TIMESTAMP NOT NULL,
    first_seen_at TIMESTAMP NOT NULL,
    last_ingested_at TIMESTAMP NOT NULL,
    source TEXT NOT NULL,
    last_error TEXT
);
```

### 6.2 Deduplication Strategy
- For speed: first compare size + modified time.
- If unchanged, skip.
- If ambiguous or changed: compute SHA-1 hash to confirm identity.

New location but identical hash → treat as same file.

---

## 7. FIT Ingestion Pipeline

### 7.1 Steps
1. Identify new or changed files.
2. Parse via `fitparse` (or Garmin FIT SDK).
3. Extract messages:
   - `record`
   - `monitoring`
   - `sleep` / `sleep_level`
   - `stress`
   - `activity` / `session`
4. Convert to normalized tables:
   - `metrics_heart_rate`
   - `metrics_hrv`
   - `metrics_sleep`
   - `metrics_stress`
   - `metrics_steps`
   - `activities`
5. Insert into DuckDB.
6. Update registry.

### 7.2 Error Handling
- Catch parsing exceptions.
- Log path + exception.
- Store error string in registry.
- Continue processing other files.

---

## 8. User Experience Requirements

### 8.1 Onboarding

Present three clear choices:

#### Option A — Automatic via Garmin Express
> “Connect your Garmin watch using the charging cable. Garmin Express will automatically create a private backup of your FIT files. Foldline can read these files to stay fully up to date—without any cloud access.”

Buttons:
- **Use Garmin Express Folder**
- **Install Garmin Express**

#### Option B — Manual Import
> “Import FIT files from any folder—ideal for historical data or occasional updates.”

Button: **Import FIT Folder**

#### Option C — Watched Folders (Advanced)
> “Power users can add any folder (Dropbox, Syncthing, etc.) to check for new FIT files during sync.”

Button: **Add Watched Folder**

---

## 9. Settings Panel

Include:

- **Sync on startup** toggle
- **Sync now** button
- List of configured Garmin Express devices (with enable/disable)
- List of watched folders (add/remove)
- Link to import error logs
- “Rebuild database” (advanced)

---

## 10. Privacy and Security Guarantees

- Foldline **never touches the cloud**.
- Foldline **never uses Garmin APIs**.
- No telemetry.
- No analytics.
- No data leaves the machine.
- All sync paths are read-only.
- All ingestion is local.

User data remains 100% under their control.

---

## 11. Future Extensions (Post v1)

- Continuous file watching with OS APIs.
- Multi-vendor import (Suunto, Coros, Polar).
- Conflict resolution for multi-source FITs.
- Smart metrics recalculation after schema changes.
- User-defined sync rules (e.g., ignore certain folders).

---

## 12. v1 Acceptance Criteria

- Must ingest historical data (FIT folders or GDPR ZIP).
- Must allow users to configure Garmin Express folder.
- Must ingest new files on demand reliably.
- Must never double-ingest the same FIT file.
- Must never lose user data.
- Must present understandable onboarding for non-technical users.
- Must preserve privacy at all times.
