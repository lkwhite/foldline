# 🛠️ Foldline Technical Implementation Guide

## Overview

This guide covers technical implementation details for the Foldline design system, including font loading, dark mode persistence, responsive images, naming conventions, and best practices.

---

## 1. Font Loading Strategy

### **Font Stack**

```css
--font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
--font-mono: 'Inter', 'SF Mono', Monaco, 'Cascadia Code', 'Courier New', monospace;
```

### **Google Fonts Loading (Marketing Site)**

**Optimized for performance:**

```html
<head>
  <!-- Preconnect to Google Fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>

  <!-- Load Inter with display: swap -->
  <link
    href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap"
    rel="stylesheet"
  >

  <!-- Optional: Preload for critical text -->
  <link
    rel="preload"
    as="style"
    href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap"
  >
</head>
```

**Benefits:**
- `display=swap`: Show fallback font immediately, swap when Inter loads (prevents FOIT)
- `preconnect`: Establish early connection to Google Fonts servers
- `preload`: Prioritize font loading for critical content

### **Self-Hosted Fonts (Tauri App)**

For the desktop app, self-host fonts to avoid external dependencies:

```css
/* /frontend/src/lib/styles/fonts.css */

@font-face {
  font-family: 'Inter';
  src: url('/fonts/Inter-Regular.woff2') format('woff2'),
       url('/fonts/Inter-Regular.woff') format('woff');
  font-weight: 400;
  font-style: normal;
  font-display: swap;
}

@font-face {
  font-family: 'Inter';
  src: url('/fonts/Inter-Medium.woff2') format('woff2'),
       url('/fonts/Inter-Medium.woff') format('woff');
  font-weight: 500;
  font-style: normal;
  font-display: swap;
}

@font-face {
  font-family: 'Inter';
  src: url('/fonts/Inter-SemiBold.woff2') format('woff2'),
       url('/fonts/Inter-SemiBold.woff') format('woff');
  font-weight: 600;
  font-style: normal;
  font-display: swap;
}
```

**File locations:**
```
/frontend/static/fonts/
  ├── Inter-Regular.woff2
  ├── Inter-Regular.woff
  ├── Inter-Medium.woff2
  ├── Inter-Medium.woff
  ├── Inter-SemiBold.woff2
  └── Inter-SemiBold.woff
```

### **Font Loading Performance**

**Lighthouse targets:**
- First Contentful Paint: < 1.5s
- Cumulative Layout Shift: < 0.1

**Techniques:**
1. **Subset fonts**: Include only Latin characters (reduces file size by ~60%)
2. **Preload critical fonts**: Preload Regular (400) weight only
3. **Use system fonts as fallback**: Minimal layout shift
4. **Font-display: swap**: Prevent invisible text

---

## 2. Dark Mode Implementation

### **Theme Persistence**

Store user preference in `localStorage`:

```javascript
// /frontend/src/lib/stores/theme.js (Svelte store)

import { writable } from 'svelte/store';
import { browser } from '$app/environment';

// Detect system preference
const getSystemTheme = () => {
  if (!browser) return 'light';
  return window.matchMedia('(prefers-color-scheme: dark)').matches
    ? 'dark'
    : 'light';
};

// Get stored preference or fallback to system
const getInitialTheme = () => {
  if (!browser) return 'light';
  const stored = localStorage.getItem('foldline-theme');
  if (stored === 'light' || stored === 'dark') return stored;
  if (stored === 'auto') return getSystemTheme();
  return getSystemTheme(); // Default to system preference
};

// Create store
const theme = writable(getInitialTheme());

// Subscribe to changes and update localStorage + DOM
theme.subscribe((value) => {
  if (browser) {
    localStorage.setItem('foldline-theme', value);
    const resolvedTheme = value === 'auto' ? getSystemTheme() : value;
    document.documentElement.classList.toggle('dark', resolvedTheme === 'dark');
  }
});

// Listen to system theme changes
if (browser) {
  window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
    const current = localStorage.getItem('foldline-theme');
    if (current === 'auto') {
      theme.set('auto'); // Trigger re-evaluation
    }
  });
}

export default theme;
```

### **Theme Toggle Component**

```svelte
<!-- /frontend/src/lib/components/ThemeToggle.svelte -->

<script>
  import theme from '$lib/stores/theme';

  function cycleTheme() {
    const themes = ['light', 'auto', 'dark'];
    const currentIndex = themes.indexOf($theme);
    const nextIndex = (currentIndex + 1) % themes.length;
    $theme = themes[nextIndex];
  }
</script>

<button
  on:click={cycleTheme}
  aria-label="Toggle theme"
  class="theme-toggle"
>
  {#if $theme === 'light'}
    <svg aria-hidden="true"><!-- Sun icon --></svg>
  {:else if $theme === 'dark'}
    <svg aria-hidden="true"><!-- Moon icon --></svg>
  {:else}
    <svg aria-hidden="true"><!-- Auto icon --></svg>
  {/if}
  <span class="sr-only">Current theme: {$theme}</span>
</button>

<style>
  .theme-toggle {
    background: transparent;
    border: none;
    padding: var(--space-s);
    border-radius: var(--radius-md);
    cursor: pointer;
    color: var(--text-primary);
    transition: background var(--transition-quick-standard);
  }

  .theme-toggle:hover {
    background: var(--line-color);
  }

  .theme-toggle:focus-visible {
    outline: 2px solid var(--accent-orange);
    outline-offset: 2px;
  }
</style>
```

### **SSR Considerations**

Prevent flash of wrong theme on page load:

```html
<!-- /frontend/src/app.html -->
<script>
  // Run before any rendering
  (function() {
    const stored = localStorage.getItem('foldline-theme');
    const systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    const theme = stored === 'auto' || !stored
      ? (systemPrefersDark ? 'dark' : 'light')
      : stored;

    if (theme === 'dark') {
      document.documentElement.classList.add('dark');
    }
  })();
</script>
```

---

## 3. Responsive Image Strategy

### **Screenshot Optimization**

**File formats (priority order):**
1. **AVIF** (best compression, modern browsers)
2. **WebP** (good compression, wide support)
3. **PNG** (fallback, universal support)

**Implementation:**

```html
<picture>
  <source
    srcset="/screenshots/hero-dashboard.avif 1x, /screenshots/hero-dashboard@2x.avif 2x"
    type="image/avif"
  >
  <source
    srcset="/screenshots/hero-dashboard.webp 1x, /screenshots/hero-dashboard@2x.webp 2x"
    type="image/webp"
  >
  <img
    src="/screenshots/hero-dashboard.png"
    srcset="/screenshots/hero-dashboard@2x.png 2x"
    alt="Foldline dashboard showing heart rate trends and activity heatmap"
    loading="lazy"
    decoding="async"
    width="1200"
    height="800"
    class="screenshot"
  >
</picture>
```

**Benefits:**
- 60-80% smaller file size (AVIF vs PNG)
- Retina-ready (@2x variants)
- Progressive enhancement
- Lazy loading for below-the-fold images

### **File Size Targets**

| Image Type | Max Size | Recommended |
|------------|----------|-------------|
| Hero screenshot | 300 KB | 150-200 KB (AVIF) |
| Feature screenshot | 200 KB | 100-150 KB (AVIF) |
| Thumbnail | 50 KB | 30 KB (AVIF) |
| Icon (PNG) | 10 KB | 5 KB |
| Logo (SVG) | 5 KB | 2-3 KB |

### **Image Generation Script**

```bash
# /scripts/generate-screenshots.sh

#!/bin/bash
# Generates optimized screenshot variants

for file in screenshots/*.png; do
  filename=$(basename "$file" .png)

  # Generate @2x PNG (retina)
  convert "$file" -resize 200% "screenshots/${filename}@2x.png"

  # Generate WebP variants
  cwebp -q 85 "$file" -o "screenshots/${filename}.webp"
  cwebp -q 85 "screenshots/${filename}@2x.png" -o "screenshots/${filename}@2x.webp"

  # Generate AVIF variants
  avifenc -s 5 --min 20 --max 25 "$file" "screenshots/${filename}.avif"
  avifenc -s 5 --min 20 --max 25 "screenshots/${filename}@2x.png" "screenshots/${filename}@2x.avif"

  echo "✅ Generated variants for ${filename}"
done
```

---

## 4. Component Naming Conventions

### **CSS Class Naming**

**System**: Semantic, descriptive class names (not utility-first)

**Pattern**: `.component-name__element--modifier`

**Examples:**

```css
/* Component */
.hero-section { }

/* Element within component */
.hero-section__title { }
.hero-section__cta { }

/* Modifier */
.btn { }
.btn--primary { }
.btn--secondary { }
.btn--loading { }

/* State classes */
.is-active { }
.is-disabled { }
.is-loading { }
.is-visible { }
```

### **Svelte Component Naming**

**Files**: PascalCase

```
HeroSection.svelte
FeatureBlock.svelte
ThemeToggle.svelte
DataTable.svelte
```

**Props**: camelCase

```svelte
<script>
  export let title;
  export let subtitle;
  export let imageSrc;
  export let imageAlt;
  export let isLoading = false;
</script>
```

### **JavaScript/TypeScript**

```javascript
// Variables: camelCase
const userName = 'John';
const isActive = true;

// Functions: camelCase
function fetchUserData() { }
function handleSubmit() { }

// Classes: PascalCase
class DataService { }
class ThemeManager { }

// Constants: UPPER_SNAKE_CASE
const API_BASE_URL = 'https://api.example.com';
const MAX_RETRIES = 3;
```

### **CSS Custom Properties**

**Pattern**: `--category-property-modifier`

```css
/* Colors */
--color-bg-light
--color-text-dark
--data-orange-60

/* Spacing */
--space-xs
--space-xxl

/* Typography */
--font-family
--line-height-tight

/* Layout */
--container-max-width
--nav-height

/* Interaction */
--hover-lift
--transition-quick
```

---

## 5. File Organization

### **Recommended Structure**

```
/frontend/
  ├── src/
  │   ├── lib/
  │   │   ├── components/
  │   │   │   ├── marketing/
  │   │   │   │   ├── HeroSection.svelte
  │   │   │   │   ├── FeatureBlock.svelte
  │   │   │   │   └── Footer.svelte
  │   │   │   ├── ui/
  │   │   │   │   ├── Button.svelte
  │   │   │   │   ├── Input.svelte
  │   │   │   │   └── Modal.svelte
  │   │   │   └── data/
  │   │   │       ├── DataTable.svelte
  │   │   │       ├── LineChart.svelte
  │   │   │       └── Heatmap.svelte
  │   │   ├── styles/
  │   │   │   ├── fonts.css
  │   │   │   ├── linework.css
  │   │   │   └── utilities.css
  │   │   └── stores/
  │   │       └── theme.js
  │   ├── routes/
  │   │   └── +page.svelte
  │   └── app.css
  ├── static/
  │   ├── brand/
  │   │   ├── logo-light.svg
  │   │   ├── logo-dark.svg
  │   │   └── icon.svg
  │   ├── screenshots/
  │   │   ├── hero-dashboard.avif
  │   │   ├── hero-dashboard.webp
  │   │   └── hero-dashboard.png
  │   └── fonts/
  │       └── Inter-*.woff2
  └── package.json

/design/
  ├── BRAND_TOKENS.css          (Import this in app.css)
  ├── TYPOGRAPHY.css             (Import this in app.css)
  ├── LAYOUT.md                  (Documentation)
  ├── FORMS.md                   (Documentation)
  ├── DATA_VISUALIZATION.md      (Documentation)
  ├── COMPONENT_STATES.md        (Documentation)
  ├── DATA_TABLES.md             (Documentation)
  ├── LOADING_EMPTY_STATES.md    (Documentation)
  ├── ACCESSIBILITY.md           (Documentation)
  └── IMPLEMENTATION.md          (This file)
```

---

## 6. CSS Import Order

**Recommended order in `app.css`:**

```css
/* 1. Design tokens (variables first) */
@import './design/BRAND_TOKENS.css';

/* 2. Typography */
@import './design/TYPOGRAPHY.css';

/* 3. Utility styles */
@import './lib/styles/linework.css';

/* 4. Base/reset styles */
*,
*::before,
*::after {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

/* 5. Global element styles */
body {
  font-family: var(--font-family);
  color: var(--text-primary);
  background: var(--bg-primary);
  line-height: var(--line-height-normal);
}

/* 6. Component styles (scoped to components, not here) */
```

---

## 7. Performance Best Practices

### **CSS**

- ✅ Use CSS custom properties (they're fast!)
- ✅ Avoid `@import` in production (use build tool)
- ✅ Minimize specificity (single class selectors)
- ✅ Avoid universal selectors for transitions
- ❌ Don't use `!important` (except for utilities)

### **JavaScript**

- ✅ Lazy load below-the-fold components
- ✅ Use `loading="lazy"` for images
- ✅ Debounce expensive operations (search, resize)
- ✅ Use `requestAnimationFrame` for animations
- ❌ Don't animate layout properties (use `transform` instead)

### **Images**

- ✅ Use modern formats (AVIF, WebP)
- ✅ Serve responsive images (`srcset`, `<picture>`)
- ✅ Compress aggressively (80-85% quality)
- ✅ Use SVG for logos and icons
- ❌ Don't use PNGs for large screenshots

---

## 8. Browser Support

### **Target Browsers**

| Browser | Minimum Version |
|---------|----------------|
| Chrome | 90+ |
| Firefox | 88+ |
| Safari | 14+ |
| Edge | 90+ |

### **Feature Support**

**CSS:**
- ✅ CSS Custom Properties (variables)
- ✅ CSS Grid
- ✅ Flexbox
- ✅ `focus-visible` pseudo-class
- ✅ `prefers-color-scheme` media query
- ✅ `prefers-reduced-motion` media query

**JavaScript:**
- ✅ ES2020 features
- ✅ `async`/`await`
- ✅ `localStorage`
- ✅ `matchMedia`

### **Polyfills**

Not needed for target browsers. If supporting older browsers:

```javascript
// Polyfill for focus-visible (Safari < 15.4)
import 'focus-visible';
```

---

## 9. Build Configuration

### **Vite Config** (`vite.config.js`)

```javascript
import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

export default defineConfig({
  plugins: [sveltekit()],
  css: {
    devSourcemap: true,
  },
  build: {
    cssMinify: 'lightningcss',
    rollupOptions: {
      output: {
        manualChunks: {
          // Separate vendor chunks for better caching
          'vendor': ['svelte', '@sveltejs/kit'],
        },
      },
    },
  },
});
```

### **Tauri Config** (`src-tauri/tauri.conf.json`)

```json
{
  "build": {
    "beforeBuildCommand": "npm run build",
    "beforeDevCommand": "npm run dev",
    "devPath": "http://localhost:5173",
    "distDir": "../frontend/build"
  },
  "tauri": {
    "bundle": {
      "active": true,
      "icon": [
        "icons/32x32.png",
        "icons/128x128.png",
        "icons/128x128@2x.png",
        "icons/icon.png"
      ],
      "identifier": "com.foldline.app"
    }
  }
}
```

---

## 10. Development Workflow

### **Local Development**

```bash
# Install dependencies
npm install

# Start dev server (marketing site)
cd marketing && npm run dev

# Start dev server (app)
cd frontend && npm run dev

# Start Tauri dev (desktop app)
npm run tauri dev
```

### **Type Checking**

```bash
# Check TypeScript/JSDoc types
npm run check

# Watch mode
npm run check -- --watch
```

### **Linting**

```bash
# Lint JavaScript/Svelte
npm run lint

# Auto-fix
npm run lint -- --fix
```

### **Testing**

```bash
# Run unit tests
npm run test

# Run accessibility tests
npm run test:a11y
```

---

## 11. Deployment

### **Marketing Site** (Static)

```bash
# Build for production
npm run build

# Preview production build
npm run preview

# Deploy to static host (Vercel, Netlify, Cloudflare Pages)
```

### **Desktop App** (Tauri)

```bash
# Build desktop app
npm run tauri build

# Outputs:
# - macOS: .app, .dmg
# - Windows: .exe, .msi
# - Linux: .deb, .AppImage
```

---

## Summary

**Key Implementation Details:**

- **Fonts**: Self-hosted for app, Google Fonts for marketing
- **Dark mode**: localStorage with system preference fallback
- **Images**: AVIF → WebP → PNG with lazy loading
- **Naming**: Semantic CSS classes, PascalCase components
- **Performance**: Modern formats, lazy loading, minimal JS
- **Browser support**: Evergreen browsers (Chrome 90+)
- **Build**: Vite + SvelteKit + Tauri
