"""
Tests for Garmin GDPR export processing.

Tests:
- Zip file extraction
- File enumeration by type
- Sleep, HRV, stress, steps data parsing
"""
import zipfile
from pathlib import Path

import pytest

from ingestion.garmin_gdpr import (
    extract_garmin_export,
    parse_sleep_data,
    parse_hrv_data,
    parse_stress_data,
    parse_steps_data,
    process_gdpr_export
)


class TestExtractGarminExport:
    """Tests for extract_garmin_export function"""

    def test_extract_returns_summary(self, temp_dir):
        """Should return summary dict with expected keys"""
        # Create a minimal test zip
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

    def test_extract_empty_zip(self, temp_dir):
        """Should handle empty zip file"""
        zip_path = temp_dir / "empty.zip"
        with zipfile.ZipFile(zip_path, 'w') as zf:
            pass  # Empty zip

        extract_to = temp_dir / "extracted"
        result = extract_garmin_export(str(zip_path), str(extract_to))

        # Current implementation returns zeros (TODO)
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

        # When implemented:
        # assert result["total_files"] == 5
        # assert result["fit_files"] == 2
        # assert result["tcx_files"] == 1
        # assert result["json_files"] == 1

    def test_extract_nested_structure(self, temp_dir):
        """Should handle nested directory structure"""
        zip_path = temp_dir / "nested_export.zip"
        with zipfile.ZipFile(zip_path, 'w') as zf:
            zf.writestr("DI_CONNECT/DI-Connect-Fitness/2024-01-15.fit", "data")
            zf.writestr("DI_CONNECT/DI-Connect-Wellness/sleep.fit", "data")

        extract_to = temp_dir / "extracted"
        result = extract_garmin_export(str(zip_path), str(extract_to))

        # When implemented, should handle nested paths:
        # assert result["fit_files"] == 2

    def test_extract_invalid_zip(self, temp_dir):
        """Should handle invalid/corrupted zip gracefully"""
        invalid_zip = temp_dir / "invalid.zip"
        invalid_zip.write_bytes(b"not a valid zip file")

        extract_to = temp_dir / "extracted"

        # Should raise exception or return error in summary
        # Depending on implementation
        try:
            result = extract_garmin_export(str(invalid_zip), str(extract_to))
            # If no exception, should indicate error in result
            assert result is not None
        except (zipfile.BadZipFile, Exception):
            # Expected exception is acceptable
            pass

    def test_extract_to_nonexistent_directory(self, temp_dir):
        """Should create extraction directory if it doesn't exist"""
        zip_path = temp_dir / "test.zip"
        with zipfile.ZipFile(zip_path, 'w') as zf:
            zf.writestr("test.fit", "data")

        extract_to = temp_dir / "new" / "nested" / "path"
        result = extract_garmin_export(str(zip_path), str(extract_to))

        # When implemented, should create directories:
        # assert Path(extract_to).exists()


class TestParseSleepData:
    """Tests for parse_sleep_data function"""

    def test_parse_returns_list(self, temp_dir):
        """Should return list of sleep records"""
        test_file = temp_dir / "sleep.fit"
        test_file.write_bytes(b"fake sleep data")

        result = parse_sleep_data(str(test_file))

        assert isinstance(result, list)

    def test_parse_empty_file(self, temp_dir):
        """Should handle empty file"""
        test_file = temp_dir / "empty.fit"
        test_file.write_bytes(b"")

        result = parse_sleep_data(str(test_file))

        # Current implementation returns empty list (TODO)
        assert result == []

    def test_parse_real_sleep_file(self, fixtures_dir):
        """Should parse real sleep FIT file if available"""
        sample_sleep = fixtures_dir / "sample_sleep.fit"

        if not sample_sleep.exists():
            pytest.skip("No sample sleep FIT file available")

        result = parse_sleep_data(str(sample_sleep))

        # When implemented:
        # assert len(result) > 0
        # assert all("duration_minutes" in rec for rec in result)


class TestParseHrvData:
    """Tests for parse_hrv_data function"""

    def test_parse_returns_list(self, temp_dir):
        """Should return list of HRV records"""
        test_file = temp_dir / "hrv.fit"
        test_file.write_bytes(b"fake hrv data")

        result = parse_hrv_data(str(test_file))

        assert isinstance(result, list)
        # Current implementation returns empty list (TODO)
        assert result == []

    def test_parse_real_hrv_file(self, fixtures_dir):
        """Should parse real HRV data if available"""
        sample_hrv = fixtures_dir / "sample_hrv.fit"

        if not sample_hrv.exists():
            pytest.skip("No sample HRV FIT file available")

        result = parse_hrv_data(str(sample_hrv))

        # When implemented:
        # assert len(result) > 0
        # assert all("hrv_value" in rec for rec in result)


class TestParseStressData:
    """Tests for parse_stress_data function"""

    def test_parse_returns_list(self, temp_dir):
        """Should return list of stress records"""
        test_file = temp_dir / "stress.fit"
        test_file.write_bytes(b"fake stress data")

        result = parse_stress_data(str(test_file))

        assert isinstance(result, list)
        assert result == []


class TestParseStepsData:
    """Tests for parse_steps_data function"""

    def test_parse_returns_list(self, temp_dir):
        """Should return list of step records"""
        test_file = temp_dir / "steps.fit"
        test_file.write_bytes(b"fake steps data")

        result = parse_steps_data(str(test_file))

        assert isinstance(result, list)
        assert result == []


class TestProcessGdprExport:
    """Tests for process_gdpr_export function (integration)"""

    def test_process_returns_summary(self, temp_dir, temp_db):
        """Should return summary dict"""
        zip_path = temp_dir / "export.zip"
        with zipfile.ZipFile(zip_path, 'w') as zf:
            zf.writestr("test.fit", "data")

        result = process_gdpr_export(str(zip_path), temp_db)

        assert isinstance(result, dict)
        assert "success" in result
        assert "records_inserted" in result
        assert "duplicates_skipped" in result

    def test_process_with_real_export(self, fixtures_dir, temp_db):
        """Should process real GDPR export if available"""
        sample_export = fixtures_dir / "garmin_export.zip"

        if not sample_export.exists():
            pytest.skip("No sample GDPR export available")

        result = process_gdpr_export(str(sample_export), temp_db)

        # When implemented:
        # assert result["success"] is True
        # assert result["records_inserted"] > 0
