# ⏳ Foldline Loading & Empty State Patterns

## Overview

Loading and empty states provide crucial feedback to users. These patterns maintain the minimal aesthetic while clearly communicating system status.

---

## 1. Loading States

### **Spinner (Primary)**

**Use case**: Button loading, inline actions, small components

```css
.spinner {
  display: inline-block;
  width: 24px;
  height: 24px;
  border: 2px solid var(--line-color);
  border-top-color: var(--accent-orange);
  border-radius: var(--radius-full);
  animation: spin 600ms linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Variants */
.spinner-sm {
  width: 16px;
  height: 16px;
  border-width: 1.5px;
}

.spinner-lg {
  width: 32px;
  height: 32px;
  border-width: 3px;
}

.spinner-xl {
  width: 48px;
  height: 48px;
  border-width: 3px;
}
```

**HTML**:
```html
<div class="spinner" role="status" aria-label="Loading..."></div>
```

---

### **Progress Bar**

**Use case**: File uploads, data syncing, known duration tasks

```css
.progress {
  width: 100%;
  height: 4px;
  background: var(--line-color);
  border-radius: var(--radius-full);
  overflow: hidden;
}

.progress-bar {
  height: 100%;
  background: var(--accent-orange);
  border-radius: var(--radius-full);
  transition: width 250ms cubic-bezier(0.25, 0.1, 0.25, 1);
  width: var(--progress-value, 0%);
}

/* With label */
.progress-wrapper {
  width: 100%;
}

.progress-label {
  display: flex;
  justify-content: space-between;
  margin-bottom: var(--space-xs);
  font-size: 14px;
  color: var(--text-primary);
  opacity: 0.7;
}
```

**HTML**:
```html
<div class="progress-wrapper">
  <div class="progress-label">
    <span>Syncing data...</span>
    <span>67%</span>
  </div>
  <div class="progress">
    <div class="progress-bar" style="--progress-value: 67%"></div>
  </div>
</div>
```

---

### **Indeterminate Progress Bar**

**Use case**: Unknown duration, background processing

```css
.progress-bar.indeterminate {
  width: 30%;
  animation: progress-indeterminate 1.5s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

@keyframes progress-indeterminate {
  0% { transform: translateX(-100%); }
  100% { transform: translateX(400%); }
}
```

---

### **Skeleton Screen**

**Use case**: Page load, content placeholders, table loading

```css
.skeleton {
  background: var(--line-color);
  border-radius: var(--radius-sm);
  animation: skeleton-pulse 2s ease-in-out infinite;
}

@keyframes skeleton-pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

/* Text skeleton */
.skeleton-text {
  height: 16px;
  width: 100%;
  margin-bottom: var(--space-s);
}

.skeleton-text.short {
  width: 60%;
}

.skeleton-text.medium {
  width: 80%;
}

/* Heading skeleton */
.skeleton-heading {
  height: 24px;
  width: 40%;
  margin-bottom: var(--space-m);
}

/* Circle skeleton (avatar, icon) */
.skeleton-circle {
  width: 40px;
  height: 40px;
  border-radius: var(--radius-full);
}

/* Rectangle skeleton (image, chart) */
.skeleton-rect {
  width: 100%;
  height: 200px;
  border-radius: var(--radius-md);
}

/* Card skeleton */
.skeleton-card {
  border: 1.25px solid var(--line-color);
  border-radius: var(--radius-md);
  padding: var(--space-l);
}
```

**Example - Card Skeleton**:
```html
<div class="skeleton-card">
  <div class="skeleton-heading"></div>
  <div class="skeleton-text"></div>
  <div class="skeleton-text medium"></div>
  <div class="skeleton-text short"></div>
</div>
```

---

### **Table Skeleton**

```css
.table-skeleton tbody tr {
  pointer-events: none;
}

.skeleton-cell {
  height: 16px;
  background: var(--line-color);
  border-radius: var(--radius-sm);
  animation: skeleton-pulse 2s ease-in-out infinite;
}

/* Stagger animation for visual interest */
.skeleton-cell:nth-child(1) { animation-delay: 0ms; }
.skeleton-cell:nth-child(2) { animation-delay: 100ms; }
.skeleton-cell:nth-child(3) { animation-delay: 200ms; }
.skeleton-cell:nth-child(4) { animation-delay: 300ms; }
```

---

### **Button Loading State**

```css
.btn.loading {
  position: relative;
  color: transparent;
  pointer-events: none;
}

.btn.loading::after {
  content: '';
  position: absolute;
  width: 16px;
  height: 16px;
  border: 2px solid currentColor;
  border-top-color: transparent;
  border-radius: var(--radius-full);
  animation: spin 600ms linear infinite;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

/* Primary button - white spinner */
.btn-primary.loading::after {
  border-color: var(--bg-primary);
  border-top-color: transparent;
}

/* Secondary button - text color spinner */
.btn-secondary.loading::after {
  border-color: var(--text-primary);
  border-top-color: transparent;
}
```

---

### **Inline Loading Indicator**

**Use case**: Loading text mid-sentence, saving indicators

```css
.loading-dots {
  display: inline-block;
}

.loading-dots::after {
  content: '';
  animation: loading-dots 1.5s infinite;
}

@keyframes loading-dots {
  0%, 20% { content: ''; }
  40% { content: '.'; }
  60% { content: '..'; }
  80%, 100% { content: '...'; }
}
```

**HTML**:
```html
<span>Saving<span class="loading-dots"></span></span>
```

---

### **Full Page Loading**

**Use case**: Initial app load, page transitions

```css
.page-loader {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: var(--bg-primary);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  z-index: 9999;
}

.page-loader-spinner {
  width: 48px;
  height: 48px;
  border: 3px solid var(--line-color);
  border-top-color: var(--accent-orange);
  border-radius: var(--radius-full);
  animation: spin 600ms linear infinite;
}

.page-loader-text {
  margin-top: var(--space-l);
  font-size: 16px;
  color: var(--text-primary);
  opacity: 0.7;
}
```

---

### **Overlay Loading**

**Use case**: Form submission, modal actions

```css
.loading-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: var(--bg-primary);
  opacity: 0.9;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 100;
  border-radius: inherit;
}

.loading-overlay .spinner {
  width: 32px;
  height: 32px;
  border-width: 3px;
}
```

---

### **Shimmer Effect** (Alternative to Pulse)

**Use case**: Premium feel, marketing pages

```css
.skeleton-shimmer {
  background: linear-gradient(
    90deg,
    var(--line-color) 0%,
    var(--text-primary) 20%,
    var(--line-color) 40%,
    var(--line-color) 100%
  );
  background-size: 200% 100%;
  animation: shimmer 2s infinite;
  opacity: 0.1;
}

@keyframes shimmer {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}
```

---

## 2. Empty States

### **General Empty State**

```css
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: var(--space-xxl) var(--space-l);
  text-align: center;
  min-height: 320px;
}

.empty-state-icon {
  width: 64px;
  height: 64px;
  margin-bottom: var(--space-l);
  opacity: 0.2;
  color: var(--text-primary);
}

.empty-state-title {
  font-size: 18px;
  font-weight: 500;
  margin-bottom: var(--space-s);
  color: var(--text-primary);
}

.empty-state-message {
  font-size: 16px;
  color: var(--text-primary);
  opacity: 0.6;
  max-width: 400px;
  margin-bottom: var(--space-l);
  line-height: 1.5;
}

.empty-state-action {
  /* CTA button styling */
  background: var(--accent-orange);
  color: var(--bg-primary);
  border: none;
  padding: var(--space-m) var(--space-xl);
  border-radius: var(--radius-md);
  font-weight: 500;
  cursor: pointer;
}
```

**HTML**:
```html
<div class="empty-state">
  <svg class="empty-state-icon" aria-hidden="true">
    <!-- Icon SVG -->
  </svg>
  <h3 class="empty-state-title">No data yet</h3>
  <p class="empty-state-message">
    Connect your device to start tracking your physiological metrics.
  </p>
  <button class="empty-state-action">Connect Device</button>
</div>
```

---

### **Empty Table**

```css
.table-empty {
  padding: var(--space-xxl);
  text-align: center;
  color: var(--text-primary);
}

.table-empty-icon {
  font-size: 48px;
  margin-bottom: var(--space-m);
  opacity: 0.2;
}

.table-empty-message {
  font-size: 16px;
  margin-bottom: var(--space-s);
  opacity: 0.7;
}

.table-empty-hint {
  font-size: 14px;
  opacity: 0.5;
}
```

---

### **Empty Search Results**

```css
.search-empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: var(--space-xxl) var(--space-l);
  text-align: center;
}

.search-empty-icon {
  width: 48px;
  height: 48px;
  margin-bottom: var(--space-m);
  opacity: 0.2;
}

.search-empty-title {
  font-size: 18px;
  font-weight: 500;
  margin-bottom: var(--space-s);
}

.search-empty-query {
  font-family: var(--font-mono);
  background: var(--line-color);
  padding: 2px var(--space-s);
  border-radius: var(--radius-sm);
  margin: 0 4px;
}

.search-empty-suggestions {
  margin-top: var(--space-m);
  font-size: 14px;
  opacity: 0.7;
}

.search-empty-suggestions ul {
  list-style: none;
  padding: 0;
  margin-top: var(--space-s);
}

.search-empty-suggestions li {
  margin-bottom: var(--space-xs);
}
```

**HTML**:
```html
<div class="search-empty">
  <svg class="search-empty-icon"><!-- Icon --></svg>
  <p class="search-empty-title">
    No results found for <span class="search-empty-query">"cardio zone 5"</span>
  </p>
  <div class="search-empty-suggestions">
    <p>Suggestions:</p>
    <ul>
      <li>Check your spelling</li>
      <li>Try different keywords</li>
      <li>Use more general terms</li>
    </ul>
  </div>
</div>
```

---

### **Empty Chart/Graph**

```css
.chart-empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 300px;
  border: 1.25px dashed var(--line-color);
  border-radius: var(--radius-md);
  background: var(--bg-primary);
}

.chart-empty-icon {
  width: 64px;
  height: 64px;
  margin-bottom: var(--space-m);
  opacity: 0.15;
  stroke: var(--text-primary);
  fill: none;
  stroke-width: 1.25px;
}

.chart-empty-message {
  font-size: 16px;
  color: var(--text-primary);
  opacity: 0.6;
}
```

---

### **First-Time User Empty State**

**Use case**: Onboarding, encouraging first action

```css
.welcome-empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: var(--space-xxl);
  text-align: center;
  background: var(--bg-primary);
  border: 1.25px solid var(--line-color);
  border-radius: var(--radius-md);
}

.welcome-empty-state-illustration {
  width: 200px;
  height: 150px;
  margin-bottom: var(--space-l);
  opacity: 0.3;
}

.welcome-empty-state-title {
  font-size: 24px;
  font-weight: 500;
  margin-bottom: var(--space-m);
}

.welcome-empty-state-message {
  font-size: 16px;
  opacity: 0.7;
  max-width: 480px;
  margin-bottom: var(--space-xl);
  line-height: 1.6;
}

.welcome-empty-state-actions {
  display: flex;
  gap: var(--space-m);
}
```

---

### **Error Empty State**

**Use case**: Failed data fetch, connection errors

```css
.error-empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: var(--space-xxl);
  text-align: center;
}

.error-empty-state-icon {
  width: 64px;
  height: 64px;
  margin-bottom: var(--space-l);
  color: #D55E00;
  opacity: 0.5;
}

.error-empty-state-title {
  font-size: 18px;
  font-weight: 500;
  margin-bottom: var(--space-s);
  color: #D55E00;
}

.error-empty-state-message {
  font-size: 16px;
  opacity: 0.7;
  max-width: 400px;
  margin-bottom: var(--space-l);
}

.error-empty-state-action {
  /* Secondary button styling */
  background: transparent;
  color: var(--text-primary);
  border: 1.25px solid var(--line-color);
  padding: var(--space-m) var(--space-xl);
  border-radius: var(--radius-md);
  font-weight: 500;
  cursor: pointer;
}
```

---

### **No Permission Empty State**

```css
.no-permission-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: var(--space-xxl);
  text-align: center;
}

.no-permission-state-icon {
  width: 64px;
  height: 64px;
  margin-bottom: var(--space-l);
  opacity: 0.2;
}

.no-permission-state-title {
  font-size: 18px;
  font-weight: 500;
  margin-bottom: var(--space-s);
}

.no-permission-state-message {
  font-size: 16px;
  opacity: 0.6;
  max-width: 400px;
}
```

---

## 3. Transition Between States

### **Loading → Content**

```css
.content-loaded {
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

### **Loading → Error**

```css
.error-appeared {
  animation: slideIn 300ms cubic-bezier(0.25, 0.1, 0.25, 1);
}

@keyframes slideIn {
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

## 4. Accessibility

### **Loading Indicators**

```html
<!-- Spinner -->
<div class="spinner" role="status" aria-label="Loading data"></div>

<!-- With live region -->
<div role="status" aria-live="polite" aria-atomic="true">
  <span class="spinner"></span>
  <span class="sr-only">Loading your health metrics...</span>
</div>
```

### **Empty States**

```html
<div class="empty-state" role="status">
  <svg class="empty-state-icon" aria-hidden="true"><!-- Icon --></svg>
  <h3 class="empty-state-title">No data yet</h3>
  <p class="empty-state-message">
    Connect your device to start tracking.
  </p>
  <button class="empty-state-action">Connect Device</button>
</div>
```

### **Screen Reader Only Text**

```css
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}
```

---

## 5. Dark Mode

All loading and empty states automatically adapt via CSS variables. No special overrides needed, except:

```css
[data-theme="dark"] {
  /* Skeleton slightly more visible in dark mode */
  .skeleton {
    opacity: 0.3;
  }

  /* Page loader background */
  .page-loader {
    background: var(--bg-primary); /* #0C0D0E */
  }
}
```

---

## Summary

**Loading States:**
- **Spinner**: Quick actions, buttons, inline (600ms rotation)
- **Progress bar**: Known duration tasks, file uploads
- **Skeleton screen**: Page/content loading, tables
- **Overlay**: Modal actions, form submissions

**Empty States:**
- **General**: No data yet, first-time experience
- **Search**: No results found
- **Error**: Failed fetch, connection issues
- **Permission**: Access denied, feature locked

**Key Principles:**
- Always provide visual feedback within 100ms
- Use skeleton screens for content > 500ms load time
- Animated spinners use 600ms rotation (not too fast, not too slow)
- Empty states include helpful messaging and CTAs
- All states are accessible with proper ARIA labels
- Transitions are smooth (400ms fade in)
- Dark mode supported automatically
