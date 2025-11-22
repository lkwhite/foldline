# Development Scripts

This directory contains legacy test and debugging scripts from early development. These are preserved for reference but are not part of the main test suite.

## Scripts

- `create_sample_json.py` - Generates sample JSON data for testing
- `debug_fit_file.py` - FIT file debugging utilities
- `reset_and_test.py` - Database reset and testing helper
- `test_api_endpoint.py` - Manual API endpoint testing
- `test_fit_parsing.py` - FIT parsing validation
- `test_fixed_json.py` - JSON format testing
- `test_json_api.py` - JSON API testing
- `test_json_processing.py` - JSON processing validation
- `test_real_fit_data.py` - Real FIT file data testing
- `test_schema_tables.py` - Database schema testing

## Note

For the current test suite, see:
- `backend/tests/` - Python backend tests (pytest)
- `frontend/src/lib/*.test.ts` - Frontend tests (Vitest)
- `src-tauri/tests/` - Tauri integration tests

See `TESTING_PLAN.md` for the comprehensive testing strategy.
