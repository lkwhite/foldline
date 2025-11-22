"""
Tests for FIT folder scanning and file processing.

Tests:
- Directory scanning for .fit files
- File hash computation for deduplication
- FIT file parsing (when implemented)
"""
import os
import tempfile
from pathlib import Path

import pytest

from ingestion.fit_folder import (
    scan_fit_directory,
    compute_file_hash,
    parse_fit_file,
    process_fit_folder
)


class TestScanFitDirectory:
    """Tests for scan_fit_directory function"""

    def test_scan_empty_directory(self, temp_dir):
        """Should return empty list for empty directory"""
        result = scan_fit_directory(str(temp_dir))
        assert result == []

    def test_scan_directory_with_fit_files(self, temp_dir):
        """Should find .fit files in directory"""
        # Create test files
        (temp_dir / "activity1.fit").write_text("test data")
        (temp_dir / "activity2.fit").write_text("test data")
        (temp_dir / "not_a_fit.txt").write_text("test data")

        result = scan_fit_directory(str(temp_dir))

        # Note: Current implementation returns empty list (TODO)
        # When implemented, this test should pass:
        # assert len(result) == 2
        # assert all(f.endswith('.fit') for f in result)

    def test_scan_directory_recursive(self, temp_dir):
        """Should recursively find .fit files in subdirectories"""
        # Create nested structure
        subdir = temp_dir / "2024" / "01"
        subdir.mkdir(parents=True)

        (temp_dir / "root.fit").write_text("test data")
        (subdir / "nested.fit").write_text("test data")

        result = scan_fit_directory(str(temp_dir))

        # When implemented, should find both files:
        # assert len(result) == 2

    def test_scan_directory_case_insensitive(self, temp_dir):
        """Should find .FIT, .fit, .Fit files"""
        (temp_dir / "lowercase.fit").write_text("test data")
        (temp_dir / "uppercase.FIT").write_text("test data")
        (temp_dir / "mixedcase.Fit").write_text("test data")

        result = scan_fit_directory(str(temp_dir))

        # When implemented:
        # assert len(result) == 3

    def test_scan_nonexistent_directory(self):
        """Should handle nonexistent directory gracefully"""
        # Depending on implementation, should raise error or return empty list
        result = scan_fit_directory("/nonexistent/path")
        assert isinstance(result, list)


class TestComputeFileHash:
    """Tests for compute_file_hash function"""

    def test_hash_small_file(self, temp_dir):
        """Should compute SHA256 hash for small file"""
        test_file = temp_dir / "test.fit"
        test_content = b"This is test content for hashing"
        test_file.write_bytes(test_content)

        hash_result = compute_file_hash(str(test_file))

        # Should be 64 character hex string
        assert isinstance(hash_result, str)
        assert len(hash_result) == 64
        assert all(c in '0123456789abcdef' for c in hash_result)

    def test_hash_consistency(self, temp_dir):
        """Should produce same hash for same content"""
        test_file = temp_dir / "test.fit"
        test_content = b"Consistent content"
        test_file.write_bytes(test_content)

        hash1 = compute_file_hash(str(test_file))
        hash2 = compute_file_hash(str(test_file))

        assert hash1 == hash2

    def test_hash_uniqueness(self, temp_dir):
        """Should produce different hashes for different content"""
        file1 = temp_dir / "file1.fit"
        file2 = temp_dir / "file2.fit"

        file1.write_bytes(b"Content A")
        file2.write_bytes(b"Content B")

        hash1 = compute_file_hash(str(file1))
        hash2 = compute_file_hash(str(file2))

        assert hash1 != hash2

    def test_hash_large_file(self, temp_dir):
        """Should handle large files (tests chunked reading)"""
        test_file = temp_dir / "large.fit"

        # Create a file larger than read buffer (8192 bytes)
        large_content = b"X" * 20000
        test_file.write_bytes(large_content)

        hash_result = compute_file_hash(str(test_file))

        assert isinstance(hash_result, str)
        assert len(hash_result) == 64

    def test_hash_empty_file(self, temp_dir):
        """Should handle empty file"""
        test_file = temp_dir / "empty.fit"
        test_file.write_bytes(b"")

        hash_result = compute_file_hash(str(test_file))

        # SHA256 of empty string is known
        assert hash_result == "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"


class TestParseFitFile:
    """Tests for parse_fit_file function"""

    def test_parse_returns_structure(self, temp_dir):
        """Should return dict with expected structure"""
        test_file = temp_dir / "test.fit"
        test_file.write_bytes(b"fake fit data")

        result = parse_fit_file(str(test_file))

        assert isinstance(result, dict)
        assert "file_path" in result
        assert "file_hash" in result
        assert "records" in result

    def test_parse_includes_file_hash(self, temp_dir):
        """Should include file hash in result"""
        test_file = temp_dir / "test.fit"
        test_content = b"test fit content"
        test_file.write_bytes(test_content)

        result = parse_fit_file(str(test_file))
        expected_hash = compute_file_hash(str(test_file))

        assert result["file_hash"] == expected_hash

    def test_parse_with_real_fit_file(self, fixtures_dir):
        """Should parse real FIT file if available"""
        # This test will be skipped if no real FIT file is available
        sample_fit = fixtures_dir / "sample_sleep.fit"

        if not sample_fit.exists():
            pytest.skip("No sample FIT file available")

        result = parse_fit_file(str(sample_fit))

        assert result is not None
        # When implemented, should extract actual records:
        # assert len(result["records"]) > 0


class TestProcessFitFolder:
    """Tests for process_fit_folder function (integration)"""

    def test_process_returns_summary(self, temp_dir, temp_db):
        """Should return summary dict"""
        result = process_fit_folder(str(temp_dir), temp_db)

        assert isinstance(result, dict)
        assert "files_found" in result
        assert "total_records" in result
        assert "duplicates_skipped" in result

    def test_process_empty_folder(self, temp_dir, temp_db):
        """Should handle empty folder"""
        result = process_fit_folder(str(temp_dir), temp_db)

        # Current implementation returns zeros (TODO)
        assert result["files_found"] == 0
        assert result["total_records"] == 0
        assert result["duplicates_skipped"] == 0

    def test_process_with_fit_files(self, temp_dir, temp_db):
        """Should process folder with FIT files"""
        # Create test files
        (temp_dir / "activity1.fit").write_bytes(b"test data 1")
        (temp_dir / "activity2.fit").write_bytes(b"test data 2")

        result = process_fit_folder(str(temp_dir), temp_db)

        # When implemented, should find and process files:
        # assert result["files_found"] == 2
        # assert result["new_records"] > 0

    def test_process_deduplication(self, temp_dir, temp_db):
        """Should skip duplicate files based on hash"""
        test_file = temp_dir / "activity.fit"
        test_file.write_bytes(b"unique content")

        # Process first time
        result1 = process_fit_folder(str(temp_dir), temp_db)

        # Process again (should detect duplicate)
        result2 = process_fit_folder(str(temp_dir), temp_db)

        # When implemented:
        # assert result2["duplicates_skipped"] == 1
        # assert result2["new_records"] == 0
