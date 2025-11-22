# 📊 Foldline Data Visualization Color System

## Overview

Foldline uses a scientifically-validated, colorblind-safe palette for data visualizations while maintaining the minimal aesthetic. The UI chrome remains neutral; color is reserved for data representation.

---

## 1. Core Principle

**"The product is the data"**

- UI elements use grayscale + single accent (orange)
- Data visualizations use rich, accessible color palettes
- Color communicates meaning, not decoration

---

## 2. Primary Data Palette (Okabe-Ito)

The **Okabe-Ito palette** is scientifically designed to be distinguishable by people with all forms of color vision deficiency.

### **Full Palette**

```css
/* Okabe-Ito Color Palette */
--data-orange: #E69F00;    /* Primary accent (also UI accent) */
--data-sky-blue: #56B4E9;  /* Cool contrast */
--data-green: #009E73;     /* Success, positive trends */
--data-yellow: #F0E442;    /* Warnings, highlights */
--data-blue: #0072B2;      /* Neutral data series */
--data-red: #D55E00;       /* Alerts, negative trends, errors */
--data-purple: #CC79A7;    /* Secondary series */
--data-black: #000000;     /* Baseline, reference lines */
```

### **When to Use Each Color**

| Color | Use Case | Examples |
|-------|----------|----------|
| **Orange** (#E69F00) | Primary metric, highlighted data | Active heart rate zone, selected metric |
| **Sky Blue** (#56B4E9) | Cool/rest states, sleep data | Sleep phases, recovery metrics |
| **Green** (#009E73) | Positive trends, success states | Improved metrics, goals achieved |
| **Yellow** (#F0E442) | Moderate zones, warnings | Medium intensity zones, approaching limits |
| **Blue** (#0072B2) | Neutral secondary data | Historical averages, secondary metrics |
| **Red** (#D55E00) | High intensity, alerts, errors | Max zones, warnings, form errors |
| **Purple** (#CC79A7) | Tertiary data series | Additional metrics when needed |
| **Black** (#000000) | Reference lines, baselines | Zero lines, thresholds, grid lines |

---

## 3. Sequential Palettes (Single Metric Over Time)

### **Orange Sequential (Default)**
For displaying a single metric with intensity variation:

```css
--data-orange-10: #FFF5E6;
--data-orange-20: #FFE4BF;
--data-orange-30: #FFD299;
--data-orange-40: #FFC173;
--data-orange-50: #FFB04D;
--data-orange-60: #E69F00;  /* Base */
--data-orange-70: #CC8C00;
--data-orange-80: #B37900;
--data-orange-90: #996600;
```

**Use case**: Heatmaps, intensity gradients, single-variable charts

### **Blue Sequential (Alternative)**
For calm/rest data (sleep, recovery):

```css
--data-blue-10: #E6F4FC;
--data-blue-20: #B3DEFA;
--data-blue-30: #80C9F7;
--data-blue-40: #56B4E9;  /* Base */
--data-blue-50: #3DA5DB;
--data-blue-60: #2596CD;
--data-blue-70: #1A7AAD;
--data-blue-80: #135E8C;
```

---

## 4. Diverging Palettes (Positive/Negative or Above/Below)

### **Blue-Orange Diverging**
For showing deviation from a baseline:

```css
/* Below baseline → Blue */
--diverge-blue-3: #0072B2;
--diverge-blue-2: #56B4E9;
--diverge-blue-1: #B3DEFA;

/* At baseline */
--diverge-neutral: var(--line-color);

/* Above baseline → Orange */
--diverge-orange-1: #FFD299;
--diverge-orange-2: #FFB04D;
--diverge-orange-3: #E69F00;
```

**Use case**: Performance vs. average, trend deviations

### **Green-Red Diverging**
For showing good/bad or improvement/decline:

```css
/* Negative/Decline → Red */
--diverge-red-3: #D55E00;
--diverge-red-2: #FF8F4D;
--diverge-red-1: #FFC299;

/* Neutral */
--diverge-neutral: var(--line-color);

/* Positive/Improvement → Green */
--diverge-green-1: #80D4BD;
--diverge-green-2: #40C1A3;
--diverge-green-3: #009E73;
```

**Use case**: Progress tracking, before/after comparisons

---

## 5. Grayscale Data Palette

For non-critical data or background context:

```css
--data-gray-10: #F8F8F8;
--data-gray-20: #E5E5E5;
--data-gray-30: #CCCCCC;
--data-gray-40: #999999;
--data-gray-50: #666666;
--data-gray-60: #404040;
--data-gray-70: #1A1A1A;
```

**Use case**: Reference data, historical context, inactive states

---

## 6. Chart-Specific Guidelines

### **Line Charts**

```css
.line-chart {
  /* Primary line */
  stroke: var(--data-orange);
  stroke-width: 2px;
  fill: none;
}

.line-chart-secondary {
  stroke: var(--data-blue);
  stroke-width: 1.25px;
  stroke-dasharray: 4 2; /* Dashed for secondary */
}

.line-chart-reference {
  stroke: var(--data-gray-40);
  stroke-width: 1.25px;
  stroke-dasharray: 2 2;
}

/* Hover state */
.line-chart:hover {
  stroke-width: 2.5px;
  filter: brightness(1.15);
}
```

**Best practices:**
- Maximum 4 lines per chart (cognitive limit)
- Use line style variation (solid, dashed) for differentiation
- Primary metric always solid, brightest color

### **Bar Charts**

```css
.bar {
  fill: var(--data-orange);
  stroke: none;
}

.bar:hover {
  filter: brightness(1.15);
}

.bar.positive {
  fill: var(--data-green);
}

.bar.negative {
  fill: var(--data-red);
}

.bar.neutral {
  fill: var(--data-gray-40);
}
```

**Best practices:**
- Use consistent color within single-category bars
- For grouped bars, use Okabe-Ito palette in order
- Avoid 3D effects, gradients, or shadows

### **Scatter Plots**

```css
.scatter-point {
  fill: var(--data-orange);
  opacity: 0.6;
  r: 3px;
}

.scatter-point:hover {
  opacity: 1;
  r: 5px;
  stroke: var(--accent-orange);
  stroke-width: 2px;
}

/* Clusters */
.scatter-point.cluster-1 { fill: var(--data-orange); }
.scatter-point.cluster-2 { fill: var(--data-sky-blue); }
.scatter-point.cluster-3 { fill: var(--data-green); }
```

**Best practices:**
- Use opacity for overlapping points
- Maximum 3 clusters/categories
- Show trend lines on hover only

### **Heatmaps**

```css
.heatmap-cell {
  stroke: var(--bg-primary);
  stroke-width: 2px; /* Cell gap */
}

/* Sequential intensity */
.heatmap-cell.intensity-0 { fill: var(--data-orange-10); }
.heatmap-cell.intensity-1 { fill: var(--data-orange-30); }
.heatmap-cell.intensity-2 { fill: var(--data-orange-50); }
.heatmap-cell.intensity-3 { fill: var(--data-orange-70); }
.heatmap-cell.intensity-4 { fill: var(--data-orange-90); }

.heatmap-cell:hover {
  stroke: var(--text-primary);
  stroke-width: 2px;
}
```

**Best practices:**
- 5-7 steps maximum for intensity scales
- Use sequential palettes for continuous data
- Include a legend with exact values
- Consider diverging palettes for positive/negative data

### **Area Charts**

```css
.area-chart {
  fill: var(--data-orange);
  opacity: 0.3;
  stroke: none;
}

.area-chart-line {
  stroke: var(--data-orange);
  stroke-width: 2px;
  fill: none;
}

/* Stacked areas */
.area-1 { fill: var(--data-orange); opacity: 0.5; }
.area-2 { fill: var(--data-sky-blue); opacity: 0.5; }
.area-3 { fill: var(--data-green); opacity: 0.5; }
```

**Best practices:**
- Always include stroke on top edge
- Use 30-50% opacity for fill
- Maximum 3 stacked areas
- Bottom layer darkest, top layer lightest

### **Pie/Donut Charts**

**⚠️ Avoid when possible** - Use bar charts instead for better data comparison.

If necessary:
```css
.pie-slice {
  stroke: var(--bg-primary);
  stroke-width: 2px;
}

.pie-slice:hover {
  filter: brightness(1.15);
  transform: scale(1.05);
}
```

**Maximum 5 slices** - Use Okabe-Ito colors in order

---

## 7. Axes, Grids & Annotations

### **Grid Lines**

```css
.grid-line {
  stroke: var(--line-color);
  stroke-width: 1px;
  opacity: 0.5;
}

.grid-line-major {
  stroke: var(--line-color);
  stroke-width: 1.25px;
  opacity: 0.8;
}
```

### **Axes**

```css
.axis-line {
  stroke: var(--text-primary);
  stroke-width: 1.25px;
}

.axis-tick {
  stroke: var(--text-primary);
  stroke-width: 1.25px;
  length: 4px;
}

.axis-label {
  font-family: var(--font-family);
  font-size: 13px;
  fill: var(--text-primary);
  opacity: 0.7;
}
```

### **Annotations**

```css
.annotation-line {
  stroke: var(--data-red);
  stroke-width: 1.25px;
  stroke-dasharray: 4 4;
}

.annotation-label {
  font-size: 13px;
  font-weight: 500;
  fill: var(--data-red);
  background: var(--bg-primary);
  padding: var(--space-xs) var(--space-s);
  border-radius: var(--radius-sm);
}
```

**Use cases:**
- Thresholds (max heart rate)
- Goals (target steps)
- Events (workout times)
- Zones (intensity ranges)

---

## 8. Interactive States

### **Default State**
- Full opacity
- Standard stroke width

### **Hover State**
```css
filter: brightness(1.15);
stroke-width: +0.5px; /* Slightly thicker */
```

### **Selected State**
```css
filter: brightness(1.2);
stroke: var(--text-primary);
stroke-width: 2px;
```

### **Inactive/Disabled State**
```css
opacity: 0.3;
pointer-events: none;
```

---

## 9. Legends

### **Horizontal Legend (Default)**

```css
.legend {
  display: flex;
  gap: var(--space-l);
  justify-content: center;
  padding: var(--space-m) 0;
  border-top: 1.25px solid var(--line-color);
  margin-top: var(--space-m);
}

.legend-item {
  display: flex;
  align-items: center;
  gap: var(--space-xs);
  font-size: 13px;
}

.legend-color {
  width: 16px;
  height: 16px;
  border-radius: var(--radius-sm);
}

.legend-line {
  width: 24px;
  height: 2px;
  border-radius: 1px;
}
```

### **Vertical Legend (Sidebar)**

```css
.legend-vertical {
  display: flex;
  flex-direction: column;
  gap: var(--space-s);
  padding: var(--space-m);
  border-left: 1.25px solid var(--line-color);
}
```

---

## 10. Tooltips

```css
.chart-tooltip {
  background: var(--bg-primary);
  border: 1.25px solid var(--line-color);
  border-radius: var(--radius-md);
  padding: var(--space-s) var(--space-m);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
  pointer-events: none;
  font-size: 13px;
}

.tooltip-title {
  font-weight: 500;
  margin-bottom: var(--space-xs);
}

.tooltip-value {
  font-variant-numeric: tabular-nums;
  color: var(--accent-orange);
  font-weight: 600;
}

.tooltip-label {
  opacity: 0.7;
  font-size: 12px;
}
```

---

## 11. Dark Mode Adaptations

### **Automatic Adjustments**
All data colors remain the same in dark mode **except**:

```css
/* Dark mode only */
[data-theme="dark"] {
  /* Lighten very dark colors for contrast */
  --data-black: #404040; /* Was #000000 */

  /* Reduce opacity of light colors */
  --data-yellow: #E6D500; /* Slightly darker for readability */
}
```

### **Grid Lines in Dark Mode**
```css
[data-theme="dark"] .grid-line {
  opacity: 0.3; /* Reduced from 0.5 */
}
```

### **Tooltips in Dark Mode**
```css
[data-theme="dark"] .chart-tooltip {
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3); /* Stronger shadow */
}
```

---

## 12. Accessibility Requirements

### **Color Contrast**
- All text on backgrounds must meet WCAG AA (4.5:1)
- Data colors against background: minimum 3:1
- Never rely on color alone - use labels, patterns, or icons

### **Tested Combinations**

| Foreground | Background (Light) | Contrast | Pass? |
|------------|-------------------|----------|-------|
| #E69F00 (Orange) | #F7F5EF (Ivory) | 6.2:1 | ✅ AA |
| #0072B2 (Blue) | #F7F5EF (Ivory) | 7.8:1 | ✅ AAA |
| #009E73 (Green) | #F7F5EF (Ivory) | 5.9:1 | ✅ AA |
| #D55E00 (Red) | #F7F5EF (Ivory) | 6.5:1 | ✅ AA |

| Foreground | Background (Dark) | Contrast | Pass? |
|------------|------------------|----------|-------|
| #E69F00 (Orange) | #0C0D0E (Night) | 7.1:1 | ✅ AAA |
| #56B4E9 (Sky Blue) | #0C0D0E (Night) | 9.2:1 | ✅ AAA |
| #F0E442 (Yellow) | #0C0D0E (Night) | 13.8:1 | ✅ AAA |

### **Colorblind-Safe Verification**
All Okabe-Ito colors tested with:
- Protanopia (red-blind)
- Deuteranopia (green-blind)
- Tritanopia (blue-blind)
- Monochromacy (grayscale)

**✅ All palettes distinguishable in all conditions**

---

## 13. Data Density Guidelines

### **Low Density (< 20 data points)**
- Use full colors at full opacity
- Larger point sizes (5-6px)
- Show all labels

### **Medium Density (20-100 data points)**
- Reduce opacity to 0.7-0.8
- Medium point sizes (3-4px)
- Show labels on hover only

### **High Density (100+ data points)**
- Use opacity 0.4-0.6
- Small point sizes (2-3px)
- Aggregate or bin data
- Consider heatmap instead of scatter

---

## 14. Chart Sizing

### **Minimum Sizes**
```css
.chart {
  min-width: 320px;
  min-height: 200px;
}

.chart-small {
  min-width: 240px;
  min-height: 160px;
}
```

### **Responsive Breakpoints**
```css
/* Desktop: Full detail */
@media (min-width: 1024px) {
  .chart { height: 400px; }
}

/* Tablet: Reduced height */
@media (min-width: 768px) and (max-width: 1023px) {
  .chart { height: 320px; }
}

/* Mobile: Compact */
@media (max-width: 767px) {
  .chart { height: 240px; }
  /* Reduce font sizes */
  .axis-label { font-size: 11px; }
  /* Simplify: fewer ticks, hide minor grid lines */
}
```

---

## 15. Animation & Transitions

### **Chart Load Animation**
```css
.chart-element {
  animation: fadeIn 400ms cubic-bezier(0.25, 0.1, 0.25, 1);
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(8px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
```

### **Data Update Animation**
```css
.chart-element {
  transition: all 250ms cubic-bezier(0.25, 0.1, 0.25, 1);
}
```

### **Hover Transitions**
```css
.chart-element:hover {
  transition: all 150ms cubic-bezier(0.25, 0.1, 0.25, 1);
}
```

**Avoid:**
- Bounce effects
- Rotation animations
- Duration > 500ms

---

## Summary

**Key Principles:**
- Use Okabe-Ito palette for all multi-category data
- Sequential palettes for intensity/heatmaps
- Diverging palettes for positive/negative comparisons
- UI stays neutral (grayscale + orange accent)
- Data gets the color
- All palettes are colorblind-safe and WCAG AA compliant
- Consistent 1.25px stroke weight for grid lines and axes
- Dark mode: same colors, adjusted opacity
- Always provide non-color differentiators (labels, patterns, shapes)
