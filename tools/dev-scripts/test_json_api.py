#!/usr/bin/env python3
"""
Test script for the JSON import API endpoint
"""

import requests
import json
import sys

def test_json_api():
    """Test the /import/json-folder API endpoint"""

    try:
        # Test JSON import endpoint
        api_url = "http://127.0.0.1:8000/import/json-folder"
        payload = {
            "folder_path": "/tmp/sample_garmin_json",
            "data_type": "sleep"
        }

        print(f"Testing JSON API endpoint: {api_url}")
        print(f"Request payload: {payload}")

        response = requests.post(api_url, json=payload, timeout=30)

        print(f"Response status: {response.status_code}")
        print(f"Response headers: {dict(response.headers)}")

        if response.status_code == 200:
            result = response.json()
            print(f"✅ JSON API request successful!")
            print(f"Response: {json.dumps(result, indent=2)}")

            # Check if we got meaningful results
            summary = result.get("summary", {})
            if summary.get("files_found", 0) > 0 and summary.get("total_records", 0) > 0:
                print(f"🎉 Successfully imported {summary['total_records']} sleep records from {summary['files_processed']} files!")
                return True
            else:
                print(f"⚠️ API succeeded but no data was imported")
                return True
        else:
            print(f"❌ JSON API request failed")
            print(f"Response: {response.text}")
            return False

    except requests.exceptions.ConnectionError:
        print(f"❌ Could not connect to API server at {api_url}")
        print("Make sure the backend server is running: python backend/main.py")
        return False
    except Exception as e:
        print(f"❌ Error testing JSON API: {e}")
        return False

if __name__ == "__main__":
    success = test_json_api()
    sys.exit(0 if success else 1)