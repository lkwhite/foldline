"""
Foldline Backend - Local-only FastAPI server for wearable data analysis

This backend runs entirely on localhost and never makes external API calls.
It processes:
  - Garmin GDPR export zips
  - Local FIT file directories

All data stays on the user's machine.
"""

import argparse
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import date, datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Foldline Backend",
    description="Local-only wearable data analyzer",
    version="0.1.0"
)

# CORS middleware - only allow localhost origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite dev server
        "http://localhost:1420",  # Tauri dev
        "http://127.0.0.1:5173",
        "http://127.0.0.1:1420",
        "tauri://localhost",  # Tauri production
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================================
# Request/Response Models
# ============================================================================

class GarminExportRequest(BaseModel):
    """Request to import a Garmin GDPR export zip"""
    zip_path: str


class FitFolderRequest(BaseModel):
    """Request to import a FIT file folder"""
    folder_path: str


class JsonFolderRequest(BaseModel):
    """Request to import JSON files from GDPR export"""
    folder_path: str
    data_type: str = "sleep"  # "sleep", "daily_summaries", "all"


class DataRootRequest(BaseModel):
    """Request to set the data root directory"""
    data_root: str


class StatusResponse(BaseModel):
    """System status response"""
    db_initialized: bool
    available_metrics: List[str]
    min_date: Optional[str]
    max_date: Optional[str]
    counts: Dict[str, int]


class ImportResponse(BaseModel):
    """Response from import operations"""
    success: bool
    message: str
    summary: Dict[str, Any]


class HeatmapDataPoint(BaseModel):
    """Single data point for heatmap"""
    date: str
    value: Optional[float]


class TimeSeriesDataPoint(BaseModel):
    """Single data point for time series"""
    date: str
    value: Optional[float]


class CorrelationResponse(BaseModel):
    """Correlation analysis response"""
    x_values: List[float]
    y_values: List[float]
    dates: List[str]
    stats: Dict[str, Any]


# ============================================================================
# Status Endpoints
# ============================================================================

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"status": "ok", "message": "Foldline backend is running"}


@app.get("/status", response_model=StatusResponse)
async def get_status():
    """
    Get the current status of the backend and database

    TODO: Replace with actual DB queries
    """
    # Stub response - replace with actual DB checks
    return StatusResponse(
        db_initialized=True,  # TODO: Check if DB exists and has schema
        available_metrics=[
            "sleep_duration",
            "resting_hr",
            "hrv",
            "stress",
            "steps",
            "training_load"
        ],
        min_date="2020-01-01",  # TODO: Query actual min date from DB
        max_date="2025-01-01",  # TODO: Query actual max date from DB
        counts={
            "nights": 1825,  # TODO: Count sleep records
            "activities": 542,  # TODO: Count activity records
            "days_with_data": 1800,  # TODO: Count distinct dates with any data
        }
    )


# ============================================================================
# Import Endpoints
# ============================================================================

@app.post("/import/garmin-export", response_model=ImportResponse)
async def import_garmin_export(request: GarminExportRequest):
    """
    Import a Garmin GDPR export zip file

    Steps:
    1. Validate zip file exists
    2. Extract to internal data directory
    3. Locate FIT/TCX/JSON files
    4. Parse relevant metrics (sleep, HR, HRV, stress, steps, training load)
    5. Store in DB with deduplication
    6. Return summary

    This implements the complete GDPR import pipeline per PRE_COMMERCIAL_MVP_PLAN.md Week 1
    """
    logger.info(f"Importing Garmin export from: {request.zip_path}")

    import os
    from db.connection import get_db
    from ingestion.garmin_gdpr import process_gdpr_export

    # Validate file exists
    if not os.path.exists(request.zip_path):
        raise HTTPException(status_code=400, detail=f"ZIP file not found: {request.zip_path}")

    if not request.zip_path.lower().endswith('.zip'):
        raise HTTPException(status_code=400, detail=f"File must be a ZIP archive: {request.zip_path}")

    try:
        # Get database connection
        db = get_db()

        # Process the GDPR export using the full pipeline
        summary = process_gdpr_export(
            zip_path=request.zip_path,
            db_connection=db.connection,
            progress_callback=None,  # TODO: Add WebSocket support for real-time progress
            cleanup_temp=True
        )

        # Build success message
        if summary["success"]:
            message = f"GDPR export imported successfully! "
            message += f"Processed {summary['total_files_processed']} files, "
            message += f"inserted {summary['total_records_inserted']} records "
            message += f"({summary['success_rate']}% success rate)"

            if summary["duplicates_skipped"] > 0:
                message += f", skipped {summary['duplicates_skipped']} duplicates"

            if summary["errors"] > 0:
                message += f". Warning: {summary['errors']} errors occurred"
        else:
            message = f"GDPR export import completed with errors. "
            message += f"Processed {summary['total_files_processed']}/{summary['total_files_found']} files, "
            message += f"inserted {summary['total_records_inserted']} records. "
            message += f"{summary['errors']} errors occurred."

        return ImportResponse(
            success=summary["success"],
            message=message,
            summary={
                "zip_path": summary["zip_path"],
                "total_files_found": summary["total_files_found"],
                "total_files_processed": summary["total_files_processed"],
                "total_records_inserted": summary["total_records_inserted"],
                "duplicates_skipped": summary["duplicates_skipped"],
                "errors": summary["errors"],
                "success_rate": summary["success_rate"],
                "processing_time_seconds": summary["processing_time_seconds"],
                "by_category": summary["by_category"],
                "error_details": summary["error_details"][:10] if summary["error_details"] else []  # Limit to first 10 errors
            }
        )

    except Exception as e:
        logger.error(f"Failed to import GDPR export {request.zip_path}: {e}")
        raise HTTPException(status_code=500, detail=f"Import failed: {str(e)}")


@app.post("/import/fit-folder", response_model=ImportResponse)
async def import_fit_folder(request: FitFolderRequest):
    """
    Import FIT files from a local directory (e.g., Garmin Express folder)

    Steps:
    1. Validate folder exists
    2. Recursively walk directory tree
    3. Parse all .fit files
    4. Deduplicate based on file hash or activity ID
    5. Insert new records into DB
    6. Return summary
    """
    logger.info(f"Importing FIT folder from: {request.folder_path}")

    import os
    from db.connection import get_db
    from ingestion.fit_folder import process_fit_folder

    # Validate directory exists
    if not os.path.exists(request.folder_path):
        raise HTTPException(status_code=400, detail=f"Directory not found: {request.folder_path}")

    if not os.path.isdir(request.folder_path):
        raise HTTPException(status_code=400, detail=f"Path is not a directory: {request.folder_path}")

    try:
        # Get database connection
        db = get_db()

        # Process the FIT folder using our implementation
        summary = process_fit_folder(request.folder_path, db.connection)

        # Build success message
        message = f"Processed {summary['files_found']} FIT files"
        if summary['files_processed'] > 0:
            message += f", inserted {summary['total_records']} records"
        if summary['duplicates_skipped'] > 0:
            message += f", skipped {summary['duplicates_skipped']} duplicates"
        if summary['errors'] > 0:
            message += f", {summary['errors']} errors"

        return ImportResponse(
            success=summary['errors'] == 0,
            message=message,
            summary={
                "files_found": summary['files_found'],
                "files_processed": summary['files_processed'],
                "total_records": summary['total_records'],
                "duplicates_skipped": summary['duplicates_skipped'],
                "errors": summary['errors'],
                "error_files": summary.get('error_files', [])
            }
        )

    except Exception as e:
        logger.error(f"Failed to import FIT folder {request.folder_path}: {e}")
        raise HTTPException(status_code=500, detail=f"Import failed: {str(e)}")


@app.post("/import/json-folder", response_model=ImportResponse)
async def import_json_folder(request: JsonFolderRequest):
    """
    Import JSON files from Garmin GDPR export

    Steps:
    1. Validate folder exists
    2. Scan for JSON files by type (sleep, daily summaries, etc.)
    3. Parse and extract health metrics
    4. Deduplicate and insert into appropriate tables
    5. Return summary

    Supported data_type values:
    - "sleep": Process sleep_*.json files
    - "daily_summaries": Process UdsFile_*.json files
    - "all": Process all supported JSON types
    """
    logger.info(f"Importing JSON {request.data_type} files from: {request.folder_path}")

    try:
        import os
        from db.connection import get_db
        from ingestion.json_parser import process_sleep_json_files

        # Validate directory exists
        if not os.path.exists(request.folder_path):
            raise HTTPException(status_code=400, detail=f"Directory not found: {request.folder_path}")

        if not os.path.isdir(request.folder_path):
            raise HTTPException(status_code=400, detail=f"Path is not a directory: {request.folder_path}")

        # Get database connection
        db = get_db()

        summary = {"files_found": 0, "files_processed": 0, "total_records": 0,
                  "duplicates_skipped": 0, "errors": 0, "error_files": []}

        # Process based on data type
        if request.data_type == "sleep" or request.data_type == "all":
            sleep_summary = process_sleep_json_files(request.folder_path, db.connection)

            # Aggregate sleep results
            summary["files_found"] += sleep_summary["files_found"]
            summary["files_processed"] += sleep_summary["files_processed"]
            summary["total_records"] += sleep_summary["total_records"]
            summary["duplicates_skipped"] += sleep_summary["duplicates_skipped"]
            summary["errors"] += sleep_summary["errors"]
            summary["error_files"].extend(sleep_summary.get("error_files", []))

        # TODO: Add daily_summaries processing when request.data_type includes it
        # if request.data_type == "daily_summaries" or request.data_type == "all":
        #     daily_summary = process_daily_summary_json_files(request.folder_path, db.connection)
        #     # Aggregate results...

        # Build success message
        message = f"Processed {summary['files_found']} JSON files"
        if summary['files_processed'] > 0:
            message += f", imported {summary['total_records']} records"
        if summary['duplicates_skipped'] > 0:
            message += f", skipped {summary['duplicates_skipped']} duplicates"
        if summary['errors'] > 0:
            message += f", {summary['errors']} errors"

        return ImportResponse(
            success=summary['errors'] == 0,
            message=message,
            summary={
                "data_type": request.data_type,
                "files_found": summary['files_found'],
                "files_processed": summary['files_processed'],
                "total_records": summary['total_records'],
                "duplicates_skipped": summary['duplicates_skipped'],
                "errors": summary['errors'],
                "error_files": summary.get('error_files', [])
            }
        )

    except Exception as e:
        logger.error(f"Failed to import JSON folder {request.folder_path}: {e}")
        raise HTTPException(status_code=500, detail=f"JSON import failed: {str(e)}")


# ============================================================================
# Metrics Endpoints
# ============================================================================

@app.get("/metrics/heatmap")
async def get_heatmap_data(
    metric: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
) -> List[HeatmapDataPoint]:
    """
    Get heatmap data for a specific metric

    Returns a list of {date, value} that can be binned into a year × day heatmap

    TODO: Implement actual DB queries for each metric type
    """
    logger.info(f"Fetching heatmap data for metric: {metric}")

    # TODO: Validate metric is supported
    # TODO: Query DB for metric between start_date and end_date
    # TODO: Return array of {date, value}

    # Stub response - generate some fake data
    stub_data = []
    for i in range(100):
        stub_data.append(HeatmapDataPoint(
            date=f"2024-{(i % 12) + 1:02d}-{(i % 28) + 1:02d}",
            value=float(i % 10)
        ))

    return stub_data


@app.get("/metrics/timeseries")
async def get_timeseries_data(
    metric: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
) -> List[TimeSeriesDataPoint]:
    """
    Get time series data for plotting

    Returns a simple array of {date, value} for line charts

    TODO: Implement actual DB queries and optional smoothing
    """
    logger.info(f"Fetching timeseries data for metric: {metric}")

    # TODO: Query DB for metric
    # TODO: Optional: apply smoothing (rolling mean)

    # Stub response
    stub_data = []
    for i in range(50):
        stub_data.append(TimeSeriesDataPoint(
            date=f"2024-{(i % 12) + 1:02d}-{(i % 28) + 1:02d}",
            value=float(50 + (i % 20))
        ))

    return stub_data


@app.get("/metrics/correlation", response_model=CorrelationResponse)
async def get_correlation_data(
    x_metric: str,
    y_metric: str,
    lag_days: Optional[int] = 0
):
    """
    Get correlation data between two metrics

    Returns aligned values for scatter plots and correlation stats

    TODO: Implement actual correlation analysis
    """
    logger.info(f"Calculating correlation: {x_metric} vs {y_metric} (lag={lag_days})")

    # TODO: Query both metrics from DB
    # TODO: Align by date with optional lag
    # TODO: Calculate Pearson/Spearman correlation
    # TODO: Return scatter data and stats

    # Stub response
    return CorrelationResponse(
        x_values=[1.0, 2.0, 3.0, 4.0, 5.0],
        y_values=[2.0, 4.0, 6.0, 8.0, 10.0],
        dates=["2024-01-01", "2024-01-02", "2024-01-03", "2024-01-04", "2024-01-05"],
        stats={
            "pearson_r": 0.95,
            "pearson_p": 0.001,
            "spearman_r": 0.93,
            "spearman_p": 0.002,
            "n": 5
        }
    )


# ============================================================================
# Settings Endpoints
# ============================================================================

@app.post("/settings/data-root")
async def set_data_root(request: DataRootRequest):
    """
    Set or update the root directory for data storage

    TODO: Implement persistent settings storage
    """
    logger.info(f"Setting data root to: {request.data_root}")

    # TODO: Validate directory exists or create it
    # TODO: Store setting in config file or DB
    # TODO: Migrate existing data if needed

    return {"success": True, "message": "Data root updated"}


# ============================================================================
# Main
# ============================================================================

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Foldline Backend Server")
    parser.add_argument("--port", type=int, default=8000, help="Port to run on")
    parser.add_argument("--host", type=str, default="127.0.0.1", help="Host to bind to")
    args = parser.parse_args()

    logger.info(f"Starting Foldline backend on {args.host}:{args.port}")
    logger.info("This is a LOCAL-ONLY server. No external API calls are made.")

    uvicorn.run(
        app,
        host=args.host,  # MUST be 127.0.0.1 for security
        port=args.port,
        log_level="info"
    )
