# 📐 Foldline Layout System

## Grid System

### **12-Column Responsive Grid**

```
Desktop (>1024px):  12 columns
Tablet (768-1024px): 6 columns
Mobile (<768px):     1 column (stack)
```

### **Container**
- Max width: `1280px` (desktop)
- Max width: `1400px` (ultra-wide option)
- Horizontal padding: `var(--space-xl)` (32px)
- Mobile padding: `var(--space-m)` (16px)
- Centered with `margin: 0 auto`

### **Column Gap**
- Desktop: `var(--space-l)` (24px)
- Tablet: `var(--space-m)` (16px)
- Mobile: `var(--space-s)` (8px)

---

## Spacing Scale (8pt Grid)

| Token | Value | Usage |
|-------|-------|-------|
| `--space-xs` | 4px | Tight spacing, icon gaps |
| `--space-s` | 8px | Small gaps, compact layouts |
| `--space-m` | 16px | Default spacing, text blocks |
| `--space-l` | 24px | Section padding, column gaps |
| `--space-xl` | 32px | Large gaps, container padding |
| `--space-xxl` | 48px | Section separators, hero spacing |

---

## Responsive Breakpoints

```css
/* Mobile first approach */

/* Small devices (phones) */
@media (min-width: 640px) { ... }

/* Medium devices (tablets) */
@media (min-width: 768px) { ... }

/* Large devices (desktops) */
@media (min-width: 1024px) { ... }

/* Extra large devices */
@media (min-width: 1280px) { ... }
```

---

## Layout Patterns

### **Hero Section**
```
Desktop:
┌─────────────────────────────────────┐
│ [Text 40%]        [Screenshot 60%]  │
│ Logo                                │
│ H1                                  │
│ Subtext                             │
│ CTA buttons                         │
└─────────────────────────────────────┘

Mobile (stacked):
┌─────────────┐
│ Logo        │
│ H1          │
│ Subtext     │
│ CTA         │
│ Screenshot  │
└─────────────┘
```

### **Feature Block**
```
Desktop (alternating):
┌─────────────────────────────────────┐
│ [Screenshot 60%]    [Text 40%]      │
└─────────────────────────────────────┘
┌─────────────────────────────────────┐
│ [Text 40%]        [Screenshot 60%]  │
└─────────────────────────────────────┘

Mobile (stacked):
┌─────────────┐
│ Screenshot  │
│ Text        │
└─────────────┘
```

### **Screenshot Showcase**
```
Desktop:
┌─────────────────────────────────────┐
│  Screenshot 1                       │
│  ─────────────── (thin separator)   │
│  Screenshot 2                       │
│  ─────────────── (thin separator)   │
│  Screenshot 3                       │
└─────────────────────────────────────┘

Mobile: Same, with tighter spacing
```

---

## Whitespace Rules

### **Vertical Rhythm**
- Between sections: `var(--space-xxl)` × 2 (96px desktop)
- Between elements in section: `var(--space-l)` (24px)
- Between text blocks: `var(--space-m)` (16px)
- Mobile sections: `var(--space-xxl)` (48px)

### **Screenshot Breathing Room**
- Top/bottom margin: `var(--space-xxl)` (48px)
- Side margins: `var(--space-xl)` (32px) on desktop
- Mobile: Reduce to `var(--space-m)` (16px)

---

## Container Utilities

### **`.container`**
```css
.container {
  max-width: 1280px;
  margin: 0 auto;
  padding: 0 var(--space-xl);
}

@media (max-width: 768px) {
  .container {
    padding: 0 var(--space-m);
  }
}
```

### **`.container-wide`**
```css
.container-wide {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 var(--space-xl);
}
```

### **`.section`**
```css
.section {
  padding: calc(var(--space-xxl) * 2) 0;
}

@media (max-width: 768px) {
  .section {
    padding: var(--space-xxl) 0;
  }
}
```

---

## Screenshot Layout Rules

### **Desktop**
- Width: 60-70% of container
- Max width: 900px
- Shadow: `0 10px 40px rgba(0, 0, 0, 0.06)`
- Hover lift: `translateY(-4px)`

### **Mobile**
- Width: 100%
- Shadow: `0 6px 24px rgba(0, 0, 0, 0.05)`
- Hover: disabled (touch devices)

---

## Navigation

### **Nav Bar**
```
┌─────────────────────────────────────┐
│ Logo    Links              [Toggle] │
└─────────────────────────────────────┘
  ─────────────────────────────────────
  (1.25px border)
```

- Height: 64px
- Padding: `var(--space-m)` `var(--space-xl)`
- Border bottom: `1.25px solid var(--line-color)`
- Background: transparent (light backdrop-blur optional)

---

## Footer

### **Layout**
```
┌─────────────────────────────────────┐
  ─────────────────────────────────────
  (1.25px border top)
│                                     │
│ Logo          Links        Social   │
│ Tagline       Links        Links    │
│                                     │
│         © 2025 Foldline             │
└─────────────────────────────────────┘
```

- Padding: `var(--space-xxl)` 0
- Border top: `1.25px solid var(--line-color)`
- Background: Subtle fold-line motif (opacity 0.3)

---

## Responsive Behavior

### **Typography Scaling**
```css
/* H1 */
font-size: clamp(32px, 5vw, 48px);

/* H2 */
font-size: clamp(24px, 4vw, 32px);

/* H3 */
font-size: clamp(18px, 3vw, 22px);

/* Body */
font-size: clamp(16px, 2vw, 18px);
```

### **Spacing Scaling**
- Desktop: Use full spacing scale
- Tablet: Reduce by 25% (`--space-xl` → `--space-l`)
- Mobile: Reduce by 50% for section gaps

---

## Z-Index Scale

```css
--z-base: 0;
--z-nav: 100;
--z-modal: 200;
--z-tooltip: 300;
--z-theme-toggle: 50;
```
