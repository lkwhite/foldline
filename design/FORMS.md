# 📝 Foldline Form Elements Specification

## Overview

Form elements follow the minimal line-drawing aesthetic with clear state differentiation using the accent orange for focus and active states. All forms prioritize clarity and accessibility for health data input.

---

## 1. Text Input

### **Default State**
```css
.input {
  border: 1.25px solid var(--line-color);
  background: transparent;
  color: var(--text-primary);
  font-family: var(--font-family);
  font-size: 16px;
  line-height: 1.5;
  padding: var(--space-s) var(--space-m);
  border-radius: var(--radius-md);
  transition: all 150ms cubic-bezier(0.25, 0.1, 0.25, 1);
}
```

### **States**
- **Hover**: Border color: `var(--text-primary)` at 60% opacity
- **Focus**: Border: `2px solid var(--accent-orange)`, outline: none
- **Disabled**: Border: `var(--line-color)` at 50% opacity, background: `var(--line-color)` at 10% opacity, cursor: not-allowed
- **Error**: Border: `2px solid #D55E00` (Okabe-Ito red-orange), with error icon and message below
- **Success**: Border: `2px solid #009E73` (Okabe-Ito green) - use sparingly

### **Placeholder**
```css
.input::placeholder {
  color: var(--text-primary);
  opacity: 0.4;
  font-style: normal;
}
```

---

## 2. Textarea

### **Specification**
- Same styling as text input
- **Min height**: 120px (approx 5 lines)
- **Max height**: Optional, use `resize: vertical` for user control
- **Resize**: Vertical only

```css
.textarea {
  /* Inherits from .input */
  min-height: 120px;
  resize: vertical;
}
```

---

## 3. Select / Dropdown

### **Default State**
```css
.select {
  /* Inherits from .input */
  appearance: none;
  background-image: url("data:image/svg+xml,..."); /* Custom chevron */
  background-position: right var(--space-m) center;
  background-repeat: no-repeat;
  padding-right: var(--space-xl);
}
```

### **Custom Chevron Icon**
- Stroke: `var(--text-primary)`
- Size: 16px × 16px
- Style: Simple downward chevron (line-drawing)
- Rotates 180deg when open

### **Dropdown Menu**
```css
.select-menu {
  border: 1.25px solid var(--line-color);
  background: var(--bg-primary);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
  border-radius: var(--radius-md);
  padding: var(--space-xs) 0;
  max-height: 240px;
  overflow-y: auto;
}

.select-option {
  padding: var(--space-s) var(--space-m);
  cursor: pointer;
}

.select-option:hover {
  background: var(--accent-orange);
  color: var(--bg-primary);
}

.select-option:selected,
.select-option[aria-selected="true"] {
  background: var(--line-color);
  font-weight: 500;
}
```

---

## 4. Checkbox

### **Structure**
```html
<label class="checkbox">
  <input type="checkbox" class="checkbox-input">
  <span class="checkbox-box"></span>
  <span class="checkbox-label">Label text</span>
</label>
```

### **Styling**
```css
.checkbox-input {
  position: absolute;
  opacity: 0;
  pointer-events: none;
}

.checkbox-box {
  width: 20px;
  height: 20px;
  border: 1.25px solid var(--line-color);
  border-radius: var(--radius-sm);
  background: transparent;
  position: relative;
  transition: all 150ms cubic-bezier(0.25, 0.1, 0.25, 1);
}

/* Checked state */
.checkbox-input:checked + .checkbox-box {
  background: var(--accent-orange);
  border-color: var(--accent-orange);
}

/* Checkmark (simple line-drawing) */
.checkbox-input:checked + .checkbox-box::after {
  content: '';
  position: absolute;
  left: 6px;
  top: 3px;
  width: 5px;
  height: 9px;
  border: solid var(--bg-primary);
  border-width: 0 2px 2px 0;
  transform: rotate(45deg);
}

/* Focus state */
.checkbox-input:focus-visible + .checkbox-box {
  outline: 2px solid var(--accent-orange);
  outline-offset: 2px;
}

/* Hover state */
.checkbox:hover .checkbox-box {
  border-color: var(--text-primary);
}

/* Disabled state */
.checkbox-input:disabled + .checkbox-box {
  opacity: 0.4;
  cursor: not-allowed;
}
```

---

## 5. Radio Button

### **Structure**
```html
<label class="radio">
  <input type="radio" name="group" class="radio-input">
  <span class="radio-circle"></span>
  <span class="radio-label">Option text</span>
</label>
```

### **Styling**
```css
.radio-circle {
  width: 20px;
  height: 20px;
  border: 1.25px solid var(--line-color);
  border-radius: var(--radius-full);
  background: transparent;
  position: relative;
  transition: all 150ms cubic-bezier(0.25, 0.1, 0.25, 1);
}

/* Selected state - filled circle */
.radio-input:checked + .radio-circle {
  border-color: var(--accent-orange);
}

.radio-input:checked + .radio-circle::after {
  content: '';
  position: absolute;
  width: 10px;
  height: 10px;
  border-radius: var(--radius-full);
  background: var(--accent-orange);
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

/* Focus state */
.radio-input:focus-visible + .radio-circle {
  outline: 2px solid var(--accent-orange);
  outline-offset: 2px;
}

/* Hover state */
.radio:hover .radio-circle {
  border-color: var(--text-primary);
}
```

---

## 6. Toggle Switch

**Use case**: On/off settings, boolean preferences

### **Structure**
```html
<label class="toggle">
  <input type="checkbox" class="toggle-input">
  <span class="toggle-track"></span>
  <span class="toggle-label">Enable notifications</span>
</label>
```

### **Styling**
```css
.toggle-track {
  width: 44px;
  height: 24px;
  border: 1.25px solid var(--line-color);
  border-radius: var(--radius-full);
  background: transparent;
  position: relative;
  transition: all 200ms cubic-bezier(0.25, 0.1, 0.25, 1);
}

/* Thumb */
.toggle-track::after {
  content: '';
  position: absolute;
  width: 18px;
  height: 18px;
  border-radius: var(--radius-full);
  background: var(--text-primary);
  top: 2px;
  left: 2px;
  transition: all 200ms cubic-bezier(0.25, 0.1, 0.25, 1);
}

/* Checked state */
.toggle-input:checked + .toggle-track {
  background: var(--accent-orange);
  border-color: var(--accent-orange);
}

.toggle-input:checked + .toggle-track::after {
  background: var(--bg-primary);
  left: 22px;
}

/* Focus state */
.toggle-input:focus-visible + .toggle-track {
  outline: 2px solid var(--accent-orange);
  outline-offset: 2px;
}

/* Hover state */
.toggle:hover .toggle-track {
  border-color: var(--text-primary);
}
```

---

## 7. Date/Time Picker

**Critical for physiological tracking**

### **Date Input**
```css
.date-input {
  /* Inherits from .input */
  font-variant-numeric: tabular-nums;
}

/* Custom calendar icon */
.date-input::after {
  content: url("data:image/svg+xml,..."); /* Calendar icon */
  position: absolute;
  right: var(--space-m);
  pointer-events: none;
}
```

### **Calendar Popup**
```css
.calendar {
  border: 1.25px solid var(--line-color);
  background: var(--bg-primary);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
  border-radius: var(--radius-md);
  padding: var(--space-m);
}

.calendar-header {
  border-bottom: 1.25px solid var(--line-color);
  padding-bottom: var(--space-s);
  margin-bottom: var(--space-s);
}

.calendar-day {
  width: 32px;
  height: 32px;
  border-radius: var(--radius-sm);
  border: none;
  background: transparent;
  font-variant-numeric: tabular-nums;
}

.calendar-day:hover {
  background: var(--line-color);
}

.calendar-day.selected {
  background: var(--accent-orange);
  color: var(--bg-primary);
}

.calendar-day.today {
  border: 1.25px solid var(--accent-orange);
}
```

### **Time Input**
- Use native time input with custom styling
- Tabular numerics for consistent width
- AM/PM toggle buttons styled as secondary buttons

---

## 8. Range Slider

**Use case**: Intensity levels, duration settings

### **Styling**
```css
.range {
  -webkit-appearance: none;
  width: 100%;
  height: 1.25px;
  background: var(--line-color);
  outline: none;
}

/* Thumb */
.range::-webkit-slider-thumb {
  -webkit-appearance: none;
  width: 16px;
  height: 16px;
  border-radius: var(--radius-full);
  background: var(--accent-orange);
  cursor: pointer;
  border: 2px solid var(--bg-primary);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.range::-moz-range-thumb {
  width: 16px;
  height: 16px;
  border-radius: var(--radius-full);
  background: var(--accent-orange);
  cursor: pointer;
  border: 2px solid var(--bg-primary);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

/* Track fill */
.range::-webkit-slider-runnable-track {
  background: linear-gradient(
    to right,
    var(--accent-orange) 0%,
    var(--accent-orange) var(--range-value),
    var(--line-color) var(--range-value),
    var(--line-color) 100%
  );
}

/* Focus state */
.range:focus-visible::-webkit-slider-thumb {
  outline: 2px solid var(--accent-orange);
  outline-offset: 2px;
}
```

---

## 9. Field Groups & Labels

### **Label Styling**
```css
.label {
  display: block;
  font-size: 14px;
  font-weight: 500;
  color: var(--text-primary);
  margin-bottom: var(--space-xs);
}

.label.required::after {
  content: '*';
  color: var(--accent-orange);
  margin-left: 4px;
}
```

### **Help Text**
```css
.help-text {
  font-size: 13px;
  color: var(--text-primary);
  opacity: 0.6;
  margin-top: var(--space-xs);
}
```

### **Error Message**
```css
.error-message {
  font-size: 13px;
  color: #D55E00; /* Okabe-Ito red-orange */
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

### **Field Group**
```css
.field-group {
  margin-bottom: var(--space-l);
}

.field-group:last-child {
  margin-bottom: 0;
}
```

---

## 10. Validation States

### **Client-side Validation**
- Validate on blur, not on every keystroke (avoid distraction)
- Show success state only for critical fields (e.g., password strength)
- Error messages appear below field with icon

### **Inline Validation Icons**
```css
.input-wrapper {
  position: relative;
}

.input-icon {
  position: absolute;
  right: var(--space-m);
  top: 50%;
  transform: translateY(-50%);
  pointer-events: none;
}

.input-icon.error {
  color: #D55E00;
}

.input-icon.success {
  color: #009E73;
}
```

---

## 11. Form Layout

### **Single Column (Default)**
```css
.form {
  max-width: 480px;
  margin: 0 auto;
}
```

### **Two Column (Desktop)**
```css
.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--space-m);
}

@media (max-width: 768px) {
  .form-row {
    grid-template-columns: 1fr;
  }
}
```

### **Full Width**
For data tables or dashboard settings:
```css
.form.form-wide {
  max-width: 100%;
}
```

---

## 12. Submit Buttons

### **Primary Submit (CTA)**
```css
.btn-submit {
  background: var(--accent-orange);
  color: var(--bg-primary);
  border: none;
  padding: var(--space-m) var(--space-xl);
  border-radius: var(--radius-md);
  font-weight: 500;
  cursor: pointer;
  transition: all 150ms cubic-bezier(0.25, 0.1, 0.25, 1);
}

.btn-submit:hover {
  filter: brightness(1.1);
}

.btn-submit:active {
  transform: translateY(1px);
}

.btn-submit:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}
```

### **Secondary Action**
```css
.btn-secondary {
  background: transparent;
  color: var(--text-primary);
  border: 1.25px solid var(--line-color);
  padding: var(--space-m) var(--space-xl);
  border-radius: var(--radius-md);
  font-weight: 500;
  cursor: pointer;
}

.btn-secondary:hover {
  border-color: var(--text-primary);
  background: var(--line-color);
}
```

### **Loading State**
```css
.btn-submit.loading {
  position: relative;
  color: transparent;
}

.btn-submit.loading::after {
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

@keyframes spin {
  to { transform: translate(-50%, -50%) rotate(360deg); }
}
```

---

## 13. Accessibility Requirements

### **WCAG 2.1 AA Compliance**
- ✅ All form elements have visible labels
- ✅ Focus indicators have 2px outline with 2px offset
- ✅ Color is not the only indicator of state (icons + text)
- ✅ Touch targets minimum 44×44px (mobile)
- ✅ Error messages associated via `aria-describedby`

### **Required ARIA Attributes**
```html
<label for="email" class="label">
  Email address
  <span class="required" aria-label="required">*</span>
</label>
<input
  type="email"
  id="email"
  class="input"
  aria-required="true"
  aria-invalid="false"
  aria-describedby="email-error"
>
<span id="email-error" class="error-message" role="alert">
  Please enter a valid email address
</span>
```

### **Keyboard Navigation**
- Tab order follows visual order
- Enter submits form from any text input
- Space toggles checkboxes/radios
- Arrow keys navigate radio groups
- Escape closes dropdowns/modals

---

## 14. Dark Mode

All form elements automatically adapt via CSS custom properties:
- Borders: `var(--line-color)` switches from `#DCD8CA` to `#3E3E3F`
- Text: `var(--text-primary)` switches from `#111111` to `#F8F8F8`
- Background: `var(--bg-primary)` switches from `#F7F5EF` to `#0C0D0E`
- Accent: `var(--accent-orange)` remains `#E69F00` (unchanged)

No form-specific dark mode overrides needed.

---

## 15. Special Use Cases

### **Multi-Step Forms**
```css
.form-steps {
  display: flex;
  gap: var(--space-s);
  margin-bottom: var(--space-xl);
}

.form-step {
  flex: 1;
  height: 2px;
  background: var(--line-color);
  border-radius: var(--radius-full);
}

.form-step.active {
  background: var(--accent-orange);
}

.form-step.completed {
  background: var(--text-primary);
}
```

### **File Upload**
```css
.file-upload {
  border: 1.25px dashed var(--line-color);
  border-radius: var(--radius-md);
  padding: var(--space-xl);
  text-align: center;
  cursor: pointer;
  transition: all 150ms cubic-bezier(0.25, 0.1, 0.25, 1);
}

.file-upload:hover {
  border-color: var(--accent-orange);
  background: var(--line-color);
}

.file-upload.dragging {
  border-color: var(--accent-orange);
  background: var(--accent-orange);
  opacity: 0.1;
}
```

---

## Summary

**Key Principles:**
- All form elements use 1.25px stroke weight
- Accent orange for focus/active states only
- Clear visual feedback for all interactions
- Accessibility-first design
- Consistent spacing using 8pt grid
- Dark mode support via CSS variables
- Minimal, line-drawing aesthetic throughout
