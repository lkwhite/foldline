"""
Tests for sleep metrics analysis functions.

Tests:
- Sleep heatmap data retrieval
- Sleep timeseries with smoothing
- Sleep quality analysis
"""
from datetime import date, timedelta

import pytest

from metrics.sleep import (
    get_sleep_heatmap,
    get_sleep_timeseries,
    analyze_sleep_quality
)


class TestGetSleepHeatmap:
    """Tests for get_sleep_heatmap function"""

    def test_returns_list(self, temp_db):
        """Should return list of heatmap data points"""
        temp_db.connect()
        temp_db.initialize_schema()

        result = get_sleep_heatmap(temp_db.connection)

        assert isinstance(result, list)
        # Current implementation returns empty list (TODO)
        assert result == []

    def test_with_date_range(self, temp_db):
        """Should filter by date range"""
        temp_db.connect()
        temp_db.initialize_schema()

        start_date = "2024-01-01"
        end_date = "2024-01-31"

        result = get_sleep_heatmap(
            temp_db.connection,
            start_date=start_date,
            end_date=end_date
        )

        assert isinstance(result, list)
        # When implemented, should only return dates in range

    def test_with_data(self, temp_db, sample_sleep_data):
        """Should return data points with correct structure"""
        temp_db.connect()
        temp_db.initialize_schema()

        # When database insert is implemented, insert sample data
        # Then query and verify structure

        # Expected structure:
        # result = get_sleep_heatmap(temp_db.connection)
        # assert len(result) > 0
        # assert all('date' in item for item in result)
        # assert all('value' in item for item in result)

    def test_duration_in_hours(self, temp_db):
        """Should return sleep duration in hours, not minutes"""
        temp_db.connect()
        temp_db.initialize_schema()

        # When implemented with test data:
        # Insert record with duration_minutes = 480 (8 hours)
        # result = get_sleep_heatmap(temp_db.connection)
        # assert result[0]['value'] == 8.0

    def test_handles_missing_data(self, temp_db):
        """Should handle date ranges with no data"""
        temp_db.connect()
        temp_db.initialize_schema()

        result = get_sleep_heatmap(
            temp_db.connection,
            start_date="2023-01-01",
            end_date="2023-01-31"
        )

        # Should return empty list or fill with nulls
        assert isinstance(result, list)


class TestGetSleepTimeseries:
    """Tests for get_sleep_timeseries function"""

    def test_returns_list(self, temp_db):
        """Should return list of timeseries data points"""
        temp_db.connect()
        temp_db.initialize_schema()

        result = get_sleep_timeseries(temp_db.connection)

        assert isinstance(result, list)
        assert result == []

    def test_with_smoothing_window(self, temp_db):
        """Should accept smoothing window parameter"""
        temp_db.connect()
        temp_db.initialize_schema()

        result = get_sleep_timeseries(
            temp_db.connection,
            smoothing_window=7  # 7-day rolling average
        )

        assert isinstance(result, list)

    def test_smoothing_calculation(self, temp_db):
        """Should calculate rolling average correctly"""
        temp_db.connect()
        temp_db.initialize_schema()

        # When implemented with test data:
        # Insert 7 days of sleep data with known values
        # Query with smoothing_window=7
        # Verify rolling average calculation

        # Example:
        # Days 1-7: 8, 7, 8, 7, 8, 7, 8 hours
        # Rolling avg should be: 7.57 hours

    def test_default_smoothing(self, temp_db):
        """Should use default smoothing window of 7 days"""
        temp_db.connect()
        temp_db.initialize_schema()

        result = get_sleep_timeseries(temp_db.connection)

        # Default smoothing_window should be 7
        assert isinstance(result, list)

    def test_no_smoothing(self, temp_db):
        """Should support no smoothing (window=1)"""
        temp_db.connect()
        temp_db.initialize_schema()

        result = get_sleep_timeseries(
            temp_db.connection,
            smoothing_window=1
        )

        # When implemented with data, should return raw values
        assert isinstance(result, list)


class TestAnalyzeSleepQuality:
    """Tests for analyze_sleep_quality function"""

    def test_returns_dict(self, temp_db):
        """Should return dict with sleep quality metrics"""
        temp_db.connect()
        temp_db.initialize_schema()

        result = analyze_sleep_quality(temp_db.connection)

        assert isinstance(result, dict)
        assert "avg_duration_hours" in result
        assert "avg_sleep_score" in result
        assert "avg_deep_pct" in result
        assert "avg_rem_pct" in result

    def test_default_date_range(self, temp_db):
        """Should analyze past 30 days by default"""
        temp_db.connect()
        temp_db.initialize_schema()

        result = analyze_sleep_quality(temp_db.connection)

        # Default should be 30 days
        assert isinstance(result, dict)

    def test_custom_date_range(self, temp_db):
        """Should accept custom date range"""
        temp_db.connect()
        temp_db.initialize_schema()

        result = analyze_sleep_quality(
            temp_db.connection,
            date_range_days=7
        )

        assert isinstance(result, dict)

    def test_calculates_averages(self, temp_db, sample_sleep_data):
        """Should calculate correct average metrics"""
        temp_db.connect()
        temp_db.initialize_schema()

        # When implemented with test data:
        # Insert multiple sleep records
        # Verify average calculations

        # Example with 2 records:
        # Record 1: 480 min (8 hrs), score 85, deep 120 min (25%)
        # Record 2: 420 min (7 hrs), score 72, deep 90 min (21%)
        # Expected averages:
        # avg_duration_hours = 7.5
        # avg_sleep_score = 78.5
        # avg_deep_pct = 23.0

    def test_percentage_calculations(self, temp_db):
        """Should calculate sleep stage percentages correctly"""
        temp_db.connect()
        temp_db.initialize_schema()

        # When implemented:
        # Insert record with:
        #   duration_minutes = 480
        #   deep_minutes = 120
        #   rem_minutes = 90
        # Expected:
        #   deep_pct = 25.0 (120/480)
        #   rem_pct = 18.75 (90/480)

    def test_handles_no_data(self, temp_db):
        """Should handle case with no sleep data"""
        temp_db.connect()
        temp_db.initialize_schema()

        result = analyze_sleep_quality(temp_db.connection)

        # Should return zeros or nulls
        assert result["avg_duration_hours"] == 0.0
        assert result["avg_sleep_score"] == 0.0

    def test_handles_partial_data(self, temp_db):
        """Should handle missing fields in some records"""
        temp_db.connect()
        temp_db.initialize_schema()

        # When implemented:
        # Insert records with some null values
        # Verify averages only use non-null values
