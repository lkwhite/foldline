# 📐 Foldline SVG Pattern Library

## Overview

SVG patterns and line-drawing motifs are structural elements throughout the Foldline interface. This document defines all decorative and functional SVG patterns used in the design system.

**Principle**: "Line-drawing motifs must feel structural, not decorative."

---

## 1. Fold Line Background Motif

**Use case**: Subtle background texture for footers, empty states, section backgrounds

### **Vertical Fold Lines**

```css
.fold-lines-bg {
  background-image: repeating-linear-gradient(
    90deg,
    transparent,
    transparent 120px,
    var(--line-color) 120px,
    var(--line-color) calc(120px + 1.25px),
    transparent calc(120px + 1.25px)
  );
  opacity: 0.3;
}
```

**Visual**: Vertical lines spaced 120px apart, 1.25px wide

---

### **Horizontal Fold Lines**

```css
.fold-lines-horizontal-bg {
  background-image: repeating-linear-gradient(
    180deg,
    transparent,
    transparent 120px,
    var(--line-color) 120px,
    var(--line-color) calc(120px + 1.25px),
    transparent calc(120px + 1.25px)
  );
  opacity: 0.3;
}
```

---

### **Grid Pattern (Subtle)**

```css
.grid-pattern-bg {
  background-image:
    repeating-linear-gradient(
      90deg,
      transparent,
      transparent 120px,
      var(--line-color) 120px,
      var(--line-color) calc(120px + 1px)
    ),
    repeating-linear-gradient(
      180deg,
      transparent,
      transparent 120px,
      var(--line-color) 120px,
      var(--line-color) calc(120px + 1px)
    );
  opacity: 0.2;
}
```

**Visual**: Subtle grid, 120px squares

---

## 2. Map Outline Decorative Motif

**Use case**: Behind hero sections, large feature blocks

### **SVG Definition**

```svg
<!-- /frontend/static/patterns/map-outline.svg -->
<svg
  xmlns="http://www.w3.org/2000/svg"
  viewBox="0 0 200 600"
  fill="none"
  stroke="currentColor"
  stroke-width="1.25"
  opacity="0.15"
>
  <!-- Outer rectangle (map outline) -->
  <rect
    x="20"
    y="20"
    width="160"
    height="560"
    rx="2"
    ry="2"
  />

  <!-- Vertical fold lines -->
  <line x1="80" y1="20" x2="80" y2="580" />
  <line x1="120" y1="20" x2="120" y2="580" />

  <!-- Horizontal fold lines -->
  <line x1="20" y1="200" x2="180" y2="200" />
  <line x1="20" y1="400" x2="180" y2="400" />
</svg>
```

### **CSS Usage**

```css
.hero-section::before {
  content: '';
  position: absolute;
  top: 0;
  right: -100px;
  width: 200px;
  height: 600px;
  background-image: url('/patterns/map-outline.svg');
  background-repeat: no-repeat;
  opacity: 0.15;
  pointer-events: none;
  z-index: -1;
}
```

---

## 3. Grid Tick Pattern

**Use case**: Chart backgrounds, data table headers

### **SVG Definition**

```svg
<!-- /frontend/static/patterns/grid-ticks.svg -->
<svg
  xmlns="http://www.w3.org/2000/svg"
  viewBox="0 0 100 100"
  fill="none"
  stroke="currentColor"
  stroke-width="1"
>
  <!-- Vertical ticks -->
  <line x1="0" y1="0" x2="0" y2="5" />
  <line x1="25" y1="0" x2="25" y2="5" />
  <line x1="50" y1="0" x2="50" y2="5" />
  <line x1="75" y1="0" x2="75" y2="5" />
  <line x1="100" y1="0" x2="100" y2="5" />
</svg>
```

### **CSS Usage**

```css
.chart-axis {
  background-image: url('/patterns/grid-ticks.svg');
  background-repeat: repeat-x;
  background-position: bottom;
  opacity: 0.5;
}
```

---

## 4. Separator Line (Animated)

**Use case**: Section dividers with subtle animation

### **SVG Definition**

```svg
<!-- /frontend/static/patterns/animated-separator.svg -->
<svg
  xmlns="http://www.w3.org/2000/svg"
  viewBox="0 0 1200 2"
  fill="none"
  stroke="currentColor"
  stroke-width="1.25"
  class="separator-animated"
>
  <line x1="0" y1="1" x2="1200" y2="1" stroke-dasharray="8 4" />
</svg>
```

### **CSS Animation**

```css
.separator-animated {
  animation: dash-flow 20s linear infinite;
}

@keyframes dash-flow {
  to {
    stroke-dashoffset: -100;
  }
}
```

**Visual**: Subtle dashed line that appears to flow slowly

---

## 5. Icon System

### **Close Icon (Modal/Dialog)**

```svg
<svg
  xmlns="http://www.w3.org/2000/svg"
  viewBox="0 0 24 24"
  fill="none"
  stroke="currentColor"
  stroke-width="1.25"
  stroke-linecap="round"
  stroke-linejoin="round"
  width="24"
  height="24"
  aria-hidden="true"
>
  <line x1="18" y1="6" x2="6" y2="18" />
  <line x1="6" y1="6" x2="18" y2="18" />
</svg>
```

---

### **Chevron Down (Dropdown)**

```svg
<svg
  xmlns="http://www.w3.org/2000/svg"
  viewBox="0 0 16 16"
  fill="none"
  stroke="currentColor"
  stroke-width="1.25"
  stroke-linecap="round"
  stroke-linejoin="round"
  width="16"
  height="16"
  aria-hidden="true"
>
  <polyline points="4,6 8,10 12,6" />
</svg>
```

---

### **Checkmark (Success, Checkbox)**

```svg
<svg
  xmlns="http://www.w3.org/2000/svg"
  viewBox="0 0 16 16"
  fill="none"
  stroke="currentColor"
  stroke-width="2"
  stroke-linecap="round"
  stroke-linejoin="round"
  width="16"
  height="16"
  aria-hidden="true"
>
  <polyline points="3,8 6,11 13,4" />
</svg>
```

---

### **Arrow Right (Navigation, CTA)**

```svg
<svg
  xmlns="http://www.w3.org/2000/svg"
  viewBox="0 0 24 24"
  fill="none"
  stroke="currentColor"
  stroke-width="1.25"
  stroke-linecap="round"
  stroke-linejoin="round"
  width="24"
  height="24"
  aria-hidden="true"
>
  <line x1="5" y1="12" x2="19" y2="12" />
  <polyline points="12,5 19,12 12,19" />
</svg>
```

---

### **Calendar (Date Picker)**

```svg
<svg
  xmlns="http://www.w3.org/2000/svg"
  viewBox="0 0 24 24"
  fill="none"
  stroke="currentColor"
  stroke-width="1.25"
  stroke-linecap="round"
  stroke-linejoin="round"
  width="24"
  height="24"
  aria-hidden="true"
>
  <rect x="3" y="4" width="18" height="18" rx="2" ry="2" />
  <line x1="16" y1="2" x2="16" y2="6" />
  <line x1="8" y1="2" x2="8" y2="6" />
  <line x1="3" y1="10" x2="21" y2="10" />
</svg>
```

---

### **Search (Input, Button)**

```svg
<svg
  xmlns="http://www.w3.org/2000/svg"
  viewBox="0 0 24 24"
  fill="none"
  stroke="currentColor"
  stroke-width="1.25"
  stroke-linecap="round"
  stroke-linejoin="round"
  width="24"
  height="24"
  aria-hidden="true"
>
  <circle cx="11" cy="11" r="8" />
  <line x1="21" y1="21" x2="16.65" y2="16.65" />
</svg>
```

---

### **Warning/Alert Triangle**

```svg
<svg
  xmlns="http://www.w3.org/2000/svg"
  viewBox="0 0 24 24"
  fill="none"
  stroke="currentColor"
  stroke-width="1.25"
  stroke-linecap="round"
  stroke-linejoin="round"
  width="24"
  height="24"
  aria-hidden="true"
>
  <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z" />
  <line x1="12" y1="9" x2="12" y2="13" />
  <line x1="12" y1="17" x2="12.01" y2="17" />
</svg>
```

---

### **Info Circle**

```svg
<svg
  xmlns="http://www.w3.org/2000/svg"
  viewBox="0 0 24 24"
  fill="none"
  stroke="currentColor"
  stroke-width="1.25"
  stroke-linecap="round"
  stroke-linejoin="round"
  width="24"
  height="24"
  aria-hidden="true"
>
  <circle cx="12" cy="12" r="10" />
  <line x1="12" y1="16" x2="12" y2="12" />
  <line x1="12" y1="8" x2="12.01" y2="8" />
</svg>
```

---

### **Menu (Hamburger)**

```svg
<svg
  xmlns="http://www.w3.org/2000/svg"
  viewBox="0 0 24 24"
  fill="none"
  stroke="currentColor"
  stroke-width="1.25"
  stroke-linecap="round"
  stroke-linejoin="round"
  width="24"
  height="24"
  aria-hidden="true"
>
  <line x1="3" y1="6" x2="21" y2="6" />
  <line x1="3" y1="12" x2="21" y2="12" />
  <line x1="3" y1="18" x2="21" y2="18" />
</svg>
```

---

## 6. Data Visualization Icons

### **Trend Up**

```svg
<svg
  xmlns="http://www.w3.org/2000/svg"
  viewBox="0 0 24 24"
  fill="none"
  stroke="currentColor"
  stroke-width="1.25"
  stroke-linecap="round"
  stroke-linejoin="round"
  width="24"
  height="24"
>
  <polyline points="23,6 13.5,15.5 8.5,10.5 1,18" />
  <polyline points="17,6 23,6 23,12" />
</svg>
```

---

### **Trend Down**

```svg
<svg
  xmlns="http://www.w3.org/2000/svg"
  viewBox="0 0 24 24"
  fill="none"
  stroke="currentColor"
  stroke-width="1.25"
  stroke-linecap="round"
  stroke-linejoin="round"
  width="24"
  height="24"
>
  <polyline points="23,18 13.5,8.5 8.5,13.5 1,6" />
  <polyline points="17,18 23,18 23,12" />
</svg>
```

---

### **Activity (Heart Rate)**

```svg
<svg
  xmlns="http://www.w3.org/2000/svg"
  viewBox="0 0 24 24"
  fill="none"
  stroke="currentColor"
  stroke-width="1.25"
  stroke-linecap="round"
  stroke-linejoin="round"
  width="24"
  height="24"
>
  <polyline points="22,12 18,12 15,21 9,3 6,12 2,12" />
</svg>
```

---

## 7. Empty State Illustrations

### **No Data (Simple)**

```svg
<svg
  xmlns="http://www.w3.org/2000/svg"
  viewBox="0 0 200 200"
  fill="none"
  stroke="currentColor"
  stroke-width="1.25"
  opacity="0.2"
>
  <!-- Chart outline -->
  <rect x="20" y="40" width="160" height="120" rx="2" />

  <!-- Empty chart bars -->
  <line x1="40" y1="140" x2="40" y2="140" stroke-dasharray="2 2" />
  <line x1="80" y1="120" x2="80" y2="140" stroke-dasharray="2 2" />
  <line x1="120" y1="100" x2="120" y2="140" stroke-dasharray="2 2" />
  <line x1="160" y1="80" x2="160" y2="140" stroke-dasharray="2 2" />

  <!-- X axis -->
  <line x1="20" y1="160" x2="180" y2="160" />
</svg>
```

---

## 8. Usage Guidelines

### **Stroke Width**

**All SVG elements must use consistent stroke width:**
- Line-drawing icons: `1.25px`
- Logos: `1.25px`
- Decorative patterns: `1px` (subtler)
- Emphasis elements: `2px`

### **Color**

**Icons inherit current color:**

```css
.icon {
  color: var(--text-primary);
}

.icon-accent {
  color: var(--accent-orange);
}

.icon-success {
  color: var(--data-green);
}

.icon-error {
  color: var(--data-red);
}
```

**SVG implementation:**

```svg
<svg stroke="currentColor">
  <!-- SVG content -->
</svg>
```

### **Sizing**

Standard icon sizes:

```css
.icon-xs { width: 12px; height: 12px; }
.icon-sm { width: 16px; height: 16px; }
.icon-md { width: 24px; height: 24px; }  /* Default */
.icon-lg { width: 32px; height: 32px; }
.icon-xl { width: 48px; height: 48px; }
```

### **Accessibility**

**Decorative icons:**

```html
<svg aria-hidden="true">
  <!-- Icon content -->
</svg>
```

**Functional icons:**

```html
<button aria-label="Close modal">
  <svg aria-hidden="true">
    <!-- X icon -->
  </svg>
</button>
```

---

## 9. SVG Optimization

### **Manual Optimization Checklist**

- [ ] Remove unnecessary `id` attributes
- [ ] Remove `<title>` and `<desc>` (use ARIA labels instead)
- [ ] Remove comments
- [ ] Remove unused definitions
- [ ] Simplify paths when possible
- [ ] Use `viewBox` instead of `width`/`height` for scalability
- [ ] Round coordinates to 2 decimal places max

### **Automated Optimization**

Use SVGO:

```bash
# Install
npm install -g svgo

# Optimize single file
svgo input.svg -o output.svg

# Optimize all SVGs in directory
svgo -f ./static/icons
```

**SVGO config** (`.svgorc.json`):

```json
{
  "plugins": [
    {
      "name": "preset-default",
      "params": {
        "overrides": {
          "removeViewBox": false,
          "cleanupIDs": {
            "remove": true,
            "minify": false
          }
        }
      }
    },
    "removeDimensions"
  ]
}
```

---

## 10. Component Integration

### **Svelte Icon Component**

```svelte
<!-- /frontend/src/lib/components/ui/Icon.svelte -->

<script>
  export let name = 'chevron-down';
  export let size = 24;
  export let color = 'currentColor';
  export let ariaLabel = undefined;

  // Icon path imports
  import ChevronDown from '$lib/icons/chevron-down.svg?raw';
  import Close from '$lib/icons/close.svg?raw';
  // ... more icons

  const icons = {
    'chevron-down': ChevronDown,
    'close': Close,
    // ... more mappings
  };

  $: icon = icons[name] || icons['chevron-down'];
</script>

<span
  class="icon"
  style="--size: {size}px; --color: {color};"
  aria-label={ariaLabel}
  aria-hidden={!ariaLabel}
>
  {@html icon}
</span>

<style>
  .icon {
    display: inline-flex;
    width: var(--size);
    height: var(--size);
    color: var(--color);
  }

  .icon :global(svg) {
    width: 100%;
    height: 100%;
  }
</style>
```

**Usage:**

```svelte
<Icon name="close" size={24} ariaLabel="Close modal" />
<Icon name="chevron-down" size={16} />
```

---

## Summary

**SVG Pattern Library Includes:**

- **Background motifs**: Fold lines, grid patterns
- **Decorative elements**: Map outlines, separators
- **Icon system**: 20+ line-drawing icons at 1.25px stroke
- **Data viz icons**: Trends, activity indicators
- **Empty state illustrations**: Simple, consistent style
- **Svelte component**: Reusable `<Icon>` component

**Key Principles:**
- Consistent 1.25px stroke weight
- Minimal, structural aesthetic
- Inherit `currentColor` for flexibility
- Optimized for performance (SVGO)
- Accessible (ARIA labels, semantic HTML)
- Dark mode compatible (no hard-coded colors)
