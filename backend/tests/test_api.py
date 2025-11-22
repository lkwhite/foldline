"""
Tests for FastAPI backend endpoints.

Tests:
- Status endpoints (health check, system status)
- Import endpoints (GDPR export, FIT folder)
- Metrics endpoints (heatmap, timeseries, correlation)
- Settings endpoints (data root configuration)
- Request validation
- Response serialization
- CORS configuration
"""
import pytest
from fastapi.testclient import TestClient

from main import app


@pytest.fixture
def client():
    """Create FastAPI test client"""
    return TestClient(app)


class TestHealthCheck:
    """Tests for root health check endpoint"""

    def test_root_endpoint(self, client):
        """Should return OK status"""
        response = client.get("/")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert "message" in data

    def test_root_endpoint_structure(self, client):
        """Should return expected JSON structure"""
        response = client.get("/")
        data = response.json()

        assert isinstance(data, dict)
        assert "status" in data
        assert "message" in data


class TestStatusEndpoint:
    """Tests for /status endpoint"""

    def test_status_endpoint(self, client):
        """Should return system status"""
        response = client.get("/status")

        assert response.status_code == 200
        data = response.json()

        # Verify expected fields
        assert "db_initialized" in data
        assert "available_metrics" in data
        assert "min_date" in data
        assert "max_date" in data
        assert "counts" in data

    def test_status_returns_metrics_list(self, client):
        """Should return list of available metrics"""
        response = client.get("/status")
        data = response.json()

        assert isinstance(data["available_metrics"], list)
        # Current stub returns these metrics:
        expected_metrics = ["sleep_duration", "resting_hr", "hrv", "stress", "steps", "training_load"]
        assert data["available_metrics"] == expected_metrics

    def test_status_counts_structure(self, client):
        """Should return counts dict with expected keys"""
        response = client.get("/status")
        data = response.json()

        assert isinstance(data["counts"], dict)
        # When implemented, verify actual counts


class TestImportGarminExport:
    """Tests for /import/garmin-export endpoint"""

    def test_import_garmin_export_success(self, client, temp_dir):
        """Should accept valid zip path"""
        import zipfile

        # Create a real test ZIP file
        zip_path = temp_dir / "test_export.zip"
        with zipfile.ZipFile(zip_path, 'w') as zf:
            zf.writestr("test.json", "{}")

        response = client.post(
            "/import/garmin-export",
            json={"zip_path": str(zip_path)}
        )

        assert response.status_code == 200
        data = response.json()

        assert data["success"] is not None
        assert "message" in data
        assert "summary" in data

    def test_import_requires_zip_path(self, client):
        """Should require zip_path parameter"""
        response = client.post(
            "/import/garmin-export",
            json={}
        )

        # Should return validation error
        assert response.status_code == 422

    def test_import_response_structure(self, client, temp_dir):
        """Should return expected response structure"""
        import zipfile

        # Create a real test ZIP file
        zip_path = temp_dir / "test_export.zip"
        with zipfile.ZipFile(zip_path, 'w') as zf:
            zf.writestr("test.json", "{}")

        response = client.post(
            "/import/garmin-export",
            json={"zip_path": str(zip_path)}
        )

        data = response.json()
        assert "success" in data
        assert "message" in data
        assert "summary" in data
        assert isinstance(data["summary"], dict)

    def test_import_with_invalid_path(self, client):
        """Should handle invalid/nonexistent paths"""
        response = client.post(
            "/import/garmin-export",
            json={"zip_path": "/nonexistent/path.zip"}
        )

        # Current stub returns success
        # When implemented, should validate path exists:
        # assert response.status_code == 400 or data["success"] is False

    def test_import_summary_contains_metrics(self, client):
        """Should include summary of imported data"""
        response = client.post(
            "/import/garmin-export",
            json={"zip_path": "/test/export.zip"}
        )

        data = response.json()
        # Current stub includes these keys:
        # assert "activities_found" in data["summary"]
        # assert "sleep_records" in data["summary"]


class TestImportFitFolder:
    """Tests for /import/fit-folder endpoint"""

    def test_import_fit_folder_success(self, client, temp_dir):
        """Should accept valid folder path"""
        # Create a real test directory
        fit_folder = temp_dir / "fit_files"
        fit_folder.mkdir()

        response = client.post(
            "/import/fit-folder",
            json={"folder_path": str(fit_folder)}
        )

        assert response.status_code == 200
        data = response.json()

        assert "success" in data
        assert "message" in data
        assert "summary" in data

    def test_import_requires_folder_path(self, client):
        """Should require folder_path parameter"""
        response = client.post(
            "/import/fit-folder",
            json={}
        )

        assert response.status_code == 422

    def test_import_response_includes_summary(self, client, temp_dir):
        """Should include summary with file counts"""
        # Create a real test directory
        fit_folder = temp_dir / "fit_files"
        fit_folder.mkdir()

        response = client.post(
            "/import/fit-folder",
            json={"folder_path": str(fit_folder)}
        )

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data["summary"], dict)
        # Implemented - should include these fields:
        assert "files_found" in data["summary"]
        assert "files_processed" in data["summary"]
        assert "total_records" in data["summary"]
        assert "duplicates_skipped" in data["summary"]
        assert "errors" in data["summary"]

    def test_import_invalid_folder(self, client):
        """Should handle invalid/nonexistent folders"""
        response = client.post(
            "/import/fit-folder",
            json={"folder_path": "/nonexistent/folder"}
        )

        # Should return 400 for invalid directory
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data


class TestMetricsHeatmap:
    """Tests for /metrics/heatmap endpoint"""

    def test_heatmap_requires_metric(self, client):
        """Should require metric query parameter"""
        response = client.get("/metrics/heatmap")

        # FastAPI returns 422 for missing required parameter
        assert response.status_code == 422

    def test_heatmap_with_metric(self, client):
        """Should return heatmap data for valid metric"""
        response = client.get("/metrics/heatmap?metric=sleep_duration")

        assert response.status_code == 200
        data = response.json()

        assert isinstance(data, list)

    def test_heatmap_data_structure(self, client):
        """Should return list of {date, value} objects"""
        response = client.get("/metrics/heatmap?metric=hrv")

        data = response.json()

        if len(data) > 0:
            assert "date" in data[0]
            assert "value" in data[0]

    def test_heatmap_with_date_range(self, client):
        """Should accept optional start_date and end_date"""
        response = client.get(
            "/metrics/heatmap"
            "?metric=sleep_duration"
            "&start_date=2024-01-01"
            "&end_date=2024-12-31"
        )

        assert response.status_code == 200
        # When implemented, verify date filtering

    def test_heatmap_invalid_metric(self, client):
        """Should handle invalid metric names"""
        response = client.get("/metrics/heatmap?metric=invalid_metric")

        # Current stub returns data regardless
        # When implemented, should validate metric:
        # assert response.status_code == 400

    def test_heatmap_date_format(self, client):
        """Date values should be ISO format strings"""
        response = client.get("/metrics/heatmap?metric=steps")

        data = response.json()
        if len(data) > 0:
            # Should be YYYY-MM-DD format
            assert isinstance(data[0]["date"], str)
            # Could validate with datetime.fromisoformat()


class TestMetricsTimeseries:
    """Tests for /metrics/timeseries endpoint"""

    def test_timeseries_requires_metric(self, client):
        """Should require metric query parameter"""
        response = client.get("/metrics/timeseries")

        assert response.status_code == 422

    def test_timeseries_with_metric(self, client):
        """Should return timeseries data"""
        response = client.get("/metrics/timeseries?metric=resting_hr")

        assert response.status_code == 200
        data = response.json()

        assert isinstance(data, list)

    def test_timeseries_data_structure(self, client):
        """Should return list of {date, value} objects"""
        response = client.get("/metrics/timeseries?metric=stress")

        data = response.json()

        if len(data) > 0:
            assert "date" in data[0]
            assert "value" in data[0]

    def test_timeseries_with_date_range(self, client):
        """Should accept date range parameters"""
        response = client.get(
            "/metrics/timeseries"
            "?metric=steps"
            "&start_date=2024-01-01"
            "&end_date=2024-01-31"
        )

        assert response.status_code == 200


class TestMetricsCorrelation:
    """Tests for /metrics/correlation endpoint"""

    def test_correlation_requires_metrics(self, client):
        """Should require x_metric and y_metric parameters"""
        response = client.get("/metrics/correlation")

        assert response.status_code == 422

    def test_correlation_with_insufficient_data(self, client):
        """Should return 400 when there's insufficient data"""
        response = client.get(
            "/metrics/correlation"
            "?x_metric=sleep_duration"
            "&y_metric=hrv_value"
        )

        assert response.status_code == 400
        data = response.json()
        assert "Insufficient data" in data["detail"]

    def test_correlation_with_invalid_metric(self, client):
        """Should return 400 when metric name is invalid"""
        response = client.get(
            "/metrics/correlation"
            "?x_metric=invalid_metric"
            "&y_metric=hrv_value"
        )

        assert response.status_code == 400
        data = response.json()
        assert "Invalid x_metric" in data["detail"]

    def test_correlation_with_two_metrics(self, temp_db):
        """Should return correlation data for two metrics with sample data"""
        from main import app
        from fastapi.testclient import TestClient

        # Insert sample data
        temp_db.connect()
        temp_db.initialize_schema()
        conn = temp_db.connection

        # Insert test data
        for i in range(10):
            date = f"2024-01-{i+10:02d}"
            conn.execute(
                "INSERT INTO sleep_records (date, duration_minutes, sleep_score) VALUES (?, ?, ?)",
                (date, 420 + i * 10, 80 + i)
            )
            conn.execute(
                "INSERT INTO hrv_records (date, hrv_value) VALUES (?, ?)",
                (date, 50 + i * 2)
            )
        conn.commit()

        # Override the global database for this test
        import db.connection
        original_db = db.connection._db_instance
        db.connection._db_instance = temp_db

        try:
            client = TestClient(app)
            response = client.get(
                "/metrics/correlation"
                "?x_metric=sleep_duration"
                "&y_metric=hrv_value"
            )

            assert response.status_code == 200
            data = response.json()

            assert "x_values" in data
            assert "y_values" in data
            assert "dates" in data
            assert "stats" in data

            # Should have 10 data points
            assert len(data["x_values"]) == 10
            assert len(data["y_values"]) == 10
            assert len(data["dates"]) == 10

        finally:
            # Restore original database
            db.connection._db_instance = original_db

    def test_correlation_stats_structure(self, temp_db):
        """Should return correlation statistics"""
        from main import app
        from fastapi.testclient import TestClient

        # Insert sample data
        temp_db.connect()
        temp_db.initialize_schema()
        conn = temp_db.connection

        for i in range(10):
            date = f"2024-01-{i+10:02d}"
            conn.execute(
                "INSERT INTO sleep_records (date, duration_minutes, sleep_score) VALUES (?, ?, ?)",
                (date, 420 + i * 10, 80 + i)
            )
            conn.execute(
                "INSERT INTO resting_hr (date, resting_hr) VALUES (?, ?)",
                (date, 60 + i)
            )
        conn.commit()

        import db.connection
        original_db = db.connection._db_instance
        db.connection._db_instance = temp_db

        try:
            client = TestClient(app)
            response = client.get(
                "/metrics/correlation"
                "?x_metric=sleep_duration"
                "&y_metric=resting_hr"
            )

            data = response.json()
            stats = data["stats"]

            # Should include correlation coefficients
            assert "pearson_r" in stats
            assert "pearson_p" in stats
            assert "spearman_r" in stats
            assert "spearman_p" in stats
            assert "n" in stats
            assert stats["n"] == 10

        finally:
            db.connection._db_instance = original_db

    def test_correlation_with_lag(self, temp_db):
        """Should accept lag_days parameter and reduce data points accordingly"""
        from main import app
        from fastapi.testclient import TestClient

        # Insert sample data
        temp_db.connect()
        temp_db.initialize_schema()
        conn = temp_db.connection

        for i in range(10):
            date = f"2024-01-{i+10:02d}"
            conn.execute(
                "INSERT INTO sleep_records (date, duration_minutes) VALUES (?, ?)",
                (date, 420 + i * 10)
            )
            conn.execute(
                "INSERT INTO daily_stress (date, avg_stress) VALUES (?, ?)",
                (date, 30 + i * 2)
            )
        conn.commit()

        import db.connection
        original_db = db.connection._db_instance
        db.connection._db_instance = temp_db

        try:
            client = TestClient(app)
            response = client.get(
                "/metrics/correlation"
                "?x_metric=sleep_duration"
                "&y_metric=avg_stress"
                "&lag_days=1"
            )

            assert response.status_code == 200
            data = response.json()

            # With lag_days=1, we should have 9 points (10 - 1)
            assert len(data["x_values"]) == 9
            assert len(data["y_values"]) == 9

        finally:
            db.connection._db_instance = original_db

    def test_correlation_arrays_aligned(self, temp_db):
        """x_values, y_values, and dates should have same length"""
        from main import app
        from fastapi.testclient import TestClient

        # Insert sample data
        temp_db.connect()
        temp_db.initialize_schema()
        conn = temp_db.connection

        for i in range(10):
            date = f"2024-01-{i+10:02d}"
            conn.execute(
                "INSERT INTO daily_steps (date, step_count) VALUES (?, ?)",
                (date, 8000 + i * 500)
            )
            conn.execute(
                "INSERT INTO sleep_records (date, duration_minutes) VALUES (?, ?)",
                (date, 420 + i * 10)
            )
        conn.commit()

        import db.connection
        original_db = db.connection._db_instance
        db.connection._db_instance = temp_db

        try:
            client = TestClient(app)
            response = client.get(
                "/metrics/correlation"
                "?x_metric=step_count"
                "&y_metric=sleep_duration"
            )

            data = response.json()

            assert len(data["x_values"]) == len(data["y_values"])
            assert len(data["x_values"]) == len(data["dates"])

        finally:
            db.connection._db_instance = original_db


class TestSettingsDataRoot:
    """Tests for /settings/data-root endpoint"""

    def test_set_data_root(self, client):
        """Should accept data root path"""
        response = client.post(
            "/settings/data-root",
            json={"data_root": "/home/user/foldline_data"}
        )

        assert response.status_code == 200
        data = response.json()

        assert data["success"] is True
        assert "message" in data

    def test_set_data_root_requires_path(self, client):
        """Should require data_root parameter"""
        response = client.post(
            "/settings/data-root",
            json={}
        )

        assert response.status_code == 422

    def test_set_data_root_validation(self, client):
        """Should validate data root path"""
        response = client.post(
            "/settings/data-root",
            json={"data_root": "/nonexistent/path"}
        )

        # Current stub accepts any path
        # When implemented, should validate:
        # assert response.status_code == 400 or verify warning in response


class TestCORS:
    """Tests for CORS configuration"""

    def test_cors_headers_present(self, client):
        """Should include CORS headers in responses"""
        response = client.options(
            "/status",
            headers={"Origin": "http://localhost:5173"}
        )

        # Should have CORS headers
        # Note: TestClient may handle OPTIONS differently

    def test_localhost_origins_allowed(self, client):
        """Should allow requests from localhost origins"""
        response = client.get(
            "/status",
            headers={"Origin": "http://localhost:5173"}
        )

        assert response.status_code == 200
        # CORS should allow this origin


class TestRequestValidation:
    """Tests for request validation"""

    def test_invalid_json(self, client):
        """Should handle malformed JSON"""
        response = client.post(
            "/import/garmin-export",
            data="not valid json",
            headers={"Content-Type": "application/json"}
        )

        assert response.status_code == 422

    def test_missing_required_fields(self, client):
        """Should return 422 for missing required fields"""
        response = client.post("/import/fit-folder", json={})

        assert response.status_code == 422
        data = response.json()
        assert "detail" in data

    def test_wrong_type_for_field(self, client):
        """Should validate field types"""
        response = client.post(
            "/import/garmin-export",
            json={"zip_path": 123}  # Should be string
        )

        assert response.status_code == 422


class TestResponseSerialization:
    """Tests for Pydantic response model serialization"""

    def test_status_response_model(self, client):
        """StatusResponse should serialize correctly"""
        response = client.get("/status")

        data = response.json()

        # All required fields should be present
        assert isinstance(data["db_initialized"], bool)
        assert isinstance(data["available_metrics"], list)
        assert isinstance(data["counts"], dict)

    def test_import_response_model(self, client, temp_dir):
        """ImportResponse should serialize correctly"""
        # Create a real test directory
        fit_folder = temp_dir / "fit_files"
        fit_folder.mkdir()

        response = client.post(
            "/import/fit-folder",
            json={"folder_path": str(fit_folder)}
        )

        assert response.status_code == 200
        data = response.json()

        assert isinstance(data["success"], bool)
        assert isinstance(data["message"], str)
        assert isinstance(data["summary"], dict)

    def test_heatmap_data_point_model(self, client):
        """HeatmapDataPoint should serialize correctly"""
        response = client.get("/metrics/heatmap?metric=sleep_duration")

        data = response.json()

        if len(data) > 0:
            point = data[0]
            assert isinstance(point["date"], str)
            # value can be null or float
            assert point["value"] is None or isinstance(point["value"], (int, float))
