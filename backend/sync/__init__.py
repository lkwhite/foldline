"""
Sync Module

Handles Garmin Express device detection and continual synchronization.
"""

from .garmin_express import (
    detect_garmin_devices,
    get_device_info,
    get_installation_guidance
)
from .sync_engine import (
    sync_garmin_express_device,
    sync_all_enabled_devices,
    register_device,
    get_enabled_devices
)

__all__ = [
    'detect_garmin_devices',
    'get_device_info',
    'get_installation_guidance',
    'sync_garmin_express_device',
    'sync_all_enabled_devices',
    'register_device',
    'get_enabled_devices'
]
