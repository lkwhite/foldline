"""
Tests for field_mappings module.

Tests field name variations and mapping functions for:
- Sleep data
- Daily summaries
- HRV
- Stress
- Activities
- Other data types
"""
import pytest
from datetime import datetime, date

from ingestion.field_mappings import (
    get_field_value,
    map_sleep_record,
    map_daily_summary_record,
    map_hrv_record,
    map_stress_record,
    map_activity_record,
    parse_date,
    parse_timestamp,
    SLEEP_FIELD_MAPPINGS,
    DAILY_SUMMARY_FIELD_MAPPINGS
)


class TestGetFieldValue:
    """Tests for get_field_value helper function"""

    def test_returns_first_match(self):
        """Should return first matching field"""
        data = {"field1": "value1", "field2": "value2"}
        result = get_field_value(data, ["field1", "field2"])
        assert result == "value1"

    def test_returns_second_match_when_first_missing(self):
        """Should try alternatives when first is missing"""
        data = {"field2": "value2"}
        result = get_field_value(data, ["field1", "field2"])
        assert result == "value2"

    def test_returns_default_when_no_match(self):
        """Should return default when no fields match"""
        data = {"field3": "value3"}
        result = get_field_value(data, ["field1", "field2"], default="default")
        assert result == "default"

    def test_skips_none_values(self):
        """Should skip None values and continue searching"""
        data = {"field1": None, "field2": "value2"}
        result = get_field_value(data, ["field1", "field2"])
        assert result == "value2"


class TestMapSleepRecord:
    """Tests for map_sleep_record function"""

    def test_maps_all_standard_fields(self):
        """Should map all standard Garmin sleep fields"""
        garmin_data = {
            "calendarDate": "2024-01-15",
            "sleepStartTimestampGMT": "2024-01-15T02:00:00.0",
            "sleepEndTimestampGMT": "2024-01-15T10:00:00.0",
            "deepSleepSeconds": 7200,
            "lightSleepSeconds": 18000,
            "remSleepSeconds": 3600,
            "awakeSleepSeconds": 600,
            "averageRespiration": 14.5,
            "lowestRespiration": 12.0,
            "highestRespiration": 18.0,
            "averageSpO2Value": 96.5,
            "lowestSpO2Value": 94.0,
            "avgSleepHeartRate": 55
        }

        result = map_sleep_record(garmin_data)

        assert result["calendar_date"] == "2024-01-15"
        assert result["sleep_start_gmt"] == "2024-01-15T02:00:00.0"
        assert result["deep_sleep_seconds"] == 7200
        assert result["light_sleep_seconds"] == 18000
        assert result["rem_sleep_seconds"] == 3600
        assert result["average_respiration"] == 14.5
        assert result["average_spo2"] == 96.5

    def test_handles_alternative_field_names(self):
        """Should handle alternative field names"""
        garmin_data = {
            "date": "2024-01-15",  # Alternative to calendarDate
            "sleepStart": "2024-01-15T02:00:00.0",  # Alternative to sleepStartTimestampGMT
            "deepSleep": 7200,  # Alternative to deepSleepSeconds
            "lightSleep": 18000,
            "remSleep": 3600
        }

        result = map_sleep_record(garmin_data)

        assert result["calendar_date"] == "2024-01-15"
        assert result["sleep_start_gmt"] == "2024-01-15T02:00:00.0"
        assert result["deep_sleep_seconds"] == 7200

    def test_handles_missing_optional_fields(self):
        """Should handle missing optional fields gracefully"""
        garmin_data = {
            "deepSleepSeconds": 7200,
            "lightSleepSeconds": 18000
        }

        result = map_sleep_record(garmin_data)

        assert result["deep_sleep_seconds"] == 7200
        assert "average_spo2" not in result or result["average_spo2"] is None


class TestMapDailySummaryRecord:
    """Tests for map_daily_summary_record function"""

    def test_maps_all_standard_fields(self):
        """Should map all standard daily summary fields"""
        garmin_data = {
            "calendarDate": "2024-01-15",
            "totalSteps": 10000,
            "totalKilocalories": 2500,
            "totalDistanceMeters": 8000,
            "floorsAscended": 10,
            "minHeartRate": 45,
            "maxHeartRate": 175,
            "restingHeartRate": 55,
            "averageHeartRate": 75,
            "averageStressLevel": 35,
            "maxStressLevel": 85,
            "restStressLevel": 15,
            "bodyBatteryChargedValue": 60,
            "bodyBatteryDrainedValue": 55,
            "moderateIntensityMinutes": 30,
            "vigorousIntensityMinutes": 20
        }

        result = map_daily_summary_record(garmin_data)

        assert result["calendar_date"] == "2024-01-15"
        assert result["step_count"] == 10000
        assert result["calories_burned"] == 2500
        assert result["distance_meters"] == 8000
        assert result["floors_climbed"] == 10
        assert result["resting_heart_rate"] == 55
        assert result["stress_avg"] == 35
        assert result["body_battery_charged"] == 60

    def test_handles_alternative_field_names(self):
        """Should handle alternative field names for daily summaries"""
        garmin_data = {
            "date": "2024-01-15",  # Alternative to calendarDate
            "steps": 10000,  # Alternative to totalSteps
            "restingHR": 55,  # Alternative to restingHeartRate
            "calories": 2500  # Alternative to totalKilocalories
        }

        result = map_daily_summary_record(garmin_data)

        assert result["calendar_date"] == "2024-01-15"
        assert result["step_count"] == 10000
        assert result["resting_heart_rate"] == 55
        assert result["calories_burned"] == 2500


class TestMapHrvRecord:
    """Tests for map_hrv_record function"""

    def test_maps_hrv_fields(self):
        """Should map HRV fields correctly"""
        garmin_data = {
            "calendarDate": "2024-01-15",
            "weeklyAvg": 55.0
        }

        result = map_hrv_record(garmin_data)

        assert result["calendar_date"] == "2024-01-15"
        assert result["hrv_value"] == 55.0

    def test_sets_default_measurement_type(self):
        """Should set measurement type based on field name"""
        garmin_data = {
            "rmssd": 55.0
        }

        result = map_hrv_record(garmin_data)

        assert result["measurement_type"] == "rmssd"


class TestMapStressRecord:
    """Tests for map_stress_record function"""

    def test_maps_stress_fields(self):
        """Should map stress fields correctly"""
        garmin_data = {
            "calendarDate": "2024-01-15",
            "avgStressLevel": 35,
            "maxStressLevel": 85,
            "restStressLevel": 15
        }

        result = map_stress_record(garmin_data)

        assert result["calendar_date"] == "2024-01-15"
        assert result["avg_stress"] == 35
        assert result["max_stress"] == 85
        assert result["min_stress"] == 15


class TestMapActivityRecord:
    """Tests for map_activity_record function"""

    def test_maps_activity_fields(self):
        """Should map activity fields correctly"""
        garmin_data = {
            "activityId": "12345",
            "startTimeGMT": "2024-01-15T08:00:00.0",
            "activityType": "running",
            "duration": 3600,
            "distance": 10000,
            "averageHR": 150,
            "maxHR": 175,
            "aerobicTrainingEffect": 3.5
        }

        result = map_activity_record(garmin_data)

        assert result["activity_id"] == "12345"
        assert result["start_time"] == "2024-01-15T08:00:00.0"
        assert result["activity_type"] == "running"
        assert result["duration_seconds"] == 3600
        assert result["distance_meters"] == 10000
        assert result["avg_hr"] == 150
        assert result["training_effect_aerobic"] == 3.5


class TestParseDateFunction:
    """Tests for parse_date helper function"""

    def test_parses_iso_date(self):
        """Should parse ISO date format"""
        result = parse_date("2024-01-15")
        assert result == date(2024, 1, 15)

    def test_parses_datetime_string(self):
        """Should parse datetime string and extract date"""
        result = parse_date("2024-01-15T08:30:00.0")
        assert result == date(2024, 1, 15)

    def test_handles_invalid_date(self):
        """Should return None for invalid date"""
        result = parse_date("not a date")
        assert result is None

    def test_handles_empty_string(self):
        """Should return None for empty string"""
        result = parse_date("")
        assert result is None

    def test_handles_none(self):
        """Should return None for None input"""
        result = parse_date(None)
        assert result is None


class TestParseTimestampFunction:
    """Tests for parse_timestamp helper function"""

    def test_parses_iso_timestamp(self):
        """Should parse ISO timestamp"""
        result = parse_timestamp("2024-01-15T08:30:00.0")
        assert isinstance(result, datetime)
        assert result.year == 2024
        assert result.month == 1
        assert result.day == 15
        assert result.hour == 8
        assert result.minute == 30

    def test_handles_z_timezone(self):
        """Should handle Z timezone marker"""
        result = parse_timestamp("2024-01-15T08:30:00Z")
        assert isinstance(result, datetime)

    def test_handles_invalid_timestamp(self):
        """Should return None for invalid timestamp"""
        result = parse_timestamp("not a timestamp")
        assert result is None

    def test_handles_empty_string(self):
        """Should return None for empty string"""
        result = parse_timestamp("")
        assert result is None


class TestFieldMappingsDictionaries:
    """Tests for field mapping dictionaries structure"""

    def test_sleep_mappings_structure(self):
        """Should have all required sleep field mappings"""
        required_fields = [
            "sleep_start_gmt",
            "sleep_end_gmt",
            "deep_sleep_seconds",
            "light_sleep_seconds",
            "rem_sleep_seconds",
            "awake_sleep_seconds",
            "average_spo2"
        ]

        for field in required_fields:
            assert field in SLEEP_FIELD_MAPPINGS
            assert isinstance(SLEEP_FIELD_MAPPINGS[field], list)
            assert len(SLEEP_FIELD_MAPPINGS[field]) > 0

    def test_daily_summary_mappings_structure(self):
        """Should have all required daily summary field mappings"""
        required_fields = [
            "step_count",
            "calories_burned",
            "resting_heart_rate",
            "stress_avg",
            "body_battery_charged"
        ]

        for field in required_fields:
            assert field in DAILY_SUMMARY_FIELD_MAPPINGS
            assert isinstance(DAILY_SUMMARY_FIELD_MAPPINGS[field], list)
            assert len(DAILY_SUMMARY_FIELD_MAPPINGS[field]) > 0


class TestRealWorldScenarios:
    """Tests with real-world data structures"""

    def test_handles_incomplete_sleep_data(self):
        """Should handle incomplete sleep data gracefully"""
        garmin_data = {
            "deepSleepSeconds": 7200
            # Missing many optional fields
        }

        result = map_sleep_record(garmin_data)

        assert result["deep_sleep_seconds"] == 7200
        # Should not crash, just return available data

    def test_handles_extra_unknown_fields(self):
        """Should ignore unknown fields without crashing"""
        garmin_data = {
            "calendarDate": "2024-01-15",
            "totalSteps": 10000,
            "unknownField1": "value1",
            "unknownField2": 123,
            "anotherWeirdField": {"nested": "object"}
        }

        result = map_daily_summary_record(garmin_data)

        assert result["calendar_date"] == "2024-01-15"
        assert result["step_count"] == 10000
        # Unknown fields are simply not mapped

    def test_field_name_case_sensitivity(self):
        """Field names are case-sensitive, verifies correct mapping"""
        garmin_data = {
            "totalSteps": 10000,  # Correct case
            "totalsteps": 5000,   # Wrong case - should be ignored
            "TOTALSTEPS": 3000    # Wrong case - should be ignored
        }

        result = map_daily_summary_record(garmin_data)

        # Should only map the correctly-cased field
        assert result["step_count"] == 10000
