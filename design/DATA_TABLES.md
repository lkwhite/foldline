# 📊 Foldline Data Table Specification

## Overview

Data tables are critical for physiological tracking. Tables prioritize readability, scanability, and data density while maintaining the minimal line-drawing aesthetic.

**Design principle: "Clean grids, not heavy boxes"**

---

## 1. Base Table Structure

### **HTML Structure**

```html
<div class="table-container">
  <table class="table">
    <thead>
      <tr>
        <th>Date</th>
        <th>Metric</th>
        <th>Value</th>
        <th>Trend</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>2025-11-22</td>
        <td>Heart Rate (avg)</td>
        <td>72 bpm</td>
        <td>↑ 2%</td>
      </tr>
      <!-- More rows -->
    </tbody>
  </table>
</div>
```

### **Base Styling**

```css
.table {
  width: 100%;
  border-collapse: collapse;
  font-variant-numeric: tabular-nums;
  font-size: 16px;
}

.table-container {
  overflow-x: auto;
  border: 1.25px solid var(--line-color);
  border-radius: var(--radius-md);
}
```

---

## 2. Table Header

### **Styling**

```css
.table thead {
  border-bottom: 1.25px solid var(--line-color);
}

.table th {
  padding: var(--space-m);
  text-align: left;
  font-weight: 500;
  font-size: 14px;
  color: var(--text-primary);
  opacity: 0.7;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

/* Right-align numeric columns */
.table th.numeric {
  text-align: right;
}

/* Center-align action columns */
.table th.actions {
  text-align: center;
}
```

### **Sortable Headers**

```css
.table th.sortable {
  cursor: pointer;
  user-select: none;
  position: relative;
  padding-right: var(--space-xl);
  transition: background 150ms cubic-bezier(0.25, 0.1, 0.25, 1);
}

.table th.sortable:hover {
  background: var(--line-color);
}

/* Sort indicator */
.table th.sortable::after {
  content: '';
  position: absolute;
  right: var(--space-m);
  top: 50%;
  transform: translateY(-50%);
  width: 0;
  height: 0;
  border-left: 4px solid transparent;
  border-right: 4px solid transparent;
  border-top: 4px solid var(--text-primary);
  opacity: 0.3;
}

.table th.sortable:hover::after {
  opacity: 0.6;
}

/* Sorted ascending */
.table th.sorted-asc::after {
  border-top: 4px solid var(--accent-orange);
  opacity: 1;
}

/* Sorted descending */
.table th.sorted-desc::after {
  border-top: none;
  border-bottom: 4px solid var(--accent-orange);
}
```

### **Sticky Headers**

```css
.table.sticky-header thead {
  position: sticky;
  top: 0;
  background: var(--bg-primary);
  z-index: 10;
  box-shadow: 0 1px 0 var(--line-color);
}

/* For tables in scrollable containers */
.table-container.scrollable {
  max-height: 600px;
  overflow-y: auto;
}
```

---

## 3. Table Body

### **Rows**

```css
.table tbody tr {
  border-bottom: 1px solid var(--line-color);
  transition: background 100ms cubic-bezier(0.25, 0.1, 0.25, 1);
}

.table tbody tr:last-child {
  border-bottom: none;
}

/* Hover state */
.table tbody tr:hover {
  background: var(--line-color);
}

/* Selected state */
.table tbody tr.selected {
  background: rgba(230, 159, 0, 0.1);
  border-left: 3px solid var(--accent-orange);
}

/* Clickable rows */
.table tbody tr.clickable {
  cursor: pointer;
}

.table tbody tr.clickable:active {
  background: var(--text-primary);
  color: var(--bg-primary);
}
```

### **Cells**

```css
.table td {
  padding: var(--space-m);
  color: var(--text-primary);
  vertical-align: middle;
}

/* Numeric columns */
.table td.numeric {
  text-align: right;
  font-variant-numeric: tabular-nums;
}

/* Emphasized/primary column */
.table td.primary {
  font-weight: 500;
}

/* Secondary/muted data */
.table td.secondary {
  opacity: 0.6;
  font-size: 14px;
}

/* Actions column */
.table td.actions {
  text-align: center;
}
```

---

## 4. Table Variants

### **Compact Table**

For data-dense views:

```css
.table-compact th,
.table-compact td {
  padding: var(--space-s) var(--space-m);
  font-size: 14px;
}
```

### **Striped Rows**

**⚠️ Use sparingly** - conflicts with minimal aesthetic

```css
.table-striped tbody tr:nth-child(even) {
  background: var(--line-color);
  opacity: 0.3;
}
```

**Recommendation**: Avoid striping; use hover states instead

### **Borderless Table**

For embedded/inline data:

```css
.table-borderless {
  border: none;
}

.table-borderless tbody tr {
  border-bottom: none;
}

.table-borderless th {
  border-bottom: 1px solid var(--line-color);
}
```

---

## 5. Column Types

### **Date/Time Columns**

```css
.table td.date {
  font-variant-numeric: tabular-nums;
  white-space: nowrap;
}
```

**Format**: `YYYY-MM-DD` or `Nov 22, 2025`

### **Numeric Columns**

```css
.table td.number {
  text-align: right;
  font-variant-numeric: tabular-nums;
  font-feature-settings: "tnum";
}

/* With units */
.table td.number .unit {
  opacity: 0.5;
  margin-left: 4px;
  font-size: 0.9em;
}
```

**Example**: `72<span class="unit">bpm</span>`

### **Trend Indicators**

```css
.table td.trend {
  text-align: center;
}

.trend-indicator {
  display: inline-flex;
  align-items: center;
  gap: var(--space-xs);
  font-size: 14px;
  font-weight: 500;
}

.trend-indicator.positive {
  color: #009E73;
}

.trend-indicator.negative {
  color: #D55E00;
}

.trend-indicator.neutral {
  color: var(--text-primary);
  opacity: 0.5;
}

/* Arrow icons */
.trend-indicator::before {
  font-size: 16px;
}

.trend-indicator.positive::before {
  content: '↑';
}

.trend-indicator.negative::before {
  content: '↓';
}

.trend-indicator.neutral::before {
  content: '→';
}
```

### **Status/Tag Columns**

```css
.status-tag {
  display: inline-block;
  padding: 2px var(--space-s);
  border-radius: var(--radius-sm);
  font-size: 12px;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.status-tag.active {
  background: rgba(0, 158, 115, 0.15);
  color: #009E73;
  border: 1px solid #009E73;
}

.status-tag.inactive {
  background: var(--line-color);
  color: var(--text-primary);
  opacity: 0.6;
  border: 1px solid var(--line-color);
}

.status-tag.warning {
  background: rgba(246, 190, 0, 0.15);
  color: #F6BE00;
  border: 1px solid #F6BE00;
}

.status-tag.error {
  background: rgba(213, 94, 0, 0.15);
  color: #D55E00;
  border: 1px solid #D55E00;
}
```

### **Action Columns**

```css
.table td.actions {
  white-space: nowrap;
}

.table-action-btn {
  background: transparent;
  border: none;
  padding: var(--space-xs);
  cursor: pointer;
  color: var(--text-primary);
  opacity: 0.6;
  transition: opacity 150ms cubic-bezier(0.25, 0.1, 0.25, 1);
}

.table-action-btn:hover {
  opacity: 1;
  background: var(--line-color);
  border-radius: var(--radius-sm);
}

.table-action-btn:focus-visible {
  outline: 2px solid var(--accent-orange);
  outline-offset: 2px;
}
```

---

## 6. Empty States

```css
.table-empty {
  padding: var(--space-xxl);
  text-align: center;
  color: var(--text-primary);
  opacity: 0.6;
}

.table-empty-icon {
  font-size: 48px;
  margin-bottom: var(--space-m);
  opacity: 0.3;
}

.table-empty-message {
  font-size: 16px;
  margin-bottom: var(--space-s);
}

.table-empty-hint {
  font-size: 14px;
  opacity: 0.7;
}
```

---

## 7. Loading States

### **Skeleton Rows**

```css
.table-skeleton tbody tr {
  pointer-events: none;
}

.table-skeleton td {
  padding: var(--space-m);
}

.skeleton-cell {
  height: 16px;
  background: var(--line-color);
  border-radius: var(--radius-sm);
  animation: skeleton-pulse 2s ease-in-out infinite;
}

@keyframes skeleton-pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}
```

### **Loading Overlay**

```css
.table-container.loading {
  position: relative;
}

.table-container.loading::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: var(--bg-primary);
  opacity: 0.8;
  display: flex;
  align-items: center;
  justify-content: center;
}
```

---

## 8. Pagination

```css
.table-pagination {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--space-m);
  border-top: 1.25px solid var(--line-color);
}

.pagination-info {
  font-size: 14px;
  color: var(--text-primary);
  opacity: 0.7;
}

.pagination-controls {
  display: flex;
  gap: var(--space-s);
}

.pagination-btn {
  padding: var(--space-s) var(--space-m);
  border: 1.25px solid var(--line-color);
  border-radius: var(--radius-md);
  background: transparent;
  cursor: pointer;
  transition: all 150ms cubic-bezier(0.25, 0.1, 0.25, 1);
}

.pagination-btn:hover:not(:disabled) {
  border-color: var(--text-primary);
  background: var(--line-color);
}

.pagination-btn:disabled {
  opacity: 0.3;
  cursor: not-allowed;
}

.pagination-btn.active {
  background: var(--accent-orange);
  color: var(--bg-primary);
  border-color: var(--accent-orange);
}
```

---

## 9. Responsive Tables

### **Mobile Strategy: Horizontal Scroll**

```css
@media (max-width: 767px) {
  .table-container {
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
  }

  .table {
    min-width: 600px; /* Prevent excessive squishing */
  }
}
```

### **Mobile Strategy: Card Transformation** (Alternative)

For complex tables, transform to cards on mobile:

```css
@media (max-width: 767px) {
  .table,
  .table thead,
  .table tbody,
  .table tr,
  .table th,
  .table td {
    display: block;
  }

  .table thead {
    display: none;
  }

  .table tbody tr {
    margin-bottom: var(--space-m);
    border: 1.25px solid var(--line-color);
    border-radius: var(--radius-md);
    padding: var(--space-m);
  }

  .table td {
    padding: var(--space-s) 0;
    text-align: left;
    position: relative;
    padding-left: 40%;
  }

  .table td::before {
    content: attr(data-label);
    position: absolute;
    left: 0;
    width: 35%;
    font-weight: 500;
    opacity: 0.7;
    font-size: 14px;
  }
}
```

**HTML requirement**:
```html
<td data-label="Heart Rate">72 bpm</td>
```

---

## 10. Expandable Rows

```css
.table tbody tr.expandable {
  cursor: pointer;
}

.table tbody tr.expandable td:first-child {
  padding-left: var(--space-xl);
  position: relative;
}

/* Expand icon */
.table tbody tr.expandable td:first-child::before {
  content: '›';
  position: absolute;
  left: var(--space-m);
  transition: transform 150ms cubic-bezier(0.25, 0.1, 0.25, 1);
  font-size: 18px;
  opacity: 0.5;
}

.table tbody tr.expandable.expanded td:first-child::before {
  transform: rotate(90deg);
}

/* Expanded content row */
.table tbody tr.expanded-content {
  background: var(--line-color);
  opacity: 0.5;
}

.table tbody tr.expanded-content td {
  padding: var(--space-l);
}

.expanded-content-wrapper {
  animation: expandRow 200ms cubic-bezier(0.25, 0.1, 0.25, 1);
}

@keyframes expandRow {
  from {
    opacity: 0;
    transform: translateY(-8px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
```

---

## 11. Selection/Checkboxes

```css
.table th.select,
.table td.select {
  width: 40px;
  text-align: center;
  padding-left: var(--space-m);
  padding-right: var(--space-s);
}

/* Checkbox styling */
.table-checkbox {
  width: 18px;
  height: 18px;
  cursor: pointer;
}

/* Bulk actions toolbar */
.table-bulk-actions {
  display: none;
  padding: var(--space-m);
  background: var(--accent-orange);
  color: var(--bg-primary);
  border-radius: var(--radius-md) var(--radius-md) 0 0;
  align-items: center;
  justify-content: space-between;
}

.table-bulk-actions.visible {
  display: flex;
}

.bulk-actions-count {
  font-weight: 500;
}

.bulk-actions-buttons {
  display: flex;
  gap: var(--space-s);
}
```

---

## 12. Inline Editing

```css
.table td.editable {
  cursor: text;
  position: relative;
}

.table td.editable:hover::after {
  content: '✎';
  position: absolute;
  right: var(--space-s);
  opacity: 0.3;
  font-size: 14px;
}

.table td.editing {
  padding: 0;
}

.table td.editing input {
  width: 100%;
  padding: var(--space-m);
  border: 2px solid var(--accent-orange);
  background: var(--bg-primary);
  font-family: inherit;
  font-size: inherit;
}
```

---

## 13. Filters & Search

### **Table Toolbar**

```css
.table-toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--space-m);
  border-bottom: 1.25px solid var(--line-color);
  gap: var(--space-m);
}

.table-search {
  flex: 1;
  max-width: 400px;
}

.table-filters {
  display: flex;
  gap: var(--space-s);
}

.filter-chip {
  padding: var(--space-xs) var(--space-m);
  border: 1.25px solid var(--line-color);
  border-radius: var(--radius-full);
  background: transparent;
  cursor: pointer;
  font-size: 14px;
  transition: all 150ms cubic-bezier(0.25, 0.1, 0.25, 1);
}

.filter-chip:hover {
  border-color: var(--text-primary);
  background: var(--line-color);
}

.filter-chip.active {
  background: var(--accent-orange);
  color: var(--bg-primary);
  border-color: var(--accent-orange);
}
```

---

## 14. Fixed Columns

For wide tables with important first column:

```css
.table-fixed-column {
  overflow-x: auto;
}

.table-fixed-column table {
  table-layout: fixed;
}

.table-fixed-column th:first-child,
.table-fixed-column td:first-child {
  position: sticky;
  left: 0;
  background: var(--bg-primary);
  z-index: 5;
  box-shadow: 1px 0 0 var(--line-color);
}

.table-fixed-column thead th:first-child {
  z-index: 15; /* Above both sticky header and column */
}
```

---

## 15. Dark Mode

Tables automatically adapt via CSS variables. No special overrides needed, except:

```css
[data-theme="dark"] {
  /* Ensure sticky headers have correct background */
  .table.sticky-header thead {
    background: var(--bg-primary); /* #0C0D0E in dark mode */
  }

  /* Ensure fixed columns have correct background */
  .table-fixed-column th:first-child,
  .table-fixed-column td:first-child {
    background: var(--bg-primary);
  }
}
```

---

## 16. Accessibility

### **Required ARIA Attributes**

```html
<table class="table" role="grid" aria-label="Physiological metrics data">
  <thead>
    <tr>
      <th scope="col" aria-sort="ascending">Date</th>
      <th scope="col">Metric</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th scope="row">2025-11-22</th>
      <td>72 bpm</td>
    </tr>
  </tbody>
</table>
```

### **Keyboard Navigation**

- **Tab**: Move between sortable headers, actions, and selectable rows
- **Enter/Space**: Activate sort, expand row, or select
- **Arrow keys**: Navigate between cells (when table has `role="grid"`)

### **Screen Reader Announcements**

```html
<div role="status" aria-live="polite" class="sr-only">
  Sorted by Date, ascending. Showing 10 of 243 results.
</div>
```

---

## Summary

**Key Principles:**
- Clean lines, minimal borders (1.25px stroke weight)
- No zebra striping (use hover states instead)
- Tabular numerics for all numeric data
- Sticky headers for long tables
- Horizontal scroll on mobile (or card transformation)
- Sortable headers with clear indicators
- Accessible keyboard navigation
- Dark mode support via CSS variables
- Orange accent for selected/active states
- Loading states use skeleton screens
- Empty states are centered with helpful messaging
