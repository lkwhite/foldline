#!/usr/bin/env python3
"""
Create sample JSON files to test the JSON processing pipeline
"""

import json
import os
from datetime import datetime, date, timedelta

# Create test directory
test_dir = "/tmp/sample_garmin_json"
os.makedirs(test_dir, exist_ok=True)

# Sample sleep JSON data (based on real Garmin export structure)
sleep_data = [
    {
        "sleepTimeSeconds": 25200,  # 7 hours
        "napTimeSeconds": 0,
        "sleepStartTimestampGMT": "2024-01-15T02:00:00.0",
        "sleepEndTimestampGMT": "2024-01-15T09:00:00.0",
        "deepSleepSeconds": 7200,   # 2 hours deep
        "lightSleepSeconds": 16200,  # 4.5 hours light
        "remSleepSeconds": 1800,    # 30 min REM
        "awakeSleepSeconds": 0,     # No awake time
        "sleepWindowConfirmationType": "ENHANCED_CONFIRMED_FINAL",
        "averageRespiration": 14.5,
        "lowestRespiration": 12.0,
        "highestRespiration": 18.0,
        "avgSleepStress": 8.5,
        "averageSpO2Value": 96.5,
        "lowestSpO2Value": 94.0,
        "avgSleepHeartRate": 55
    },
    {
        "sleepTimeSeconds": 28800,  # 8 hours
        "napTimeSeconds": 1800,     # 30 min nap
        "sleepStartTimestampGMT": "2024-01-16T01:30:00.0",
        "sleepEndTimestampGMT": "2024-01-16T09:30:00.0",
        "deepSleepSeconds": 9000,   # 2.5 hours deep
        "lightSleepSeconds": 18000,  # 5 hours light
        "remSleepSeconds": 1800,    # 30 min REM
        "awakeSleepSeconds": 0,
        "sleepWindowConfirmationType": "ENHANCED_CONFIRMED_FINAL",
        "averageRespiration": 13.8,
        "lowestRespiration": 11.5,
        "highestRespiration": 16.2,
        "avgSleepStress": 7.2,
        "averageSpO2Value": 97.1,
        "lowestSpO2Value": 95.3,
        "avgSleepHeartRate": 52
    },
    {
        "sleepTimeSeconds": 22500,  # 6.25 hours
        "napTimeSeconds": 0,
        "sleepStartTimestampGMT": "2024-01-17T02:15:00.0",
        "sleepEndTimestampGMT": "2024-01-17T08:30:00.0",
        "deepSleepSeconds": 6300,   # 1.75 hours deep
        "lightSleepSeconds": 14400,  # 4 hours light
        "remSleepSeconds": 1800,    # 30 min REM
        "awakeSleepSeconds": 0,
        "sleepWindowConfirmationType": "ENHANCED_CONFIRMED_FINAL",
        "averageRespiration": 15.2,
        "lowestRespiration": 12.8,
        "highestRespiration": 19.1,
        "avgSleepStress": 9.8,
        "averageSpO2Value": 96.0,
        "lowestSpO2Value": 93.5,
        "avgSleepHeartRate": 58
    }
]

# Sample daily summary data (UDS format)
daily_summary_data = [
    {
        "calendarDate": "2024-01-15",
        "totalSteps": 8432,
        "totalKilocalories": 2150,
        "totalDistanceMeters": 6421,
        "floorsAscended": 12,
        "activeKilocalories": 485,
        "sedentaryKilocalories": 1665,
        "minHeartRate": 48,
        "maxHeartRate": 165,
        "restingHeartRate": 58,
        "averageHeartRate": 78,
        "averageStressLevel": 22.5,
        "maxStressLevel": 85,
        "restStressLevel": 12,
        "bodyBatteryChargedValue": 45,
        "bodyBatteryDrainedValue": 65,
        "bodyBatteryHighestValue": 85,
        "bodyBatteryLowestValue": 20,
        "moderateIntensityMinutes": 28,
        "vigorousIntensityMinutes": 15
    },
    {
        "calendarDate": "2024-01-16",
        "totalSteps": 12156,
        "totalKilocalories": 2380,
        "totalDistanceMeters": 9234,
        "floorsAscended": 18,
        "activeKilocalories": 612,
        "sedentaryKilocalories": 1768,
        "minHeartRate": 45,
        "maxHeartRate": 178,
        "restingHeartRate": 56,
        "averageHeartRate": 82,
        "averageStressLevel": 28.3,
        "maxStressLevel": 92,
        "restStressLevel": 15,
        "bodyBatteryChargedValue": 55,
        "bodyBatteryDrainedValue": 75,
        "bodyBatteryHighestValue": 90,
        "bodyBatteryLowestValue": 15,
        "moderateIntensityMinutes": 45,
        "vigorousIntensityMinutes": 22
    }
]

# Create sleep JSON files
for i, sleep_record in enumerate(sleep_data):
    sleep_date = sleep_record["sleepStartTimestampGMT"][:10]  # Extract YYYY-MM-DD
    filename = f"sleep_{sleep_date}.json"
    filepath = os.path.join(test_dir, filename)

    with open(filepath, 'w') as f:
        json.dump(sleep_record, f, indent=2)

    print(f"Created: {filepath}")

# Create daily summary files
for i, summary_record in enumerate(daily_summary_data):
    summary_date = summary_record["calendarDate"]
    filename = f"UdsFile_{summary_date}.json"
    filepath = os.path.join(test_dir, filename)

    with open(filepath, 'w') as f:
        json.dump(summary_record, f, indent=2)

    print(f"Created: {filepath}")

print(f"\nSample JSON files created in: {test_dir}")
print("Files created:")
for file in sorted(os.listdir(test_dir)):
    print(f"  {file}")