# 🎛️ Foldline Component State System

## Overview

All interactive components have consistent, predictable state behaviors. This document defines the exact visual specifications for each state across all component types.

---

## 1. Universal State Types

All interactive components support these states:

1. **Default** - Resting state, no interaction
2. **Hover** - Mouse/pointer over element
3. **Active** - Element being clicked/pressed
4. **Focus** - Keyboard focus (accessibility critical)
5. **Disabled** - Non-interactive, grayed out
6. **Loading** - Processing, awaiting response
7. **Error** - Validation failed, attention needed
8. **Success** - Validation passed (use sparingly)

---

## 2. State Specifications by Component

### **Buttons**

#### **Primary Button (CTA)**

```css
/* Default */
.btn-primary {
  background: var(--accent-orange);
  color: var(--bg-primary);
  border: none;
  padding: var(--space-m) var(--space-xl);
  border-radius: var(--radius-md);
  font-weight: 500;
  cursor: pointer;
  transition: all 150ms cubic-bezier(0.25, 0.1, 0.25, 1);
}

/* Hover */
.btn-primary:hover {
  filter: brightness(1.1);
  transform: translateY(-1px);
}

/* Active (pressed) */
.btn-primary:active {
  filter: brightness(0.95);
  transform: translateY(1px);
}

/* Focus */
.btn-primary:focus-visible {
  outline: 2px solid var(--accent-orange);
  outline-offset: 2px;
}

/* Disabled */
.btn-primary:disabled {
  opacity: 0.4;
  cursor: not-allowed;
  transform: none;
}

/* Loading */
.btn-primary.loading {
  position: relative;
  color: transparent;
  pointer-events: none;
}

.btn-primary.loading::after {
  content: '';
  position: absolute;
  width: 16px;
  height: 16px;
  border: 2px solid var(--bg-primary);
  border-top-color: transparent;
  border-radius: var(--radius-full);
  animation: spin 600ms linear infinite;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}
```

#### **Secondary Button**

```css
/* Default */
.btn-secondary {
  background: transparent;
  color: var(--text-primary);
  border: 1.25px solid var(--line-color);
  padding: var(--space-m) var(--space-xl);
  border-radius: var(--radius-md);
  font-weight: 500;
  cursor: pointer;
  transition: all 150ms cubic-bezier(0.25, 0.1, 0.25, 1);
}

/* Hover */
.btn-secondary:hover {
  border-color: var(--text-primary);
  background: var(--line-color);
}

/* Active */
.btn-secondary:active {
  background: var(--text-primary);
  color: var(--bg-primary);
}

/* Focus */
.btn-secondary:focus-visible {
  outline: 2px solid var(--accent-orange);
  outline-offset: 2px;
}

/* Disabled */
.btn-secondary:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}
```

#### **Icon Button**

```css
/* Default */
.btn-icon {
  background: transparent;
  border: none;
  padding: var(--space-s);
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all 150ms cubic-bezier(0.25, 0.1, 0.25, 1);
  color: var(--text-primary);
}

/* Hover */
.btn-icon:hover {
  background: var(--line-color);
}

/* Active */
.btn-icon:active {
  background: var(--text-primary);
  color: var(--bg-primary);
}

/* Focus */
.btn-icon:focus-visible {
  outline: 2px solid var(--accent-orange);
  outline-offset: 2px;
}
```

---

### **Links**

```css
/* Default */
.link {
  color: var(--text-primary);
  text-decoration: none;
  position: relative;
  transition: color 150ms cubic-bezier(0.25, 0.1, 0.25, 1);
}

.link::after {
  content: '';
  position: absolute;
  bottom: -2px;
  left: 0;
  width: 100%;
  height: 1px;
  background: var(--text-primary);
  opacity: 0.3;
  transition: opacity 150ms cubic-bezier(0.25, 0.1, 0.25, 1);
}

/* Hover */
.link:hover::after {
  opacity: 1;
}

/* Active */
.link:active {
  color: var(--accent-orange);
}

/* Focus */
.link:focus-visible {
  outline: 2px solid var(--accent-orange);
  outline-offset: 2px;
  border-radius: 2px;
}

/* Visited (optional, usually omitted for apps) */
.link:visited {
  color: var(--text-primary); /* Same as default */
}
```

---

### **Form Inputs**

See `FORMS.md` for complete specifications. Summary:

```css
/* Default */
border: 1.25px solid var(--line-color);

/* Hover */
border-color: var(--text-primary) at 60% opacity;

/* Focus */
border: 2px solid var(--accent-orange);
outline: none;

/* Error */
border: 2px solid #D55E00;

/* Success */
border: 2px solid #009E73;

/* Disabled */
opacity: 0.4;
cursor: not-allowed;
```

---

### **Cards**

```css
/* Default */
.card {
  background: var(--bg-primary);
  border: 1.25px solid var(--line-color);
  border-radius: var(--radius-md);
  padding: var(--space-l);
  transition: all 200ms cubic-bezier(0.25, 0.1, 0.25, 1);
}

/* Hover (if clickable) */
.card.clickable:hover {
  border-color: var(--text-primary);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
  transform: translateY(-2px);
  cursor: pointer;
}

/* Active */
.card.clickable:active {
  transform: translateY(0);
}

/* Focus */
.card.clickable:focus-visible {
  outline: 2px solid var(--accent-orange);
  outline-offset: 2px;
}

/* Selected */
.card.selected {
  border-color: var(--accent-orange);
  border-width: 2px;
}

/* Disabled */
.card.disabled {
  opacity: 0.4;
  pointer-events: none;
}
```

---

### **Navigation Items**

```css
/* Default */
.nav-item {
  color: var(--text-primary);
  padding: var(--space-s) var(--space-m);
  border-radius: var(--radius-md);
  text-decoration: none;
  transition: all 150ms cubic-bezier(0.25, 0.1, 0.25, 1);
  position: relative;
}

/* Hover */
.nav-item:hover {
  background: var(--line-color);
}

/* Active (pressed) */
.nav-item:active {
  background: var(--text-primary);
  color: var(--bg-primary);
}

/* Focus */
.nav-item:focus-visible {
  outline: 2px solid var(--accent-orange);
  outline-offset: 2px;
}

/* Current page */
.nav-item.current {
  color: var(--accent-orange);
  font-weight: 500;
}

.nav-item.current::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: var(--space-m);
  right: var(--space-m);
  height: 2px;
  background: var(--accent-orange);
}
```

---

### **Tabs**

```css
/* Default */
.tab {
  color: var(--text-primary);
  opacity: 0.6;
  padding: var(--space-m) var(--space-l);
  border: none;
  border-bottom: 2px solid transparent;
  background: transparent;
  cursor: pointer;
  transition: all 150ms cubic-bezier(0.25, 0.1, 0.25, 1);
}

/* Hover */
.tab:hover {
  opacity: 1;
  background: var(--line-color);
}

/* Active (selected) */
.tab.active {
  opacity: 1;
  font-weight: 500;
  border-bottom-color: var(--accent-orange);
}

/* Focus */
.tab:focus-visible {
  outline: 2px solid var(--accent-orange);
  outline-offset: -2px;
}

/* Disabled */
.tab:disabled {
  opacity: 0.3;
  cursor: not-allowed;
}
```

---

### **Dropdown Menu Items**

```css
/* Default */
.dropdown-item {
  padding: var(--space-s) var(--space-m);
  cursor: pointer;
  transition: background 100ms cubic-bezier(0.25, 0.1, 0.25, 1);
}

/* Hover */
.dropdown-item:hover {
  background: var(--accent-orange);
  color: var(--bg-primary);
}

/* Active (pressed) */
.dropdown-item:active {
  filter: brightness(0.95);
}

/* Focus (keyboard navigation) */
.dropdown-item:focus {
  background: var(--line-color);
  outline: none;
}

/* Selected (current value) */
.dropdown-item.selected {
  background: var(--line-color);
  font-weight: 500;
}

/* Disabled */
.dropdown-item:disabled {
  opacity: 0.4;
  cursor: not-allowed;
  pointer-events: none;
}
```

---

### **Toggle Switch**

```css
/* Default (off) */
.toggle-track {
  background: transparent;
  border: 1.25px solid var(--line-color);
}

.toggle-track::after {
  background: var(--text-primary);
  left: 2px;
}

/* Hover */
.toggle:hover .toggle-track {
  border-color: var(--text-primary);
}

/* Active (on) */
.toggle-input:checked + .toggle-track {
  background: var(--accent-orange);
  border-color: var(--accent-orange);
}

.toggle-input:checked + .toggle-track::after {
  background: var(--bg-primary);
  left: 22px;
}

/* Focus */
.toggle-input:focus-visible + .toggle-track {
  outline: 2px solid var(--accent-orange);
  outline-offset: 2px;
}

/* Disabled */
.toggle-input:disabled + .toggle-track {
  opacity: 0.4;
  cursor: not-allowed;
}
```

---

### **Screenshots / Images**

```css
/* Default */
.screenshot {
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.06);
  transition: all 250ms cubic-bezier(0.25, 0.1, 0.25, 1);
}

/* Hover */
.screenshot:hover {
  box-shadow: 0 12px 48px rgba(0, 0, 0, 0.08);
  transform: translateY(-4px);
  filter: brightness(1.05);
}

/* Focus (if clickable) */
.screenshot:focus-visible {
  outline: 2px solid var(--accent-orange);
  outline-offset: 4px;
}

/* Loading */
.screenshot.loading {
  opacity: 0;
  animation: fadeIn 400ms cubic-bezier(0.25, 0.1, 0.25, 1) forwards;
}
```

---

### **Chart Elements**

```css
/* Default */
.chart-line {
  stroke-width: 2px;
  opacity: 1;
  transition: all 150ms cubic-bezier(0.25, 0.1, 0.25, 1);
}

/* Hover */
.chart-line:hover {
  stroke-width: 2.5px;
  filter: brightness(1.15);
}

/* Selected */
.chart-line.selected {
  stroke-width: 3px;
  filter: brightness(1.2);
}

/* Inactive (when another element is selected) */
.chart-line.inactive {
  opacity: 0.3;
}

/* Focus (keyboard navigation) */
.chart-line:focus {
  stroke-width: 3px;
  filter: drop-shadow(0 0 4px var(--accent-orange));
}
```

---

## 3. Loading States

### **Spinner (Circular)**

```css
.spinner {
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

/* Small variant */
.spinner-sm {
  width: 16px;
  height: 16px;
  border-width: 1.5px;
}

/* Large variant */
.spinner-lg {
  width: 32px;
  height: 32px;
  border-width: 3px;
}
```

### **Progress Bar**

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
}

/* Indeterminate */
.progress-bar.indeterminate {
  width: 30%;
  animation: progress-indeterminate 1.5s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

@keyframes progress-indeterminate {
  0% { transform: translateX(-100%); }
  100% { transform: translateX(400%); }
}
```

### **Skeleton Screen**

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

/* Variants */
.skeleton-text {
  height: 16px;
  width: 100%;
  margin-bottom: var(--space-s);
}

.skeleton-heading {
  height: 24px;
  width: 60%;
  margin-bottom: var(--space-m);
}

.skeleton-circle {
  width: 40px;
  height: 40px;
  border-radius: var(--radius-full);
}
```

---

## 4. Error States

### **Form Error**

```css
.input.error {
  border: 2px solid #D55E00;
}

.error-message {
  color: #D55E00;
  font-size: 13px;
  margin-top: var(--space-xs);
  display: flex;
  align-items: center;
  gap: var(--space-xs);
}

.error-message::before {
  content: '⚠';
  font-size: 14px;
}
```

### **Alert Box**

```css
.alert-error {
  background: rgba(213, 94, 0, 0.1);
  border: 1.25px solid #D55E00;
  border-radius: var(--radius-md);
  padding: var(--space-m);
  color: var(--text-primary);
}

.alert-error .alert-icon {
  color: #D55E00;
}
```

---

## 5. Success States

### **Form Success**

```css
.input.success {
  border: 2px solid #009E73;
}

.success-message {
  color: #009E73;
  font-size: 13px;
  margin-top: var(--space-xs);
  display: flex;
  align-items: center;
  gap: var(--space-xs);
}

.success-message::before {
  content: '✓';
  font-size: 14px;
  font-weight: bold;
}
```

### **Alert Box**

```css
.alert-success {
  background: rgba(0, 158, 115, 0.1);
  border: 1.25px solid #009E73;
  border-radius: var(--radius-md);
  padding: var(--space-m);
  color: var(--text-primary);
}

.alert-success .alert-icon {
  color: #009E73;
}
```

---

## 6. Focus Indicators (WCAG 2.1 Compliant)

### **Universal Focus Style**

```css
*:focus-visible {
  outline: 2px solid var(--accent-orange);
  outline-offset: 2px;
  border-radius: var(--radius-sm);
}

/* Remove default browser outline */
*:focus:not(:focus-visible) {
  outline: none;
}
```

### **Exceptions**

```css
/* Text inputs - focus is shown via border change */
input[type="text"]:focus-visible,
input[type="email"]:focus-visible,
input[type="password"]:focus-visible,
textarea:focus-visible {
  outline: none; /* Border handles focus state */
}

/* Custom controls (checkbox, radio) */
.checkbox-input:focus-visible + .checkbox-box,
.radio-input:focus-visible + .radio-circle {
  outline: 2px solid var(--accent-orange);
  outline-offset: 2px;
}
```

---

## 7. Disabled States

### **Universal Disabled Style**

```css
[disabled],
.disabled {
  opacity: 0.4;
  cursor: not-allowed;
  pointer-events: none;
}
```

### **Exceptions**

```css
/* Buttons - maintain structure, reduce opacity */
button:disabled,
.btn:disabled {
  opacity: 0.4;
  transform: none;
  filter: none;
}

/* Form inputs - show visual difference */
input:disabled,
textarea:disabled,
select:disabled {
  background: var(--line-color);
  opacity: 0.6;
}
```

---

## 8. Transition Specifications

### **Standard Transitions**

```css
/* Quick (hover, focus) */
--transition-quick: 150ms cubic-bezier(0.25, 0.1, 0.25, 1);

/* Standard (state changes) */
--transition-standard: 250ms cubic-bezier(0.25, 0.1, 0.25, 1);

/* Slow (complex animations) */
--transition-slow: 400ms cubic-bezier(0.25, 0.1, 0.25, 1);
```

### **Properties to Transition**

```css
/* Buttons, Links, Cards */
transition: all var(--transition-quick);

/* Specific properties for better performance */
transition:
  background var(--transition-quick),
  color var(--transition-quick),
  border-color var(--transition-quick),
  transform var(--transition-quick),
  opacity var(--transition-quick);
```

---

## 9. Touch Device Adaptations

```css
/* Remove hover states on touch devices */
@media (hover: none) {
  .btn:hover,
  .card:hover,
  .nav-item:hover {
    background: initial;
    transform: none;
    box-shadow: none;
  }
}

/* Increase touch targets */
@media (pointer: coarse) {
  .btn,
  .nav-item,
  .tab {
    min-height: 44px;
    min-width: 44px;
    padding: var(--space-m) var(--space-l);
  }
}
```

---

## 10. Dark Mode State Adjustments

Most states remain the same in dark mode thanks to CSS variables, but some need adjustment:

```css
[data-theme="dark"] {
  /* Reduce shadow opacity for dark backgrounds */
  .card:hover {
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
  }

  .screenshot:hover {
    box-shadow: 0 12px 48px rgba(0, 0, 0, 0.4);
  }

  /* Adjust skeleton pulse for dark mode */
  .skeleton {
    background: var(--line-color);
    opacity: 0.3;
  }
}
```

---

## 11. Animation Keyframes

```css
/* Spin (loading spinners) */
@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Fade in (page load, skeleton → content) */
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

/* Pulse (loading states) */
@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

/* Slide in (dropdowns, modals) */
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

## Summary

**Key Principles:**
- All states have precise, measurable specifications (no guesswork)
- Transitions are 150-250ms with consistent easing
- Focus indicators are WCAG 2.1 AA compliant (2px outline, 2px offset)
- Disabled states use 40% opacity universally
- Hover states use brightness filters and subtle transforms
- Loading states use spinners or skeleton screens
- Error/success states use Okabe-Ito red (#D55E00) and green (#009E73)
- Touch devices get larger targets (44×44px minimum)
- Dark mode adapts automatically via CSS variables
