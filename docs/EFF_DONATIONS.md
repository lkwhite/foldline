# EFF Donation Plan

## Commitment

**Foldline donates 10% of net revenue to the Electronic Frontier Foundation (EFF).**

The EFF defends digital privacy, free expression, and innovation. Since Foldline is built on privacy-first principles — your physiological data never leaves your device — supporting the EFF aligns with our values.

**This donation is:**
- **Transparent**: Documented publicly in this repository
- **Manual**: We calculate and donate ourselves (no automated third-party split)
- **Net revenue**: After platform fees, before taxes and business expenses

---

## Why the EFF?

The EFF fights for:
- **Privacy rights**: Defending against mass surveillance and data collection
- **User control**: Advocating for software that respects user autonomy
- **Open standards**: Supporting interoperability and avoiding vendor lock-in

Foldline embodies these principles by:
- Processing all data locally (no cloud sync)
- Exporting data in open formats (FIT, CSV, JSON)
- Avoiding telemetry and tracking

Supporting the EFF is our way of contributing to the broader ecosystem that makes privacy-respecting software possible.

**Learn more**: [eff.org](https://www.eff.org)

---

## Revenue Calculation Methodology

### Definitions

| Term | Definition |
|------|------------|
| **Gross Revenue** | Total payment received from customers (before any fees) |
| **Platform Fees** | Lemon Squeezy transaction fees + payment processor fees |
| **Net Revenue** | Gross Revenue − Platform Fees |
| **EFF Donation Target** | 10% of Net Revenue |

### Why Net Revenue?

- **Gross revenue** includes fees we never actually receive (Lemon Squeezy keeps ~5% + payment processor fees)
- **Net revenue** reflects the actual money that reaches our bank account
- **Before taxes/expenses**: We donate based on revenue, not profit, to ensure consistency regardless of business costs

### Example Calculation

```
Gross Revenue (month):    $10,000
Platform Fees (5.5%):     −$550
─────────────────────────────────
Net Revenue:              $9,450

EFF Donation (10%):       $945
```

---

## Monthly Donation Workflow

### Step 1: Export Revenue Data from Lemon Squeezy

1. Log in to Lemon Squeezy dashboard
2. Navigate to **Reports** → **Transactions**
3. Set date range (e.g., "Last month" or custom range)
4. Export as **CSV**
5. Save to `tools/donations/data/YYYY-MM-revenue.csv`

**Expected CSV columns**:
- `Date`
- `Order ID`
- `Customer Email` (optional, can be redacted)
- `Gross Amount`
- `Fee Amount`
- `Net Amount`

### Step 2: Run Donation Calculator Script

```bash
cd tools/donations
python calculate_donation.py data/YYYY-MM-revenue.csv
```

**Output**:
```
Foldline EFF Donation Calculator
─────────────────────────────────
Period: 2025-01-01 to 2025-01-31

Gross Revenue:     $10,000.00
Platform Fees:     $550.00
Net Revenue:       $9,450.00

EFF Donation (10%): $945.00
─────────────────────────────────
```

### Step 3: Make Donation to EFF

1. Visit [eff.org/donate](https://www.eff.org/donate)
2. Enter the calculated amount (e.g., $945)
3. Use payment method (credit card, PayPal, etc.)
4. Save receipt to `tools/donations/receipts/YYYY-MM-receipt.pdf`

### Step 4: Record Donation in Ledger

Add entry to `tools/donations/ledger.csv`:

```csv
Date,Period,Gross Revenue,Platform Fees,Net Revenue,Donation Amount,Receipt
2025-02-01,2025-01,10000.00,550.00,9450.00,945.00,receipts/2025-01-receipt.pdf
```

---

## Automation (Future Enhancement)

### GitHub Actions for Monthly Reports

Potential workflow:

```yaml
# .github/workflows/eff-donation-reminder.yml
name: Monthly EFF Donation Reminder

on:
  schedule:
    - cron: '0 9 1 * *'  # 9am on the 1st of each month

jobs:
  reminder:
    runs-on: ubuntu-latest
    steps:
      - name: Create GitHub Issue
        run: |
          gh issue create \
            --title "Monthly EFF Donation - $(date +%Y-%m)" \
            --body "Time to calculate and donate 10% of last month's revenue to the EFF."
```

### Lemon Squeezy API Integration

Instead of manual CSV export:

```python
import requests
import os
from datetime import datetime, timedelta

# Fetch last month's transactions via API
api_key = os.getenv("LEMONSQUEEZY_API_KEY")
store_id = os.getenv("LEMONSQUEEZY_STORE_ID")

# Calculate date range
end_date = datetime.now().replace(day=1) - timedelta(days=1)
start_date = end_date.replace(day=1)

# Call Lemon Squeezy API
response = requests.get(
    f"https://api.lemonsqueezy.com/v1/orders",
    headers={"Authorization": f"Bearer {api_key}"},
    params={
        "filter[store_id]": store_id,
        "filter[created_at][gte]": start_date.isoformat(),
        "filter[created_at][lte]": end_date.isoformat(),
    }
)

# Parse and calculate (see tools/donations/calculate_donation.py)
```

**Note**: Requires API key with read-only access to orders. Not implemented in MVP to avoid storing secrets.

---

## Transparency & Public Reporting

### Annual Summary

At the end of each year, publish:
- **Total gross revenue**
- **Total platform fees**
- **Total net revenue**
- **Total EFF donations**
- **Receipts** (anonymized, amounts only)

Location: `tools/donations/annual-reports/YYYY-summary.md`

### Example Annual Report

```markdown
# Foldline EFF Donations - 2025 Summary

| Month | Gross Revenue | Platform Fees | Net Revenue | EFF Donation |
|-------|---------------|---------------|-------------|--------------|
| Jan   | $10,000       | $550          | $9,450      | $945         |
| Feb   | $12,000       | $660          | $11,340     | $1,134       |
| ...   | ...           | ...           | ...         | ...          |
| **Total** | **$120,000** | **$6,600** | **$113,400** | **$11,340** |

All receipts available in `tools/donations/receipts/2025-*.pdf`.
```

### Optional: Public Dashboard

If Foldline grows, consider:
- Simple HTML page at `foldline.app/eff-donations`
- Shows running total and links to annual reports
- Builds trust with privacy-conscious users

---

## Ledger Schema

**File**: `tools/donations/ledger.csv`

**Columns**:
```csv
Date,Period,Gross Revenue,Platform Fees,Net Revenue,Donation Amount,Receipt,Notes
```

**Example**:
```csv
Date,Period,Gross Revenue,Platform Fees,Net Revenue,Donation Amount,Receipt,Notes
2025-02-01,2025-01,10000.00,550.00,9450.00,945.00,receipts/2025-01-receipt.pdf,First month post-launch
2025-03-01,2025-02,12000.00,660.00,11340.00,1134.00,receipts/2025-02-receipt.pdf,
```

**Notes column** for:
- Special circumstances (e.g., refunds, chargebacks)
- Donations rounded up voluntarily
- Platform fee changes

---

## Edge Cases & Exceptions

### What if there are refunds?

- **Deduct refunds from gross revenue** for that period
- Lemon Squeezy CSV should show refunds as negative amounts
- Script automatically handles this

### What if we lose money in a month?

- If net revenue is negative (more refunds than sales), **donation is $0** for that month
- No "donation debt" carried forward

### What if we want to donate more?

- Rounding up to the nearest $10 or $100 is encouraged
- Record actual donation amount in ledger
- Note in "Notes" column: "Rounded up from $X to $Y"

### What about payment processor disputes?

- Treat disputes as refunds until resolved
- If dispute is won later, include in that month's revenue
- Document in "Notes" column

---

## Tax Considerations

**Disclaimer**: Consult a tax professional for your jurisdiction.

### U.S. Tax Implications

- EFF donations are **tax-deductible** as charitable contributions (EFF is a 501(c)(3))
- Keep all receipts for tax filings
- Report donations separately from business expenses

### International Considerations

- Tax deductibility varies by country
- Some jurisdictions may not recognize U.S. 501(c)(3) status
- May need equivalent privacy rights organization in your country

---

## Tools in This Repository

### `tools/donations/calculate_donation.py`

**Usage**:
```bash
python tools/donations/calculate_donation.py data/2025-01-revenue.csv
```

**Output**:
- Gross revenue total
- Platform fees total
- Net revenue
- 10% donation amount

**Options**:
- `--platform-fee-rate 5.5`: Override default fee percentage
- `--output json`: Output JSON for automation

### `tools/donations/ledger.csv`

**Permanent record** of all donations.

### `tools/donations/data/`

**Storage** for monthly Lemon Squeezy CSV exports (gitignored to protect customer data).

### `tools/donations/receipts/`

**Storage** for EFF donation receipts (gitignored for privacy).

---

## Privacy Considerations

To protect customer privacy:

**Gitignore entries**:
```gitignore
# Donation data (contains customer emails/info)
tools/donations/data/*.csv

# Donation receipts (may contain personal info)
tools/donations/receipts/*.pdf

# Keep the ledger (aggregated, no PII)
!tools/donations/ledger.csv
```

**Script behavior**:
- Never sends data to external services
- Operates only on local files
- Does not log customer-identifying information

---

## FAQ

### Why not automate the donation itself?

- **Accountability**: Manual donations ensure we review the numbers each month
- **Flexibility**: Allows rounding up or adjusting for special circumstances
- **Simplicity**: Avoids complex API integrations and third-party services

### Why 10%?

- **Significant but sustainable**: Enough to make an impact without jeopardizing the business
- **Round number**: Easy to calculate and communicate
- **Common standard**: Many businesses donate 5-10% of revenue or profit

### Can users opt out?

No — the 10% donation is part of Foldline's mission, not a user-selectable option. However:
- **It's transparent**: Users know before purchasing
- **It's efficient**: Comes from our revenue, not added to the price
- **It's aligned**: Privacy-focused users often support the EFF already

### What if Foldline becomes very profitable?

- **10% remains the target** regardless of scale
- If revenue exceeds significant thresholds, consider:
  - Increasing to 15-20%
  - Supporting additional privacy/open-source organizations
  - Creating a Foldline Foundation for broader privacy advocacy

---

## Summary

✅ **Transparent**: Public ledger and annual reports
✅ **Simple**: Monthly CSV → script → donate → record
✅ **Accountable**: Manual process with clear documentation
✅ **Aligned**: Supports organizations defending privacy rights
✅ **Sustainable**: 10% of net revenue, not gross

**Next donation due**: 1st of each month (for previous month's revenue)

**Questions?** See `PAYMENT_ARCHITECTURE.md` for revenue tracking details.
