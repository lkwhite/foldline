# Test Fixtures

This directory contains sample data files for testing.

## FIT Files

To test FIT file parsing, add a minimal valid `.fit` file here:
- `sample_sleep.fit` - Sleep activity
- `sample_activity.fit` - Workout/training activity

You can obtain these from a real Garmin device or GDPR export.

## GDPR Export

To test Garmin GDPR export parsing, create a minimal zip file:
- `garmin_export.zip` - Contains a few sample FIT files in the expected directory structure

## Test Data

`test_data.json` contains synthetic health metrics for testing calculations without requiring real FIT files.
