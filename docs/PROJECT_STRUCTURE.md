# Foldline Project Structure

This document explains the reorganized project structure with separate marketing and desktop app codebases.

## Overview

Foldline is now structured as two separate projects:

1. **Desktop App** (`frontend/`) - Tauri-based cross-platform desktop application
2. **Marketing Website** (`marketing/`) - Standalone marketing landing page

## Directory Structure

```
foldline/
├── frontend/              # Desktop App (Tauri + SvelteKit)
│   ├── src/
│   │   ├── routes/        # App routes (Setup, Dashboard, Heatmaps, etc.)
│   │   ├── lib/
│   │   │   ├── components/
│   │   │   └── stores/
│   │   └── app.css
│   ├── static/
│   │   ├── brand/         # Logo files
│   │   └── design/        # Design tokens (copied from /design)
│   └── package.json
│
├── marketing/             # Marketing Website (SvelteKit)
│   ├── src/
│   │   ├── routes/        # Marketing landing page
│   │   ├── lib/
│   │   │   ├── components/
│   │   │   │   └── marketing/  # Marketing-specific components
│   │   │   └── stores/
│   │   └── app.css
│   ├── static/
│   │   ├── brand/         # Logo files
│   │   ├── design/        # Design tokens (copied from /design)
│   │   └── screenshots/   # Marketing screenshots
│   └── package.json
│
├── src-tauri/             # Tauri Rust backend
│   ├── src/
│   ├── Cargo.toml
│   └── tauri.conf.json
│
├── backend/               # Python backend (runs as Tauri sidecar)
│   └── main.py
│
├── design/                # Design System (source of truth)
│   ├── BRAND_TOKENS.css
│   ├── TYPOGRAPHY.css
│   └── BRAND_SPEC.md
│
└── package.json           # Root scripts for running both projects
```

## Running the Projects

### Marketing Website (Development)
```bash
npm run dev:marketing
```
- Runs on: http://localhost:5174
- Clean landing page without app navigation
- Can be deployed to Vercel, Netlify, etc.

### Desktop App (Development)
```bash
npm run dev:frontend
# or for full Tauri experience:
npm run tauri:dev
```
- Runs on: http://localhost:5173
- Full app navigation (Setup, Dashboard, Heatmaps, etc.)
- Includes Tauri features (file system access, native dialogs, etc.)

### Full App with Backend
```bash
npm run dev           # Runs backend + frontend
npm run tauri:dev     # Runs full Tauri app
```

## Building for Production

### Marketing Website
```bash
npm run build:marketing
# Output: marketing/build/
```

### Desktop App (All Platforms)
```bash
npm run tauri:build
# Creates installers for Windows, macOS, Linux
```

## Key Differences

| Feature | Marketing Site | Desktop App |
|---------|---------------|-------------|
| **URL** | `localhost:5174` | `localhost:5173` |
| **Layout** | Clean, logo + theme toggle only | Full app navigation bar |
| **Routes** | Single landing page | Setup, Dashboard, Heatmaps, Trends, etc. |
| **Deployment** | Static hosting (Vercel/Netlify) | Tauri installers (.exe, .dmg, .deb) |
| **Purpose** | Public-facing landing page | Private desktop application |

## Design System Sharing

Both projects share the same design tokens from `/design/`:
- `BRAND_TOKENS.css` - Colors, spacing, typography tokens
- `TYPOGRAPHY.css` - Font definitions
- `linework.css` - Minimal line-drawing utilities

These are copied to each project's `static/design/` directory and imported via `app.css`.

## Installation

### First Time Setup
```bash
# Install all dependencies
npm run install:all

# Or individually:
npm run install:frontend
npm run install:marketing
npm run install:backend
```

### Development Workflow
1. **Marketing site**: Work in `marketing/` - runs independently
2. **Desktop app**: Work in `frontend/` - integrates with Tauri and Python backend
3. **Shared design**: Edit source files in `/design/`, then copy to both projects

## Cross-Platform Desktop App

Thanks to Tauri, the desktop app can be built for:
- **Windows** (.exe installer)
- **macOS** (.dmg and .app)
- **Linux** (.deb, .AppImage)

All from a single codebase, with native performance and small bundle sizes (~3-5MB).

## Tech Stack

- **Frontend Framework**: SvelteKit
- **Desktop Framework**: Tauri 2.0
- **Backend**: Python (runs as sidecar)
- **Styling**: CSS with design tokens
- **Package Manager**: npm
