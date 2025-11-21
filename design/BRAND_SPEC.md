# 📘 **Foldline Design System v0.1.0**
### *Minimal, technical, line-drawing aesthetic for data-first product*

## 1. **Brand Overview**

### **Brand Essence**
Foldline maps your physiological data the way topographic maps reveal terrain: clean, structured, understated, and precise.

**Tagline:**
**"Your physiological map, unfolded."**

### **Visual Philosophy**
- **The UI is a quiet diagram.**
- **The product is the data.**
- **Screenshots are the hero.**

Foldline's line-drawing framework exists only to support rich, interactive data exploration.

---

## 2. **Logo System**

### **Primary Logo (Simple Line Outline)**
- Tall, USGS-inspired folded-map silhouette (1:3 ratio).
- 1.25–1.5 px stroke weight (scaled for device pixel density).
- 2–4 vertical fold lines.
- No heatmap interior — purely structural.
- Corners: extremely slight rounding (2–3 px @ 1x).
- No shading, no fills.

### **Light / Dark Variants**
- Light: stroke `#111111` on `#F7F5EF`.
- Dark: stroke `#E5E5E5` on `#0C0D0E`.

### **Icon Mark**
- Cropped square version of fold lines only.
- Used for favicon, app icon base, menu icon.

### **Logo Misuse**
- No shadows
- No colors except stroke
- No fills
- No rotations
- No texture overlays
- No typography embedded inside

---

## 3. **Color System**

### **Core Palette (Neutral / Technical)**

| Role | Name | Hex |
|------|------|-----|
| Background (light) | Paper Ivory | `#F7F5EF` |
| Background (dark) | Graphite Night | `#0C0D0E` |
| Primary Text (light) | Ink Black | `#111111` |
| Primary Text (dark) | Soft Ink | `#F8F8F8` |
| Linework (light) | Fog Line | `#DCD8CA` |
| Linework (dark) | Fog Line Dark | `#3E3E3F` |
| Accent | Okabe–Ito Orange | `#E69F00` |

### **Behavior**
- Accent orange is **the only saturated UI chrome color**.
- Visualizations may use richer palettes; UI should not.
- Lines use grayscale tones only.
- Solid backgrounds only, no gradients.

---

## 4. **Typography**

### **Primary Typeface: Inter**

| Usage | Style |
|-------|--------|
| H1 | Inter Medium |
| H2 | Inter Regular / Medium |
| H3 | Inter Regular |
| Body | Inter Regular |
| Numerics | Inter Tabular Lining or Inter Mono |

**Type Scale**
- H1: 40–48 px
- H2: 28–32 px
- H3: 20–22 px
- Body: 16–18 px
- Microcopy: 13–14 px

---

## 5. **Stroke, Spacing, and Layout Rules**

### **Stroke Weight**
- All line-drawing elements: **1.25 px**

### **Spacing System (8-pt grid)**
- XS: 4
- S: 8
- M: 16
- L: 24
- XL: 32
- XXL: 48

### **Grid**
- 12-column responsive grid
- Max width: 1280–1400 px
- Mobile → single column
- Tablet: 6-column

---

## 6. **Website Visual Language**

### **Aesthetic**
- Clean, neutral surfaces
- Thin line-drawing structures
- Large whitespace zones
- Single accent color
- Line-drawing motifs as structural elements
- No blocks of color except CTA buttons
- No gradients, textures, or heavy shadows

### **Hero Section**
- Left: text → logo small, H1, subtext, CTA(s)
- Right: billboard-style screenshot with very soft shadow (blur 8–12px, opacity ~5%)
- No frames around screenshot

### **Motifs**
- Vertical fold lines
- Tall map-outline shapes behind sections
- Thin, subtle grid ticks
- Horizontal separators

All motifs must feel structural, not decorative.

---

## 7. **Dark Mode Rules**

### **Invert neutrally**
- Background → `#0C0D0E`
- Text → `#F8F8F8`
- Lines → `#3E3E3F`
- Accent orange unchanged

### **Screenshots**
- Prefer native dark screenshots if available
- Light screenshots still allowed (soft white halo around them)

---

## 8. **Screenshot Presentation Rules**

### ✔ Screenshots are the product.

**Rules**
- Always placed large (~70% width desktop)
- Always orthographic (never angled)
- Soft shadow only (blur 10–12px, 5–8% opacity)
- No frames or borders
- Generous whitespace around them
- Hover: small lift + brightness increase

### **Multi-screenshot Sections**
- Even vertical rhythm
- Thin line separators
- Simple stacking on mobile

---

## 9. **Interactive Data UI Spec (app)**

### **Charts**
- Thin grid lines
- Minimal axes
- Accent orange for highlights
- No bold outlines
- Hover → line brightens by 10–15%
- Motion: fade/slide, no bounce

### **Heatmaps**
- Low-contrast cells
- Accent used sparingly
- 2–3px grid gap
- Typography: Inter Mono or Tabular

### **Scatter + Correlation**
- Tiny points, neutral by default
- Hover → brighten cluster + show trend line
- Trend line = thin stroke

---

## 10. **Navigation + Components**

### **Nav Bar**
- Transparent background
- Thin bottom border
- Logo left, links right
- Minimal hover underline

### **Buttons**
- CTA: orange fill
- Secondary: line-outline
- Border radius: 4px max

---

## 11. **Motion Principles**

- Duration: 150–250 ms
- Easing: cubic-bezier(0.25, 0.1, 0.25, 1)
- No bounce
- No rotations
- Line motifs may animate via stroke-dashoffset subtly

---

## 12. **Assets Claude Can Generate**

### **Logo (SVG)**
- 1:3 tall map outline
- 2–4 fold lines
- 1.5px stroke
- Two exports: light & dark

### **Icons**
- Favicon
- App icon (512px base)
- Line icons for nav items

### **Color Token Files**
- CSS vars
- Tailwind plugin optional

### **Templates**
- Hero section
- Feature block
- Screenshot gallery
- Footer

---

## 13. **SvelteKit + Tauri Implementation Notes**
- Light/dark via Svelte store + `html` class toggle
- All color tokens in `:root`
- Linework defined with CSS variables (`--line-color`, etc.)
- Screenshots in `/static/screenshots/`
- Brand assets in `/static/brand/`
- Use container queries for screenshot responsiveness
