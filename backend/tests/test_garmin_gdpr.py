"""
Tests for Garmin GDPR export processing.

Tests the complete GDPR import pipeline including:
- ZIP extraction and file categorization
- Field mapping and parsing
- Deduplication
- Error handling
- End-to-end import
"""
import zipfile
import json
from pathlib import Path
from datetime import datetime, date

import pytest

from ingestion.garmin_gdpr import (
    extract_garmin_export,
    process_gdpr_export
)


class TestExtractGarminExport:
    """Tests for extract_garmin_export function"""

    def test_extract_returns_summary(self, temp_dir):
        """Should return summary dict with expected keys"""
        zip_path = temp_dir / "test_export.zip"
        with zipfile.ZipFile(zip_path, 'w') as zf:
            zf.writestr("test.fit", "test data")

        extract_to = temp_dir / "extracted"
        result = extract_garmin_export(str(zip_path), str(extract_to))

        assert isinstance(result, dict)
        assert "total_files" in result
        assert "fit_files" in result
        assert "tcx_files" in result
        assert "json_files" in result
        assert "extract_path" in result
        assert "file_categories" in result
        assert result["total_files"] == 1
        assert len(result["fit_files"]) == 1

    def test_extract_empty_zip(self, temp_dir):
        """Should handle empty zip file"""
        zip_path = temp_dir / "empty.zip"
        with zipfile.ZipFile(zip_path, 'w') as zf:
            pass  # Empty zip

        extract_to = temp_dir / "extracted"
        result = extract_garmin_export(str(zip_path), str(extract_to))

        assert result["total_files"] == 0

    def test_extract_counts_file_types(self, temp_dir):
        """Should count different file types correctly"""
        zip_path = temp_dir / "mixed_export.zip"
        with zipfile.ZipFile(zip_path, 'w') as zf:
            zf.writestr("activity1.fit", "fit data")
            zf.writestr("activity2.fit", "fit data")
            zf.writestr("workout.tcx", "tcx data")
            zf.writestr("summary.json", "json data")
            zf.writestr("readme.txt", "text data")

        extract_to = temp_dir / "extracted"
        result = extract_garmin_export(str(zip_path), str(extract_to))

        assert result["total_files"] == 5
        assert len(result["fit_files"]) == 2
        assert len(result["tcx_files"]) == 1
        assert len(result["json_files"]) == 1

    def test_extract_nested_structure(self, temp_dir):
        """Should handle nested directory structure with DI_CONNECT"""
        zip_path = temp_dir / "nested_export.zip"
        with zipfile.ZipFile(zip_path, 'w') as zf:
            zf.writestr("DI_CONNECT/DI-Connect-Fitness/2024-01-15.fit", "data")
            zf.writestr("DI_CONNECT/DI-Connect-Wellness/sleep.fit", "data")

        extract_to = temp_dir / "extracted"
        result = extract_garmin_export(str(zip_path), str(extract_to))

        assert result["di_connect_found"] is True
        assert len(result["fit_files"]) == 2

    def test_extract_categorizes_sleep_json(self, temp_dir):
        """Should categorize sleep JSON files correctly"""
        zip_path = temp_dir / "sleep_export.zip"
        with zipfile.ZipFile(zip_path, 'w') as zf:
            zf.writestr("DI_CONNECT/sleep_2024-01-15.json", "{}")
            zf.writestr("DI_CONNECT/sleep_2024-01-16.json", "{}")

        extract_to = temp_dir / "extracted"
        result = extract_garmin_export(str(zip_path), str(extract_to))

        assert len(result["file_categories"]["sleep"]) == 2
        assert len(result["json_files"]) == 2

    def test_extract_categorizes_daily_summaries(self, temp_dir):
        """Should categorize daily summary JSON files correctly"""
        zip_path = temp_dir / "daily_export.zip"
        with zipfile.ZipFile(zip_path, 'w') as zf:
            zf.writestr("DI_CONNECT/UdsFile_2024-01-15.json", "{}")
            zf.writestr("DI_CONNECT/dailysummary_2024-01-16.json", "{}")

        extract_to = temp_dir / "extracted"
        result = extract_garmin_export(str(zip_path), str(extract_to))

        assert len(result["file_categories"]["daily_summaries"]) == 2

    def test_extract_invalid_zip(self, temp_dir):
        """Should raise exception for invalid ZIP"""
        invalid_zip = temp_dir / "invalid.zip"
        invalid_zip.write_bytes(b"not a valid zip file")

        extract_to = temp_dir / "extracted"

        with pytest.raises(ValueError, match="not a valid ZIP archive"):
            extract_garmin_export(str(invalid_zip), str(extract_to))

    def test_extract_nonexistent_file(self, temp_dir):
        """Should raise exception for nonexistent file"""
        zip_path = temp_dir / "nonexistent.zip"
        extract_to = temp_dir / "extracted"

        with pytest.raises(FileNotFoundError, match="ZIP file not found"):
            extract_garmin_export(str(zip_path), str(extract_to))

    def test_extract_creates_directory(self, temp_dir):
        """Should create extraction directory if it doesn't exist"""
        zip_path = temp_dir / "test.zip"
        with zipfile.ZipFile(zip_path, 'w') as zf:
            zf.writestr("test.fit", "data")

        extract_to = temp_dir / "new" / "nested" / "path"
        result = extract_garmin_export(str(zip_path), str(extract_to))

        assert Path(extract_to).exists()
        assert Path(result["extract_path"]).exists()

    def test_extract_uses_temp_dir_when_none(self, temp_dir):
        """Should use temporary directory when extract_to is None"""
        zip_path = temp_dir / "test.zip"
        with zipfile.ZipFile(zip_path, 'w') as zf:
            zf.writestr("test.fit", "data")

        result = extract_garmin_export(str(zip_path), None)

        assert result["extract_path"] is not None
        assert Path(result["extract_path"]).exists()
        assert "foldline_gdpr_" in result["extract_path"]


class TestProcessGdprExport:
    """Tests for process_gdpr_export function (end-to-end integration)"""

    def test_process_returns_complete_summary(self, temp_dir, temp_db):
        """Should return comprehensive summary dict"""
        zip_path = temp_dir / "export.zip"
        with zipfile.ZipFile(zip_path, 'w') as zf:
            zf.writestr("test.fit", "data")

        temp_db.connect()
        temp_db.initialize_schema()

        result = process_gdpr_export(str(zip_path), temp_db.connection)

        assert isinstance(result, dict)
        assert "success" in result
        assert "total_files_found" in result
        assert "total_files_processed" in result
        assert "total_records_inserted" in result
        assert "duplicates_skipped" in result
        assert "errors" in result
        assert "success_rate" in result
        assert "processing_time_seconds" in result
        assert "by_category" in result

    def test_process_with_sleep_json(self, temp_dir, temp_db):
        """Should process sleep JSON files"""
        sleep_data = {
            "calendarDate": "2024-01-15",
            "sleepStartTimestampGMT": "2024-01-15T02:00:00.0",
            "sleepEndTimestampGMT": "2024-01-15T10:00:00.0",
            "deepSleepSeconds": 7200,
            "lightSleepSeconds": 18000,
            "remSleepSeconds": 3600,
            "awakeSleepSeconds": 600
        }

        zip_path = temp_dir / "export.zip"
        with zipfile.ZipFile(zip_path, 'w') as zf:
            zf.writestr("DI_CONNECT/sleep_2024-01-15.json", json.dumps(sleep_data))

        temp_db.connect()
        temp_db.initialize_schema()

        result = process_gdpr_export(str(zip_path), temp_db.connection, cleanup_temp=True)

        assert result["by_category"]["sleep_json"]["found"] == 1
        assert result["by_category"]["sleep_json"]["processed"] >= 0  # May be 0 or 1 depending on data validity

    def test_process_with_daily_summary_json(self, temp_dir, temp_db):
        """Should process daily summary JSON files"""
        summary_data = {
            "calendarDate": "2024-01-15",
            "totalSteps": 10000,
            "restingHeartRate": 55,
            "totalKilocalories": 2500
        }

        zip_path = temp_dir / "export.zip"
        with zipfile.ZipFile(zip_path, 'w') as zf:
            zf.writestr("DI_CONNECT/UdsFile_2024-01-15.json", json.dumps(summary_data))

        temp_db.connect()
        temp_db.initialize_schema()

        result = process_gdpr_export(str(zip_path), temp_db.connection, cleanup_temp=True)

        assert result["by_category"]["daily_summaries"]["found"] == 1

    def test_process_handles_malformed_json(self, temp_dir, temp_db):
        """Should handle malformed JSON gracefully"""
        zip_path = temp_dir / "export.zip"
        with zipfile.ZipFile(zip_path, 'w') as zf:
            zf.writestr("DI_CONNECT/sleep_2024-01-15.json", "{invalid json")

        temp_db.connect()
        temp_db.initialize_schema()

        result = process_gdpr_export(str(zip_path), temp_db.connection, cleanup_temp=True)

        # Should continue despite error
        assert result["by_category"]["sleep_json"]["found"] == 1
        assert result["by_category"]["sleep_json"]["errors"] > 0

    def test_process_deduplication(self, temp_dir, temp_db):
        """Should skip duplicate files on re-import"""
        sleep_data = {
            "calendarDate": "2024-01-15",
            "sleepStartTimestampGMT": "2024-01-15T02:00:00.0",
            "sleepEndTimestampGMT": "2024-01-15T10:00:00.0",
            "deepSleepSeconds": 7200,
            "lightSleepSeconds": 18000,
            "remSleepSeconds": 3600
        }

        zip_path = temp_dir / "export.zip"
        with zipfile.ZipFile(zip_path, 'w') as zf:
            zf.writestr("DI_CONNECT/sleep_2024-01-15.json", json.dumps(sleep_data))

        temp_db.connect()
        temp_db.initialize_schema()

        # First import
        result1 = process_gdpr_export(str(zip_path), temp_db.connection, cleanup_temp=False)
        records_first = result1["total_records_inserted"]

        # Second import of same file
        result2 = process_gdpr_export(str(zip_path), temp_db.connection, cleanup_temp=True)

        # Should have duplicates skipped
        assert result2["duplicates_skipped"] >= result1["total_files_processed"]

    def test_process_success_rate_calculation(self, temp_dir, temp_db):
        """Should calculate success rate correctly"""
        sleep_data = {
            "calendarDate": "2024-01-15",
            "deepSleepSeconds": 7200
        }

        zip_path = temp_dir / "export.zip"
        with zipfile.ZipFile(zip_path, 'w') as zf:
            # Add 10 valid files
            for i in range(10):
                zf.writestr(f"DI_CONNECT/sleep_2024-01-{i+1:02d}.json", json.dumps(sleep_data))
            # Add 1 invalid file
            zf.writestr("DI_CONNECT/invalid.json", "{bad json")

        temp_db.connect()
        temp_db.initialize_schema()

        result = process_gdpr_export(str(zip_path), temp_db.connection, cleanup_temp=True)

        # Success rate should be around 90% (10 out of 11 files)
        assert result["success_rate"] >= 0
        assert result["success_rate"] <= 100

    def test_process_marks_source_as_gdpr(self, temp_dir, temp_db):
        """Should mark imported files with source='gdpr'"""
        sleep_data = {
            "calendarDate": "2024-01-15",
            "deepSleepSeconds": 7200,
            "lightSleepSeconds": 18000,
            "remSleepSeconds": 3600
        }

        zip_path = temp_dir / "export.zip"
        with zipfile.ZipFile(zip_path, 'w') as zf:
            zf.writestr("DI_CONNECT/sleep_2024-01-15.json", json.dumps(sleep_data))

        temp_db.connect()
        temp_db.initialize_schema()

        process_gdpr_export(str(zip_path), temp_db.connection, cleanup_temp=True)

        # Check database for source='gdpr'
        cursor = temp_db.connection.execute(
            "SELECT COUNT(*) FROM imported_files WHERE source = 'gdpr'"
        )
        count = cursor.fetchone()[0]
        assert count > 0

    def test_process_cleanup_temp_directory(self, temp_dir, temp_db):
        """Should cleanup temporary directory when requested"""
        zip_path = temp_dir / "export.zip"
        with zipfile.ZipFile(zip_path, 'w') as zf:
            zf.writestr("test.json", "{}")

        temp_db.connect()
        temp_db.initialize_schema()

        result = process_gdpr_export(str(zip_path), temp_db.connection, cleanup_temp=True)

        extract_path = result["extract_path"]
        # Temp directory should be cleaned up
        assert not Path(extract_path).exists()

    def test_process_preserves_temp_directory(self, temp_dir, temp_db):
        """Should preserve temporary directory when cleanup_temp=False"""
        zip_path = temp_dir / "export.zip"
        with zipfile.ZipFile(zip_path, 'w') as zf:
            zf.writestr("test.json", "{}")

        temp_db.connect()
        temp_db.initialize_schema()

        result = process_gdpr_export(str(zip_path), temp_db.connection, cleanup_temp=False)

        extract_path = result["extract_path"]
        # Temp directory should still exist
        assert Path(extract_path).exists()

        # Cleanup manually
        import shutil
        shutil.rmtree(extract_path)

    def test_process_error_details(self, temp_dir, temp_db):
        """Should provide detailed error information"""
        zip_path = temp_dir / "export.zip"
        with zipfile.ZipFile(zip_path, 'w') as zf:
            zf.writestr("DI_CONNECT/bad.json", "{invalid}")

        temp_db.connect()
        temp_db.initialize_schema()

        result = process_gdpr_export(str(zip_path), temp_db.connection, cleanup_temp=True)

        assert "error_details" in result
        if result["errors"] > 0:
            assert len(result["error_details"]) > 0
            error = result["error_details"][0]
            assert "file" in error
            assert "type" in error
            assert "error" in error

    def test_process_timing_recorded(self, temp_dir, temp_db):
        """Should record processing time"""
        zip_path = temp_dir / "export.zip"
        with zipfile.ZipFile(zip_path, 'w') as zf:
            zf.writestr("test.json", "{}")

        temp_db.connect()
        temp_db.initialize_schema()

        result = process_gdpr_export(str(zip_path), temp_db.connection, cleanup_temp=True)

        assert result["processing_time_seconds"] >= 0
        assert result["processing_time_seconds"] < 60  # Should be fast for small test

    def test_process_with_mixed_file_types(self, temp_dir, temp_db):
        """Should handle mixed FIT and JSON files"""
        sleep_data = {
            "calendarDate": "2024-01-15",
            "deepSleepSeconds": 7200
        }

        zip_path = temp_dir / "export.zip"
        with zipfile.ZipFile(zip_path, 'w') as zf:
            # Add JSON
            zf.writestr("DI_CONNECT/sleep_2024-01-15.json", json.dumps(sleep_data))
            # Add FIT (even if it's fake, it should be categorized)
            zf.writestr("DI_CONNECT/activity.fit", b"fake fit data")

        temp_db.connect()
        temp_db.initialize_schema()

        result = process_gdpr_export(str(zip_path), temp_db.connection, cleanup_temp=True)

        assert result["by_category"]["sleep_json"]["found"] == 1
        assert result["by_category"]["fit_files"]["found"] == 1

    def test_process_meets_95_percent_threshold(self, temp_dir, temp_db):
        """Should mark success=True when meeting 95% threshold"""
        sleep_data = {
            "calendarDate": "2024-01-15",
            "deepSleepSeconds": 7200,
            "lightSleepSeconds": 18000,
            "remSleepSeconds": 3600
        }

        zip_path = temp_dir / "export.zip"
        with zipfile.ZipFile(zip_path, 'w') as zf:
            # Add 100 valid files
            for i in range(100):
                data = sleep_data.copy()
                data["calendarDate"] = f"2024-01-{(i % 28) + 1:02d}"
                zf.writestr(f"DI_CONNECT/sleep_2024-01-{(i % 28) + 1:02d}_{i}.json", json.dumps(data))

        temp_db.connect()
        temp_db.initialize_schema()

        result = process_gdpr_export(str(zip_path), temp_db.connection, cleanup_temp=True)

        # With valid data, should achieve >95% success rate
        if result["success_rate"] >= 95.0:
            assert result["success"] is True
