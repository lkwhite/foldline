"""
Pytest configuration and shared fixtures for Foldline tests.
"""
import os
import tempfile
from pathlib import Path
from typing import Generator

import pytest
from fastapi.testclient import TestClient

from db.connection import Database


@pytest.fixture
def temp_db() -> Generator[Database, None, None]:
    """
    Create a temporary in-memory database for testing.

    Yields:
        Database instance with schema loaded
    """
    # Use in-memory SQLite for fast tests
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test.db"
        db = Database(str(db_path))

        yield db

        # Cleanup
        db.close()


@pytest.fixture
def test_client():
    """
    Create a FastAPI test client.

    Returns:
        TestClient instance for making API requests
    """
    from main import app
    return TestClient(app)


@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """
    Create a temporary directory for file operations.

    Yields:
        Path to temporary directory
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def sample_sleep_data() -> dict:
    """
    Synthetic sleep data for testing metrics calculations.

    Returns:
        Dict with sleep record fields
    """
    return {
        "date": "2024-01-15",
        "duration_minutes": 480,  # 8 hours
        "deep_minutes": 120,
        "light_minutes": 240,
        "rem_minutes": 90,
        "awake_minutes": 30,
        "sleep_score": 85,
        "bedtime": "2024-01-14T23:00:00",
        "wake_time": "2024-01-15T07:00:00"
    }


@pytest.fixture
def sample_hrv_data() -> list[dict]:
    """
    Synthetic HRV data for testing metrics calculations.

    Returns:
        List of HRV records
    """
    return [
        {
            "date": "2024-01-15",
            "hrv_value": 55,
            "measurement_type": "morning"
        },
        {
            "date": "2024-01-16",
            "hrv_value": 58,
            "measurement_type": "morning"
        },
        {
            "date": "2024-01-17",
            "hrv_value": 52,
            "measurement_type": "morning"
        }
    ]


@pytest.fixture
def sample_stress_data() -> list[dict]:
    """
    Synthetic stress data for testing aggregation.

    Returns:
        List of stress records
    """
    return [
        {
            "timestamp": "2024-01-15T08:00:00",
            "stress_level": 25
        },
        {
            "timestamp": "2024-01-15T12:00:00",
            "stress_level": 65
        },
        {
            "timestamp": "2024-01-15T18:00:00",
            "stress_level": 45
        },
        {
            "timestamp": "2024-01-15T22:00:00",
            "stress_level": 15
        }
    ]


@pytest.fixture
def fixtures_dir() -> Path:
    """
    Get path to test fixtures directory.

    Returns:
        Path to fixtures directory
    """
    return Path(__file__).parent / "fixtures"
