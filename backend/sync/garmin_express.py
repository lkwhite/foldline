"""
Garmin Express Device Detection

Detects Garmin devices synced via Garmin Express and extracts device metadata.

Platform-specific paths:
- macOS: ~/Library/Application Support/Garmin/Devices/<DEVICE-ID>/
- Windows: %APPDATA%\Garmin\Devices\<DEVICE-ID>\

Implements CONTINUAL_SYNC_SPEC.md §3.2 Device Detection Logic
"""

import os
import platform
from pathlib import Path
from typing import List, Dict, Any, Optional
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


def get_garmin_express_root() -> Optional[Path]:
    """
    Get platform-specific Garmin Express root directory

    Returns:
        Path to Garmin Devices directory, or None if not found
    """
    system = platform.system()

    if system == "Darwin":  # macOS
        root = Path.home() / "Library" / "Application Support" / "Garmin" / "Devices"
    elif system == "Windows":
        appdata = os.environ.get("APPDATA")
        if not appdata:
            logger.error("APPDATA environment variable not found on Windows")
            return None
        root = Path(appdata) / "Garmin" / "Devices"
    elif system == "Linux":
        # Garmin Express doesn't officially support Linux, but users may have
        # synced folders via Wine or manual setup
        root = Path.home() / ".wine" / "drive_c" / "users" / os.environ.get("USER", "user") / "AppData" / "Roaming" / "Garmin" / "Devices"
    else:
        logger.warning(f"Unsupported platform: {system}")
        return None

    if not root.exists():
        logger.info(f"Garmin Express directory not found: {root}")
        return None

    logger.info(f"Found Garmin Express directory: {root}")
    return root


def count_fit_files(device_path: Path) -> int:
    """
    Recursively count .fit files in a device directory

    Args:
        device_path: Path to device folder

    Returns:
        Count of .fit files found
    """
    count = 0
    try:
        for root, dirs, files in os.walk(device_path):
            for file in files:
                if file.lower().endswith('.fit'):
                    count += 1
    except Exception as e:
        logger.error(f"Error counting FIT files in {device_path}: {e}")

    return count


def get_most_recent_fit_time(device_path: Path) -> Optional[datetime]:
    """
    Get the modified time of the most recently modified .fit file

    Args:
        device_path: Path to device folder

    Returns:
        Datetime of most recent file, or None if no files found
    """
    most_recent = None

    try:
        for root, dirs, files in os.walk(device_path):
            for file in files:
                if file.lower().endswith('.fit'):
                    file_path = Path(root) / file
                    try:
                        mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
                        if most_recent is None or mtime > most_recent:
                            most_recent = mtime
                    except Exception as e:
                        logger.debug(f"Could not get mtime for {file_path}: {e}")

    except Exception as e:
        logger.error(f"Error scanning for recent files in {device_path}: {e}")

    return most_recent


def get_device_subfolders(device_path: Path) -> List[str]:
    """
    Get list of subdirectories in device folder

    Common folders: Activities, Monitor, Sleep, Stress, Daily

    Args:
        device_path: Path to device folder

    Returns:
        List of subfolder names
    """
    subfolders = []

    try:
        for item in device_path.iterdir():
            if item.is_dir():
                subfolders.append(item.name)
    except Exception as e:
        logger.error(f"Error reading subfolders in {device_path}: {e}")

    return subfolders


def extract_device_name(device_path: Path, device_id: str) -> str:
    """
    Try to extract device name from device.fit or device.xml

    Falls back to device ID if name cannot be determined.

    Args:
        device_path: Path to device folder
        device_id: Device ID (folder name)

    Returns:
        Device name or device ID
    """
    # Try device.fit first (if fitparse available)
    device_fit = device_path / "device.fit"
    if device_fit.exists():
        try:
            from fitparse import FitFile
            fitfile = FitFile(str(device_fit))
            for record in fitfile.get_messages("device_info"):
                for field in record:
                    if field.name == "product_name" and field.value:
                        logger.info(f"Found device name from FIT: {field.value}")
                        return field.value
        except Exception as e:
            logger.debug(f"Could not parse device.fit: {e}")

    # Try device.xml (if present)
    device_xml = device_path / "device.xml"
    if device_xml.exists():
        try:
            import xml.etree.ElementTree as ET
            tree = ET.parse(device_xml)
            root = tree.getroot()
            # Look for common name fields in XML
            for tag in ["Name", "ProductName", "DeviceName", "Model"]:
                name_elem = root.find(f".//{tag}")
                if name_elem is not None and name_elem.text:
                    logger.info(f"Found device name from XML: {name_elem.text}")
                    return name_elem.text
        except Exception as e:
            logger.debug(f"Could not parse device.xml: {e}")

    # Fallback: use device ID
    logger.info(f"Using device ID as name: {device_id}")
    return device_id


def get_device_info(device_path: Path, device_id: str) -> Dict[str, Any]:
    """
    Extract comprehensive device information

    Args:
        device_path: Path to device folder
        device_id: Device ID (folder name)

    Returns:
        Dictionary with device metadata
    """
    file_count = count_fit_files(device_path)
    last_sync = get_most_recent_fit_time(device_path)
    subfolders = get_device_subfolders(device_path)
    device_name = extract_device_name(device_path, device_id)

    return {
        "device_id": device_id,
        "name": device_name,
        "path": str(device_path),
        "file_count": file_count,
        "last_sync": last_sync.isoformat() if last_sync else None,
        "subfolders": subfolders
    }


def detect_garmin_devices() -> List[Dict[str, Any]]:
    """
    Detect all Garmin Express devices

    Implements CONTINUAL_SYNC_SPEC.md §3.2 Device Detection Logic:
    1. Search known platform-specific Garmin Express roots
    2. For each <DEVICE-ID> folder:
       - Look for subfolders containing .fit files
       - Record count of files + most recent modification time
    3. Present each device with metadata

    Returns:
        List of device info dictionaries, or empty list if none found
    """
    logger.info("Detecting Garmin Express devices...")

    devices = []

    # Get Garmin Express root directory
    root = get_garmin_express_root()
    if not root:
        logger.warning("Garmin Express not found on this system")
        return devices

    # Scan for device folders
    try:
        for item in root.iterdir():
            if item.is_dir():
                device_id = item.name
                logger.info(f"Found device folder: {device_id}")

                # Get device info
                device_info = get_device_info(item, device_id)

                # Only include devices with .fit files
                if device_info["file_count"] > 0:
                    devices.append(device_info)
                    logger.info(f"Added device: {device_info['name']} ({device_info['file_count']} files)")
                else:
                    logger.debug(f"Skipping device {device_id} (no FIT files)")

    except Exception as e:
        logger.error(f"Error scanning Garmin Express devices: {e}")

    logger.info(f"Detected {len(devices)} Garmin Express device(s)")
    return devices


def get_installation_guidance() -> Dict[str, Any]:
    """
    Provide platform-specific guidance for installing Garmin Express

    Returns:
        Dictionary with install URL and platform-specific instructions
    """
    system = platform.system()

    guidance = {
        "platform": system,
        "download_url": "https://www.garmin.com/en-US/software/express/",
        "instructions": []
    }

    if system == "Darwin":  # macOS
        guidance["instructions"] = [
            "1. Download Garmin Express from garmin.com",
            "2. Install and launch Garmin Express",
            "3. Connect your Garmin device via USB cable",
            "4. Follow the on-screen setup instructions",
            "5. Return to Foldline and click 'Detect Devices'"
        ]
    elif system == "Windows":
        guidance["instructions"] = [
            "1. Download Garmin Express from garmin.com",
            "2. Run the installer",
            "3. Launch Garmin Express",
            "4. Connect your Garmin device via USB cable",
            "5. Complete the device setup",
            "6. Return to Foldline and click 'Detect Devices'"
        ]
    elif system == "Linux":
        guidance["instructions"] = [
            "Note: Garmin Express doesn't officially support Linux.",
            "Alternative: Use manual FIT folder import instead.",
            "Or: Try running Garmin Express via Wine (advanced)."
        ]

    return guidance
