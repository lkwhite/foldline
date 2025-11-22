# Payment Architecture for Foldline

## Overview

Foldline uses a **privacy-first, local-only payment and licensing model** powered by Lemon Squeezy. This architecture maintains our core principle: **your data stays on your device**, with minimal external dependencies.

## Payment Model

### Freemium with One-Time Premium Upgrade

- **Free tier**: Download and use basic features at no cost
- **Premium tier**: Pay-what-you-want upgrade (minimum $15 USD) for advanced features
- **No subscriptions**: One-time payment, lifetime access
- **Upgrade anytime**: Free users can upgrade whenever they're ready

### Free vs Premium Features

| Feature | Free | Premium |
|---------|------|---------|
| Data Sources | Garmin only | All supported devices |
| Data History | Last 30 days | Unlimited |
| Dashboard | ✓ | ✓ |
| Heatmaps | Single metric | Multiple metrics |
| Trend Charts | Basic | Advanced with filters |
| Correlation Analysis | ✗ | ✓ |
| Data Export | ✗ | ✓ (CSV, JSON, FIT) |
| Custom Date Ranges | ✗ | ✓ |
| Advanced Filters | ✗ | ✓ |

### Why Lemon Squeezy?

- **Hosted checkout**: No PCI compliance burden on our end
- **Global tax handling**: Automatic VAT/GST calculation and collection
- **License key generation**: Built-in license key issuance
- **Download hosting**: Can host versioned releases
- **Merchant of record**: They handle all payment processing and legal compliance

---

## High-Level User Flows

### Free Tier Flow

```
User visits website
    ↓
Clicks "Download Free"
    ↓
Downloads app (.dmg/.exe/.AppImage)
    ↓
Installs and opens app
    ↓
Uses basic features (no license required)
    ↓
Sees upgrade prompts for premium features
```

### Premium Upgrade Flow (from within app)

```
User encounters premium feature gate
    ↓
Clicks "Upgrade to Premium"
    ↓
Redirected to Lemon Squeezy hosted checkout
    ↓
Completes purchase (PWYW amount)
    ↓
Receives email with license key
    ↓
Returns to app → enters license key in settings
    ↓
Premium features unlocked immediately
    ↓
Full offline functionality with all features
```

### Direct Purchase Flow (from website)

```
User visits website
    ↓
Clicks "See Pricing" → navigates to /buy
    ↓
Clicks "Continue to Secure Checkout"
    ↓
Completes purchase on Lemon Squeezy
    ↓
Receives email with:
  - Download link
  - License key
    ↓
Downloads and installs app
    ↓
Opens app → enters license key in settings
    ↓
All premium features unlocked
```

---

## Architecture Components

### 1. Marketing Website (SvelteKit)

**Location**: Frontend web application, separate from desktop app

**Responsibilities**:
- Display product information and screenshots
- Present "Buy Foldline" CTA
- Provide checkout URL to Lemon Squeezy
- Explain privacy model and EFF donation commitment

**Implementation**:
- Static or server-rendered SvelteKit pages
- No user accounts or login system
- Lemon Squeezy checkout URL configured via environment variable
- Can optionally use Lemon Squeezy API to dynamically generate checkout URLs (but not required for MVP)

### 2. Desktop App (Tauri + SvelteKit + Python)

**Location**: User's local machine

**Responsibilities**:
- One-time license activation on first launch
- Secure local storage of license key
- Fully offline operation after activation
- Display license status in settings/about screen

**Implementation**:
- License activation screen (SvelteKit UI)
- Tauri secure storage for license key persistence
- No continuous phone-home behavior
- No telemetry or analytics

### 3. Lemon Squeezy (External Service)

**Responsibilities**:
- Hosted checkout page
- Payment processing
- License key generation
- Email delivery (download link + license key)
- Optional: webhooks for purchase notifications (future enhancement)

**Configuration Required**:
- Store ID
- Product ID
- API key (for optional backend validation)

---

## Privacy Stance

### Core Principles

1. **No telemetry**: The app never sends usage data, crash reports, or analytics
2. **Minimal license checks**: Activation is one-time; no ongoing validation required
3. **No continuous server calls**: After activation, the app works 100% offline
4. **No user accounts**: No login, no email collection beyond what Lemon Squeezy handles for purchase
5. **Local-only data processing**: All physiological data stays on the user's device

### License Validation Strategy

**Phase 1: Trust-Based (MVP)**
- App accepts any non-empty license key
- Stores it in local secure storage
- Unlocks full functionality
- Relies on user honesty (matches indie software model)

**Phase 2: Optional Validation (Future)**
- On activation, app can optionally ping a minimal validation endpoint
- Endpoint checks if license key exists in Lemon Squeezy
- Returns simple yes/no (no user data transmitted)
- If offline, falls back to trust-based model
- Never blocks usage for connectivity issues

**Why This Works**:
- Foldline is a niche, prosumer tool with an honest target audience
- Minimal piracy incentive (data never leaves device, so no "free trial" to crack)
- Reduces infrastructure costs and privacy concerns
- Aligns with open-source ethos (10% to EFF)

---

## Technical Integration Plan

### Marketing Site: Checkout URL

**Simple Approach (MVP)**:
```javascript
// In .env
LEMONSQUEEZY_CHECKOUT_URL=https://foldline.lemonsqueezy.com/checkout/buy/PRODUCT_VARIANT_ID

// In SvelteKit component
const checkoutUrl = import.meta.env.LEMONSQUEEZY_CHECKOUT_URL;
```

Button action: `window.open(checkoutUrl, '_blank')`

**Advanced Approach (Optional)**:
- Use Lemon Squeezy API to create checkout sessions dynamically
- Allows custom data (e.g., user-selected PWYW amount)
- Requires backend endpoint to avoid exposing API key
- Endpoint: `POST /api/checkout` → returns checkout URL

### Desktop App: License Activation

**UI Flow**:
1. On first launch, show activation modal
2. Text input for license key
3. "Skip for now" option (shows limited/demo mode message)
4. "Activate" button

**Storage**:
```rust
// Tauri secure storage (Rust backend)
tauri::api::keytar::set_password("com.foldline", "license_key", &license_key)?;
```

**Validation (MVP)**:
```typescript
// Simple client-side check
function activateLicense(key: string): boolean {
  if (key.length > 0) {
    // TODO: Replace with Lemon Squeezy validation API call
    localStorage.setItem('foldline_license', key);
    return true;
  }
  return false;
}
```

**Validation (Future with API)**:
```typescript
async function validateLicense(key: string): Promise<boolean> {
  try {
    const response = await fetch('https://api.foldline.app/validate', {
      method: 'POST',
      body: JSON.stringify({ license_key: key }),
      headers: { 'Content-Type': 'application/json' }
    });
    return response.ok;
  } catch {
    // Offline or network error → allow activation anyway
    localStorage.setItem('foldline_license', key);
    return true;
  }
}
```

### Download Distribution

**Option A: Lemon Squeezy Hosted**
- Upload `.dmg`, `.exe`, `.AppImage` to Lemon Squeezy
- They serve download links in purchase emails
- Versioning via separate product variants or file uploads

**Option B: GitHub Releases + Lemon Squeezy License**
- Host binaries on GitHub Releases (public or private)
- Lemon Squeezy email contains GitHub release URL + license key
- More control, better for open-source hybrid model

**Recommendation**: Start with Option A for simplicity, migrate to Option B if needed for transparency.

---

## Upgrade Pricing (Future Consideration)

**Current Plan**: One-time purchase, all future updates free

**If Upgrade Pricing Needed Later**:
1. Major version releases (e.g., Foldline 2.0) could be separate products
2. Existing users get discount codes via Lemon Squeezy
3. License key versioning: `FOLD-V1-XXXX` vs. `FOLD-V2-XXXX`
4. App checks major version on activation

**Recommendation**: Avoid upgrade pricing initially. Better to focus on new user acquisition.

---

## Security Considerations

### Secrets Management

**Never commit**:
- Lemon Squeezy API keys
- Webhook secrets
- Real product/store IDs (use placeholders in docs)

**Where secrets live**:
- Marketing site: `.env` (server-side only)
- Desktop app: No secrets needed (license keys are user-provided, not embedded)
- CI/CD: GitHub Secrets for automated releases

### License Key Format

Lemon Squeezy generates keys like: `XXXX-XXXX-XXXX-XXXX`

**Display in app**:
- Show full key in activation input
- After activation, show last 4 characters only: `••••-••••-••••-XXXX`
- Never log full keys to console or files

### Secure Storage

- **macOS**: Keychain via Tauri
- **Windows**: Credential Manager via Tauri
- **Linux**: Secret Service API via Tauri

Fallback: Encrypted file in user config directory (if secure storage unavailable).

---

## Environment Variables

### Marketing Site (`.env`)

```bash
# Lemon Squeezy checkout URL (simplest approach)
LEMONSQUEEZY_CHECKOUT_URL=https://foldline.lemonsqueezy.com/checkout/buy/XXXXXXXX

# Or, for dynamic checkout creation:
LEMONSQUEEZY_STORE_ID=your_store_id
LEMONSQUEEZY_API_KEY=your_api_key
```

### Desktop App

**No environment variables needed** — users provide their own license keys.

---

## Testing Strategy

### Development

**Mock License Keys**:
- `DEV-XXXX-XXXX-XXXX` → always valid in dev mode
- `TEST-XXXX-XXXX-XXXX` → triggers test flows

**Lemon Squeezy Test Mode**:
- Use test mode for checkout flow development
- Generate test license keys
- No real payments

### QA Checklist

- [ ] Purchase flow from website → checkout → email received
- [ ] Download link in email works
- [ ] License key in email works in app
- [ ] App activates offline (disconnect network after download)
- [ ] App remembers activation after restart
- [ ] Light/dark mode works on activation screen
- [ ] Invalid/empty keys show appropriate error messages

---

## Open Questions & Future Work

### Open Questions

1. **Minimum PWYW amount**: $15? $20? $10?
2. **Download hosting**: Lemon Squeezy or GitHub Releases?
3. **Beta/Early Access**: Separate product or discount codes?
4. **Refund policy**: Lemon Squeezy handles, but what's our stance?

### Future Enhancements

- **Webhooks**: Listen for purchases to track revenue in real-time
- **License validation API**: Optional cloud service for piracy deterrence
- **Trial mode**: 30-day full access before requiring license (still offline)
- **Team licenses**: Bulk purchase discounts (if corporate interest emerges)

---

## Design Consistency

All payment-related UI follows the **FOLDLINE_DESIGN_SPEC.md**:

- **CTA buttons** (Buy/Activate): Orange (`#E69F00`) fill, 4px border radius
- **Text inputs**: Thin border, Inter font, tabular numbers for license keys
- **Spacing**: 8-pt grid (16px between input and button, 24px section padding)
- **Light/dark mode**: Use CSS variables from design system
- **No**: gradients, heavy shadows, or decorative elements

### Example Activation Screen Layout

```
┌─────────────────────────────────────┐
│  Activate Foldline                  │
│                                     │
│  Enter the license key from your   │
│  purchase email to unlock full     │
│  functionality.                     │
│                                     │
│  ┌─────────────────────────────┐   │
│  │ XXXX-XXXX-XXXX-XXXX         │   │
│  └─────────────────────────────┘   │
│                                     │
│  [Activate]  [Skip for now]        │
│                                     │
│  Your data never leaves this       │
│  device. This is a one-time        │
│  activation only.                   │
└─────────────────────────────────────┘
```

---

## Summary

This architecture achieves:

✅ **Privacy-first**: No telemetry, no continuous server calls
✅ **Offline-friendly**: Works 100% locally after activation
✅ **Simple**: Hosted checkout, minimal infrastructure
✅ **Honest**: Trust-based licensing for niche audience
✅ **Compliant**: Lemon Squeezy handles tax/legal
✅ **Transparent**: 10% to EFF documented and tracked

Next steps: Implement marketing site checkout flow, build activation UI, create donation tracking tools.
