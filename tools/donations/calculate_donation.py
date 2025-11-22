#!/usr/bin/env python3
"""
Foldline EFF Donation Calculator

Calculates 10% donation to EFF based on net revenue from Lemon Squeezy CSV exports.

Usage:
    python calculate_donation.py data/2025-01-revenue.csv
    python calculate_donation.py data/2025-01-revenue.csv --platform-fee-rate 5.5
    python calculate_donation.py data/2025-01-revenue.csv --output json
"""

import argparse
import csv
import json
import sys
from datetime import datetime
from decimal import Decimal
from pathlib import Path
from typing import Dict, List, Tuple


class DonationCalculator:
    """Calculate EFF donations from Lemon Squeezy revenue data."""

    def __init__(self, platform_fee_rate: float = 5.5):
        """
        Initialize calculator.

        Args:
            platform_fee_rate: Platform fee percentage (default: 5.5%)
        """
        self.platform_fee_rate = Decimal(str(platform_fee_rate))

    def parse_csv(self, csv_path: Path) -> Tuple[List[Dict], str, str]:
        """
        Parse Lemon Squeezy CSV export.

        Expected columns:
        - Date (YYYY-MM-DD format)
        - Order ID
        - Gross Amount (or Amount, or Total)
        - Fee Amount (optional)
        - Net Amount (optional)

        Args:
            csv_path: Path to CSV file

        Returns:
            Tuple of (transactions, start_date, end_date)
        """
        transactions = []
        dates = []

        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)

            # Normalize column names (handle variations)
            for row in reader:
                # Try different column name variations
                gross = self._get_amount(row, ['Gross Amount', 'Amount', 'Total', 'gross_amount'])
                fee = self._get_amount(row, ['Fee Amount', 'Fee', 'fee_amount', 'Fees'])
                net = self._get_amount(row, ['Net Amount', 'Net', 'net_amount'])
                date = row.get('Date') or row.get('date') or row.get('Created At') or ''

                if date:
                    dates.append(date)

                transactions.append({
                    'date': date,
                    'order_id': row.get('Order ID') or row.get('order_id') or 'N/A',
                    'gross': gross,
                    'fee': fee,
                    'net': net,
                })

        # Determine date range
        dates_sorted = sorted(dates) if dates else []
        start_date = dates_sorted[0] if dates_sorted else 'Unknown'
        end_date = dates_sorted[-1] if dates_sorted else 'Unknown'

        return transactions, start_date, end_date

    def _get_amount(self, row: Dict, column_names: List[str]) -> Decimal:
        """Try to extract amount from row using multiple column name variations."""
        for col in column_names:
            if col in row and row[col]:
                try:
                    # Remove currency symbols and commas
                    amount_str = row[col].replace('$', '').replace(',', '').strip()
                    return Decimal(amount_str)
                except (ValueError, KeyError):
                    continue
        return Decimal('0')

    def calculate(self, csv_path: Path) -> Dict:
        """
        Calculate donation amount from CSV.

        Args:
            csv_path: Path to Lemon Squeezy CSV export

        Returns:
            Dict with calculation results
        """
        transactions, start_date, end_date = self.parse_csv(csv_path)

        gross_revenue = Decimal('0')
        explicit_fees = Decimal('0')
        explicit_net = Decimal('0')
        has_fee_column = False
        has_net_column = False

        for txn in transactions:
            gross_revenue += txn['gross']

            if txn['fee'] > 0:
                has_fee_column = True
                explicit_fees += txn['fee']

            if txn['net'] > 0:
                has_net_column = True
                explicit_net += txn['net']

        # Calculate fees and net revenue
        if has_fee_column:
            # Use explicit fees from CSV
            platform_fees = explicit_fees
            net_revenue = gross_revenue - platform_fees
        elif has_net_column:
            # Use explicit net from CSV
            net_revenue = explicit_net
            platform_fees = gross_revenue - net_revenue
        else:
            # Estimate fees using platform fee rate
            platform_fees = gross_revenue * (self.platform_fee_rate / Decimal('100'))
            net_revenue = gross_revenue - platform_fees

        # Calculate 10% donation
        donation_amount = net_revenue * Decimal('0.10')

        return {
            'period_start': start_date,
            'period_end': end_date,
            'transaction_count': len(transactions),
            'gross_revenue': gross_revenue,
            'platform_fees': platform_fees,
            'net_revenue': net_revenue,
            'donation_amount': donation_amount,
            'donation_percentage': 10.0,
            'fee_method': 'explicit' if has_fee_column else 'estimated',
        }

    def format_currency(self, amount: Decimal) -> str:
        """Format Decimal as currency string."""
        return f"${amount:,.2f}"

    def print_report(self, results: Dict) -> None:
        """Print human-readable report."""
        print("Foldline EFF Donation Calculator")
        print("─" * 37)
        print(f"Period: {results['period_start']} to {results['period_end']}")
        print(f"Transactions: {results['transaction_count']}")
        print()
        print(f"Gross Revenue:     {self.format_currency(results['gross_revenue'])}")
        print(f"Platform Fees:     {self.format_currency(results['platform_fees'])}", end='')
        if results['fee_method'] == 'estimated':
            print(f" (estimated at {self.platform_fee_rate}%)")
        else:
            print()
        print(f"Net Revenue:       {self.format_currency(results['net_revenue'])}")
        print()
        print(f"EFF Donation (10%): {self.format_currency(results['donation_amount'])}")
        print("─" * 37)


def main():
    parser = argparse.ArgumentParser(
        description='Calculate EFF donation from Lemon Squeezy revenue CSV'
    )
    parser.add_argument(
        'csv_file',
        type=Path,
        help='Path to Lemon Squeezy CSV export'
    )
    parser.add_argument(
        '--platform-fee-rate',
        type=float,
        default=5.5,
        help='Platform fee percentage (default: 5.5%%)'
    )
    parser.add_argument(
        '--output',
        choices=['text', 'json'],
        default='text',
        help='Output format (default: text)'
    )

    args = parser.parse_args()

    # Check if file exists
    if not args.csv_file.exists():
        print(f"Error: File not found: {args.csv_file}", file=sys.stderr)
        sys.exit(1)

    # Calculate donation
    calculator = DonationCalculator(platform_fee_rate=args.platform_fee_rate)

    try:
        results = calculator.calculate(args.csv_file)

        if args.output == 'json':
            # Convert Decimal to float for JSON serialization
            json_results = {
                k: float(v) if isinstance(v, Decimal) else v
                for k, v in results.items()
            }
            print(json.dumps(json_results, indent=2))
        else:
            calculator.print_report(results)

    except Exception as e:
        print(f"Error processing CSV: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
