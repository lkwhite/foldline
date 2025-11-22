#!/usr/bin/env python3
"""
Debug script to explore FIT file structure and message types
"""

import sys
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_path))

try:
    from fitparse import FitFile
except ImportError:
    print("ERROR: fitparse library not available")
    sys.exit(1)

def debug_fit_file():
    """Explore the structure of multiple real FIT files"""
    fit_files = [
        "/tmp/laura.white@gmail.com_108471997439.fit",
        "/tmp/laura.white@gmail.com_53902275619.fit",
        "/tmp/laura.white@gmail.com_76966352163.fit"
    ]

    for fit_file_path in fit_files:
        if not Path(fit_file_path).exists():
            print(f"ERROR: FIT file not found: {fit_file_path}")
            continue

        print(f"Debugging FIT file: {fit_file_path}")
        print("=" * 60)
        debug_single_file(fit_file_path)
        print("\n" + "=" * 60 + "\n")

def debug_single_file(fit_file_path):
    """Debug a single FIT file"""

    fitfile = FitFile(fit_file_path)

    # Track message types and their counts
    message_types = {}
    total_messages = 0

    # First pass: collect all message types
    for record in fitfile.get_messages():
        message_type = record.name
        total_messages += 1

        if message_type not in message_types:
            message_types[message_type] = {
                'count': 0,
                'fields': set(),
                'sample_data': {}
            }

        message_types[message_type]['count'] += 1

        # Collect field names and sample data
        for field in record:
            if field.value is not None:
                message_types[message_type]['fields'].add(field.name)
                # Store first non-null value as sample
                if field.name not in message_types[message_type]['sample_data']:
                    message_types[message_type]['sample_data'][field.name] = field.value

    # Display summary
    print(f"Total messages: {total_messages}")
    print(f"Message types found: {len(message_types)}")
    print()

    # Display each message type with details
    for msg_type, data in sorted(message_types.items()):
        print(f"Message Type: {msg_type}")
        print(f"  Count: {data['count']}")
        print(f"  Fields: {sorted(data['fields'])}")

        if data['sample_data']:
            print("  Sample data:")
            for field_name, sample_value in sorted(data['sample_data'].items()):
                print(f"    {field_name}: {sample_value} ({type(sample_value).__name__})")

        print()

if __name__ == "__main__":
    debug_fit_file()