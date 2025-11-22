#!/usr/bin/env python3
"""
Test script for the FIT folder API endpoint
"""

import requests
import json
import tempfile
import shutil
import os
import sys
from pathlib import Path

def create_test_fit_directory():
    """Create a temporary directory with sample FIT files"""
    test_dir = tempfile.mkdtemp(prefix="foldline_test_")

    # Copy our test FIT files to the test directory
    fit_files = [
        "/tmp/laura.white@gmail.com_108471997439.fit",
        "/tmp/laura.white@gmail.com_53902275619.fit"
    ]

    for fit_file in fit_files:
        if os.path.exists(fit_file):
            dest_file = os.path.join(test_dir, os.path.basename(fit_file))
            shutil.copy2(fit_file, dest_file)
            print(f"Copied {fit_file} to {dest_file}")

    return test_dir

def test_fit_folder_api():
    """Test the /import/fit-folder API endpoint"""

    # Create test directory with FIT files
    test_dir = create_test_fit_directory()

    try:
        # Make API request
        api_url = "http://127.0.0.1:8000/import/fit-folder"
        payload = {
            "folder_path": test_dir
        }

        print(f"Testing API endpoint: {api_url}")
        print(f"Request payload: {payload}")

        response = requests.post(api_url, json=payload, timeout=30)

        print(f"Response status: {response.status_code}")
        print(f"Response headers: {dict(response.headers)}")

        if response.status_code == 200:
            result = response.json()
            print(f"✅ API request successful!")
            print(f"Response: {json.dumps(result, indent=2)}")
            return True
        else:
            print(f"❌ API request failed")
            print(f"Response: {response.text}")
            return False

    except requests.exceptions.ConnectionError:
        print(f"❌ Could not connect to API server at {api_url}")
        print("Make sure the backend server is running: python backend/main.py")
        return False
    except Exception as e:
        print(f"❌ Error testing API: {e}")
        return False
    finally:
        # Clean up test directory
        shutil.rmtree(test_dir)
        print(f"Cleaned up test directory: {test_dir}")

if __name__ == "__main__":
    success = test_fit_folder_api()
    sys.exit(0 if success else 1)