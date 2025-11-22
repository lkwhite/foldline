# EFF Donations Plan

Foldline is a privacy-first, local-only application. We believe that user autonomy over their own data should be the norm, not an exception. As a small but concrete way to support that principle, we intend to donate a portion of Foldline revenue to the **Electronic Frontier Foundation (EFF)**.

This document describes how we plan to calculate, track, and act on those donations.

---

## Why the EFF?

The EFF has a long track record of:

- Defending privacy, security, and digital civil liberties  
- Pushing back against surveillance and abusive data practices  
- Supporting open standards, encryption, and user control over technology  

Foldline’s entire premise—giving people deep, local visibility into data that usually lives in someone else’s cloud—is philosophically aligned with that mission.

---

## Donation Target

Our **current, non-binding target** is:

> Donate 10% of net revenue from Foldline to the EFF.

“Net revenue” here is a simple operational definition, not an accounting audit standard. It’s meant to be easy to reason about and easy to calculate.

---

## Working Definition of Net Revenue

For a given period (e.g. a month or quarter):

1. **Gross Revenue**  
   Total paid by customers for Foldline in the period, taken from a Lemon Squeezy (or other platform) CSV export.

2. **Platform / Processing Fees**  
   Fees charged by payment processors or by the platform itself.  
   If exact per-transaction fees are not available, we will use:
   - Fee fields from the CSV (if present), or  
   - A conservative flat percentage documented in this repo.

3. **Net Revenue**  
   Defined as:

   **Net Revenue = Gross Revenue − Platform / Processing Fees**

4. **EFF Donation**  
   Defined as:

   **EFF Donation = 10% × Net Revenue**

This definition may evolve as needed; all changes will be documented here.

---

## Workflow for Calculating Donations

### 1. Export Revenue Data

At the end of each period:

1. Log in to the payment platform (e.g. Lemon Squeezy).
2. Export a CSV of all Foldline transactions for that period.
3. Save it locally under a path like:

`tools/donations/data/foldline_revenue_YYYY_MM.csv`

These CSVs **must not** be committed to the public repository because they may contain customer information.

---

### 2. Run the Donation Calculator Script

A small script under `tools/donations/` will:

- Parse the CSV for the period
- Sum gross revenue
- Estimate or read platform fees
- Compute:
  - Gross revenue
  - Fees
  - Net revenue
  - 10% donation target

Example usage (exact command may change once implemented):

```bash
cd tools/donations
python calculate_eff_donation.py data/foldline_revenue_2025_01.csv
```

Example output:

```text
Period: 2025-01
Gross revenue:      $3,420.00
Estimated fees:     $ 205.20
Net revenue:        $3,214.80

EFF donation (10% of net): $321.48
```

---

### 3. Make the Donation

The donation itself is **manual**:

1. Go to https://www.eff.org/donate  
2. Enter the computed donation amount  
3. Complete the donation  

We may record donation receipts privately for bookkeeping but will not publish any customer-identifying data.

---

## Transparency

This plan is:

- A good-faith commitment  
- Not a legal obligation  
- Subject to future refinement  

If the definition of “net revenue,” the donation percentage, or the timing changes, we will:

- Update this document
- Explain why the change was made

We may occasionally publish a simple high-level statement like “We donated $X to the EFF in 20YY.”

---

## Privacy Considerations

- CSV exports may contain emails or other personal information.  
- These files should be:
  - Stored locally  
  - Excluded via `.gitignore`  
  - Never uploaded or shared  

The donation calculator script must operate only on local files and must never send data to external services.

---

## Future Enhancements

Optional improvements include:

- A CLI tool to summarize multiple periods  
- GitHub Actions (private repos only) for donation reporting  
- A small UI section in Foldline showing “We donate 10% to EFF”  
- A way for users to independently support EFF

---

## Summary

- Our goal is to donate ~10% of net revenue to the EFF.  
- Net revenue = gross revenue − fees.  
- Donations are calculated via local CSV exports and a simple script.  
- The actual donation is made manually.  
- We maintain this plan as part of Foldline’s commitment to user privacy and digital rights.
