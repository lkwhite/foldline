# Foldline Donation Tools

This directory contains tools for calculating and tracking the 10% EFF donation commitment.

## Quick Start

1. **Export revenue data** from Lemon Squeezy (CSV format)
2. **Save to** `data/YYYY-MM-revenue.csv`
3. **Run calculator**:
   ```bash
   python calculate_donation.py data/2025-01-revenue.csv
   ```
4. **Donate** the calculated amount at [eff.org/donate](https://www.eff.org/donate)
5. **Record** donation in `ledger.csv`

## Directory Structure

```
tools/donations/
├── calculate_donation.py    # Donation calculator script
├── ledger.csv               # Permanent donation record (tracked in git)
├── data/                    # CSV exports (gitignored)
│   └── sample-revenue.csv   # Example CSV format
├── receipts/                # Donation receipts (gitignored)
└── annual-reports/          # Yearly summaries
```

## Usage Examples

### Basic Calculation

```bash
python calculate_donation.py data/2025-01-revenue.csv
```

Output:
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

### Custom Platform Fee Rate

If Lemon Squeezy changes their fee structure:

```bash
python calculate_donation.py data/2025-01-revenue.csv --platform-fee-rate 6.0
```

### JSON Output (for automation)

```bash
python calculate_donation.py data/2025-01-revenue.csv --output json
```

Output:
```json
{
  "period_start": "2025-01-01",
  "period_end": "2025-01-31",
  "transaction_count": 42,
  "gross_revenue": 10000.00,
  "platform_fees": 550.00,
  "net_revenue": 9450.00,
  "donation_amount": 945.00,
  "donation_percentage": 10.0,
  "fee_method": "explicit"
}
```

## CSV Format

The script expects a CSV with these columns (names may vary):

| Column | Variations | Required |
|--------|-----------|----------|
| Date | `Date`, `date`, `Created At` | Yes |
| Order ID | `Order ID`, `order_id` | No |
| Gross Amount | `Gross Amount`, `Amount`, `Total` | Yes |
| Fee Amount | `Fee Amount`, `Fee`, `Fees` | No* |
| Net Amount | `Net Amount`, `Net` | No* |

*If fee/net columns are missing, fees are estimated using `--platform-fee-rate`

## Monthly Workflow

1. **Export CSV** from Lemon Squeezy on the 1st of each month
2. **Calculate donation**:
   ```bash
   python calculate_donation.py data/2025-01-revenue.csv
   ```
3. **Make donation** at eff.org
4. **Save receipt** to `receipts/2025-01-receipt.pdf`
5. **Update ledger**:
   ```csv
   2025-02-01,2025-01,10000.00,550.00,9450.00,945.00,receipts/2025-01-receipt.pdf,
   ```

## Ledger Format

`ledger.csv` tracks all donations:

```csv
Date,Period,Gross Revenue,Platform Fees,Net Revenue,Donation Amount,Receipt,Notes
2025-02-01,2025-01,10000.00,550.00,9450.00,945.00,receipts/2025-01-receipt.pdf,First month
```

**Columns:**
- `Date`: When donation was made
- `Period`: Revenue period (YYYY-MM)
- `Gross Revenue`: Total customer payments
- `Platform Fees`: Lemon Squeezy + payment processor fees
- `Net Revenue`: Gross - Fees
- `Donation Amount`: 10% of net revenue (actual donated amount)
- `Receipt`: Path to donation receipt PDF
- `Notes`: Optional notes (refunds, rounding, etc.)

## Privacy & Security

- **Never commit** CSV files with customer data (gitignored automatically)
- **Never commit** donation receipts (may contain personal info)
- **Do commit** the ledger (aggregated data only, no PII)

## Troubleshooting

### "File not found" error

Make sure the CSV path is correct:
```bash
ls data/2025-01-revenue.csv
```

### Unexpected donation amount

Check if:
- CSV has fee columns (script will use explicit fees if present)
- Platform fee rate is correct (default: 5.5%)
- CSV contains refunds (shown as negative amounts)

### Different CSV format

The script tries to handle different column names. If it fails:
1. Check the CSV has a header row
2. Verify column names match expected variations
3. Manually rename columns if needed

## See Also

- [EFF_DONATIONS.md](../../EFF_DONATIONS.md) - Full donation plan documentation
- [PAYMENT_ARCHITECTURE.md](../../PAYMENT_ARCHITECTURE.md) - Payment system overview
