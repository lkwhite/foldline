You are now the implementation agent for Foldline, a local-only, privacy-first desktop app built with Tauri + SvelteKit + Python. The goal is to design and scaffold a clean payment and licensing system using Lemon Squeezy, plus an internal plan for routing ~10% of net revenue to the EFF.

## Context

The visual and UX design spec for Foldline already exists in this repo as:

- design/FOLDLINE_DESIGN_SPEC.md

Treat that document as the authoritative source of truth for branding, layout, and UI behavior. DO NOT override its color, typography, or layout rules. Instead, integrate payment and licensing UX into that existing design language.

## High-level requirements

We want to:

1. Sell Foldline as a **one-time purchase**, ideally **pay-what-you-want (PWYW)** with a sensible minimum.
2. Use **Lemon Squeezy** for:
   - hosted checkout
   - global VAT/GST handling
   - license key issuance
   - download hosting (if appropriate)
3. Keep Foldline **privacy-first and local-only**:
   - No continuous server calls from the app
   - License check should be as minimal and optional as possible
   - Once activated, the app should be usable fully offline
4. Maintain a clear internal **EFF donation plan**:
   - Target: 10% of net revenue donated to EFF
   - Repo should contain docs and simple tools to calculate and track this
   - Actual donation is manual; we just want good accounting support
5. Follow the existing **design spec** for:
   - minimal, line-drawing aesthetic
   - neutral/technical tone
   - screenshots as the hero
   - light/dark modes

You MUST NOT:
- Hardcode any secret keys or real Lemon Squeezy credentials.
- Call out to external APIs from within this environment.
- Implement anything that contradicts the design/FOLDLINE_DESIGN_SPEC.md document.

Instead, architect everything and leave placeholders / .env usage where appropriate.

## Tasks

### 1. Read and summarize the design spec

1. Open and read: design/FOLDLINE_DESIGN_SPEC.md
2. Briefly summarize (in your own words) the key constraints that matter for:
   - payment UX
   - license UI
   - screenshot presentation
   - light/dark mode behavior
3. Confirm how you will keep the payment-related UI consistent with that spec.

Do this summary FIRST, then proceed.

---

### 2. Add repository-level planning docs for payments & donations

Create the following repo docs:

1. PAYMENT_ARCHITECTURE.md
   - Describe the chosen approach using Lemon Squeezy:
     - Hosted checkout for one-time purchases
     - PWYW with configurable minimum
     - License key issuance and activation
     - Offline-first behavior: app is fully local once license is activated
   - Describe the high-level flow:
     - User clicks “Buy Foldline” on the website
     - User is taken to Lemon Squeezy checkout page
     - On success, Lemon Squeezy sends them:
       - a download link
       - a license key
     - User downloads the app and enters the license key inside the app
   - Distinguish between:
     - marketing website (SvelteKit)
     - app UI (Tauri + SvelteKit + Python backend)
   - Describe the privacy stance: no telemetry, minimal license checks, no continuous background calls.

2. EFF_DONATIONS.md
   - Document the plan to donate ~10% of net revenue to the EFF.
   - Describe:
     - How revenue will be retrieved (e.g., Lemon Squeezy CSV export or API).
     - How net revenue is defined (e.g., after platform fees, before tax, etc. — propose a default assumption and clearly state it).
     - A simple workflow:
       1. Export CSV from Lemon Squeezy monthly.
       2. Run a small script in this repo to compute:
          - gross revenue
          - fees
          - net revenue
          - 10% donation target
       3. Use that number to make the manual donation on eff.org.
     - Future ideas (optional): GitHub Actions to generate monthly reports, etc.

3. .env.example (update or create)
   - Add placeholder variables for Lemon Squeezy integration, e.g.:
     - LEMONSQUEEZY_STORE_ID
     - LEMONSQUEEZY_PRODUCT_ID
     - LEMONSQUEEZY_API_KEY
     - OPTIONAL: LEMONSQUEEZY_WEBHOOK_SECRET
   - DO NOT use any real values.
   - Add comments explaining which parts of the code will use these and how.

---

### 3. Lemon Squeezy integration plan (no secrets)

Implement a PLAN first, then code:

1. In PAYMENT_ARCHITECTURE.md, add a section:
   - “Technical Integration Plan”
   - Describe:
     - Using Lemon Squeezy’s **hosted checkout URL** for the marketing site.
     - Optional: a minimal SvelteKit endpoint that can dynamically provide the correct checkout URL (but no secrets in client).
     - License key validation strategy:
       - simplest version: app accepts any non-empty key and uses it to unlock; user trust model
       - better version: later, validate via an internal service or Lemon Squeezy API.
       - offline-friendly considerations.

2. Outline, in that same doc, how to handle:
   - versioned downloads (e.g., linking to a stable download URL from LS)
   - upgrade pricing in the future (not implemented now, but structurally planned for)

Do NOT implement any complex backend service yet. We want a simple initial version.

---

### 4. Marketing site: “Buy Foldline” flow (SvelteKit)

Implement UI + basic plumbing for the website side, consistent with the design spec:

1. Add/modify:
   - A prominent “Buy Foldline” CTA in the hero section (label text may be “Buy Foldline” or “Get Foldline” based on existing copy style).
   - A secondary CTA like “Learn how your data stays local” (links to privacy section).

2. Implement a SvelteKit route or component (e.g. src/routes/buy/+page.svelte or a dedicated component) that:
   - Explains the one-time purchase / pay-what-you-want model.
   - Emphasizes:
     - privacy-first
     - local-only processing
     - 10% EFF donation plan (link to EFF_DONATIONS.md for transparency, if appropriate).
   - Has a “Continue to secure checkout” button that opens the Lemon Squeezy hosted checkout URL (use a placeholder URL for now, plus a TODO to replace).

3. Make sure:
   - The UI respects the line-drawing aesthetic from the design spec.
   - Buttons use the accent orange from the spec.
   - No extra UI chrome that conflicts with FOLDLINE_DESIGN_SPEC.md.

Document in PAYMENT_ARCHITECTURE.md where the checkout URL should be configured (e.g., a single config file or .env variable).

---

### 5. App-side license activation UI (Tauri + SvelteKit)

Create a basic license activation flow in the desktop app:

1. Add an “Activation” or “License” screen in the Tauri/SvelteKit app:
   - A single text input for a license key.
   - A short explanation:
     - one-time activation
     - works offline after activation
     - no telemetry.

2. Implement a simple client-side validation placeholder:
   - For now, treat any non-empty license key as “valid” and store it in a secure local storage location (e.g., via Tauri’s secure storage or filesystem).
   - Add clear TODOs:
     - “Replace this with proper Lemon Squeezy validation once the backend service is available.”
   - Ensure the storage mechanism is compatible with offline use and privacy goals.

3. Add a small “About your license” panel that:
   - shows whether the app is activated
   - shows the license key’s last 4 characters
   - does NOT show personally identifiable info

Ensure the UI for this activation screen follows the colors, typography, and line-drawing rules from FOLDLINE_DESIGN_SPEC.md.

---

### 6. Donation ledger tooling (minimal but useful)

Implement a very simple script or placeholder for computing EFF donations:

1. Add a directory: tools/donations/
2. Inside, create a script (e.g., Python or Node) that:
   - Takes a CSV export from Lemon Squeezy (place a sample or mock file in tools/donations/sample-data/).
   - Parses total revenue for a given period.
   - Calculates:
     - gross revenue
     - a configurable “platform fee” percentage (just a constant at first)
     - net revenue
     - 10% of net as “EFF donation target”
   - Prints a short summary to stdout.

3. Document usage in EFF_DONATIONS.md:
   - where to put the CSV
   - how to run the script
   - how to interpret the output

No real API calls, just local CSV parsing.

---

### 7. Respect privacy and security

Throughout all implementation:

- Do NOT hardcode real API keys or secrets.
- Do NOT bake any user-identifiable data into logs or analytics.
- Document clearly where secrets should be provided (via .env, config, etc.).
- Keep all app behavior compatible with “local-only” data processing once activated.

---

### 8. Workflow

Before writing code:

1. Summarize your understanding of the design spec and payment requirements.
2. Propose an implementation plan (files to create/modify, structures, and components).
3. Then implement in small, reviewable steps:
   - Docs first (PAYMENT_ARCHITECTURE.md, EFF_DONATIONS.md)
   - Then website changes (buy flow)
   - Then app activation UI
   - Then donation tooling

At each step, keep the codebase consistent with FOLDLINE_DESIGN_SPEC.md and the privacy-first, local-only vision.

