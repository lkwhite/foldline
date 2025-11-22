# 📁 Foldline Design System File Consolidation Strategy

## Current Situation

The Foldline design system files are currently **duplicated across multiple directories**:

```
/design/                           (Source of truth - documentation)
  ├── BRAND_TOKENS.css
  ├── TYPOGRAPHY.css
  └── LAYOUT.md

/frontend/static/design/           (Duplicate - served statically)
  ├── BRAND_TOKENS.css
  └── TYPOGRAPHY.css

/frontend/src/lib/styles/          (Application-specific styles)
  └── linework.css

/marketing/static/design/          (Duplicate - served statically)
  ├── BRAND_TOKENS.css
  └── TYPOGRAPHY.css

/marketing/src/lib/styles/         (Application-specific styles)
  └── linework.css
```

**Problem**: Changes must be manually synced across 3 locations, risking inconsistency.

---

## Recommended Strategy

### **Option 1: Single Source with Build-Time Copy** (Recommended)

**Approach**: Keep `/design/` as the single source of truth, copy files during build.

#### **Advantages**
- ✅ Single source of truth
- ✅ No runtime dependencies
- ✅ Works with static site generators
- ✅ Clear separation: `/design/` = specs, `/frontend/` = implementation

#### **Implementation**

**1. Keep `/design/` as source:**
```
/design/
  ├── BRAND_TOKENS.css           ← Source of truth
  ├── TYPOGRAPHY.css             ← Source of truth
  └── [all .md files]            ← Documentation
```

**2. Add build script:**

```json
// package.json (root)
{
  "scripts": {
    "copy-design-tokens": "node scripts/copy-design-tokens.js",
    "prebuild": "npm run copy-design-tokens"
  }
}
```

```javascript
// scripts/copy-design-tokens.js
import fs from 'fs';
import path from 'path';

const designFiles = [
  'BRAND_TOKENS.css',
  'TYPOGRAPHY.css'
];

const targets = [
  './frontend/static/design',
  './marketing/static/design'
];

// Ensure target directories exist
targets.forEach(target => {
  if (!fs.existsSync(target)) {
    fs.mkdirSync(target, { recursive: true });
  }
});

// Copy files
designFiles.forEach(file => {
  const source = path.join('./design', file);
  targets.forEach(target => {
    const dest = path.join(target, file);
    fs.copyFileSync(source, dest);
    console.log(`✅ Copied ${file} to ${target}`);
  });
});

console.log('🎨 Design tokens synced successfully');
```

**3. Add to `.gitignore`:**
```gitignore
# Generated design token files (copied from /design/)
/frontend/static/design/BRAND_TOKENS.css
/frontend/static/design/TYPOGRAPHY.css
/marketing/static/design/BRAND_TOKENS.css
/marketing/static/design/TYPOGRAPHY.css
```

**4. Update imports (no change needed):**
```html
<!-- Frontend/Marketing -->
<link rel="stylesheet" href="/design/BRAND_TOKENS.css">
<link rel="stylesheet" href="/design/TYPOGRAPHY.css">
```

---

### **Option 2: Symlinks** (Simple, but has limitations)

**Approach**: Create symbolic links from `/frontend/` and `/marketing/` to `/design/`.

#### **Advantages**
- ✅ Simplest setup
- ✅ Real-time changes
- ✅ No build step needed

#### **Disadvantages**
- ❌ Doesn't work on all platforms (Windows issues)
- ❌ Doesn't work with some deployment systems
- ❌ Git doesn't track symlinks well

#### **Implementation**

```bash
# From root directory
cd frontend/static
ln -s ../../design ./design

cd ../../marketing/static
ln -s ../../design ./design
```

**Not recommended** due to platform incompatibility.

---

### **Option 3: NPM Package** (Overkill for single project)

**Approach**: Publish design tokens as an npm package.

#### **Advantages**
- ✅ Versioned design system
- ✅ Can be shared across multiple projects
- ✅ Clear dependency management

#### **Disadvantages**
- ❌ Overkill for single project
- ❌ Requires publishing/versioning overhead
- ❌ Adds complexity

**Not recommended** unless planning multi-product ecosystem.

---

### **Option 4: Shared CSS Import** (Current, not ideal)

**Approach**: Manually keep files in sync (current state).

#### **Disadvantages**
- ❌ Error-prone
- ❌ Easy to forget to sync
- ❌ No single source of truth

**Not recommended** - this is what we're trying to fix.

---

## Recommended Implementation: Option 1

### **Step-by-Step Migration**

#### **Phase 1: Setup (Immediate)**

1. **Create build script:**
   ```bash
   mkdir -p scripts
   # Create scripts/copy-design-tokens.js (code above)
   chmod +x scripts/copy-design-tokens.js
   ```

2. **Update package.json:**
   ```bash
   npm pkg set scripts.copy-design-tokens="node scripts/copy-design-tokens.js"
   npm pkg set scripts.prebuild="npm run copy-design-tokens"
   ```

3. **Run initial sync:**
   ```bash
   npm run copy-design-tokens
   ```

4. **Update .gitignore:**
   ```bash
   echo "" >> .gitignore
   echo "# Generated design files (do not edit)" >> .gitignore
   echo "/frontend/static/design/BRAND_TOKENS.css" >> .gitignore
   echo "/frontend/static/design/TYPOGRAPHY.css" >> .gitignore
   echo "/marketing/static/design/BRAND_TOKENS.css" >> .gitignore
   echo "/marketing/static/design/TYPOGRAPHY.css" >> .gitignore
   ```

#### **Phase 2: Verify (Testing)**

1. **Test build process:**
   ```bash
   cd frontend
   npm run build

   cd ../marketing
   npm run build
   ```

2. **Verify files are copied:**
   ```bash
   ls -la frontend/static/design/
   ls -la marketing/static/design/
   ```

3. **Test hot reload (dev mode):**
   ```bash
   # Terminal 1: Watch for changes and copy
   npm run watch-design-tokens

   # Terminal 2: Run dev server
   cd frontend && npm run dev
   ```

#### **Phase 3: Document (Ongoing)**

Add to **README.md** or **CONTRIBUTING.md**:

```markdown
## Design System Files

**Important**: Design tokens are maintained in `/design/` only.

### Making Changes

1. Edit files in `/design/` directory:
   - `BRAND_TOKENS.css`
   - `TYPOGRAPHY.css`

2. Run sync command:
   ```bash
   npm run copy-design-tokens
   ```

3. Files are automatically copied to:
   - `/frontend/static/design/`
   - `/marketing/static/design/`

### DO NOT EDIT
Never edit design files in:
- ❌ `/frontend/static/design/` (auto-generated)
- ❌ `/marketing/static/design/` (auto-generated)

Always edit in:
- ✅ `/design/` (source of truth)
```

---

## Watch Mode (Optional Enhancement)

For development, add a watch mode:

```javascript
// scripts/watch-design-tokens.js
import chokidar from 'chokidar';
import { execSync } from 'child_process';

const watcher = chokidar.watch('./design/*.css', {
  persistent: true,
  ignoreInitial: false
});

console.log('👀 Watching /design/ for changes...');

watcher.on('change', (path) => {
  console.log(`📝 File changed: ${path}`);
  execSync('npm run copy-design-tokens');
});
```

```json
// package.json
{
  "scripts": {
    "watch-design-tokens": "node scripts/watch-design-tokens.js"
  },
  "devDependencies": {
    "chokidar": "^3.5.3"
  }
}
```

---

## Application-Specific Files

**`linework.css` should NOT be consolidated** - it contains application-specific utilities.

**Current structure (keep as-is):**
```
/frontend/src/lib/styles/
  └── linework.css          ← Frontend-specific utilities

/marketing/src/lib/styles/
  └── linework.css          ← Marketing-specific utilities
```

**Rationale**: These files may diverge based on app vs. marketing site needs.

If they remain identical over time, consider consolidating later.

---

## Summary

### **Recommended Approach**

| Aspect | Strategy |
|--------|----------|
| **CSS Tokens** | Single source (`/design/`) + build-time copy |
| **Documentation** | Keep in `/design/` (not copied) |
| **Build Script** | `scripts/copy-design-tokens.js` |
| **Git Tracking** | Ignore copied files, track source only |
| **Dev Workflow** | Optional watch mode for convenience |

### **Benefits**

✅ Single source of truth (`/design/`)
✅ No manual syncing required
✅ Works with all build systems
✅ Clear documentation vs. implementation separation
✅ No platform compatibility issues
✅ Scales to future additions

### **Action Items**

1. [ ] Create `scripts/copy-design-tokens.js`
2. [ ] Update `package.json` with scripts
3. [ ] Update `.gitignore`
4. [ ] Run initial sync
5. [ ] Test build process
6. [ ] Document in README/CONTRIBUTING
7. [ ] (Optional) Set up watch mode for development

---

## Future Considerations

If Foldline expands to multiple products:

- Consider publishing as `@foldline/design-tokens` npm package
- Implement Style Dictionary for multi-platform token export
- Create Figma plugin for design-to-code sync

For now, **Option 1 (build-time copy)** is the optimal balance of simplicity and maintainability.
