"""
Field Mappings for Garmin GDPR Export Data

Maps Garmin's GDPR JSON field names to Foldline's database schema.
Handles field name variations across different export versions.

References:
- FOLDLINE_HANDOFF.md - GDPR field mappings
- CONTINUAL_SYNC_SPEC.md - FIT ingestion pipeline
- PRE_COMMERCIAL_MVP_PLAN.md - Week 1 requirements
"""

from typing import Dict, Any, Optional, List
from datetime import datetime, date
import logging

logger = logging.getLogger(__name__)


# ============================================================================
# Sleep Field Mappings
# ============================================================================

SLEEP_FIELD_MAPPINGS = {
    # Primary fields (try these first)
    "sleep_start_gmt": ["sleepStartTimestampGMT", "sleepStartTimestampLocal", "sleepStart"],
    "sleep_end_gmt": ["sleepEndTimestampGMT", "sleepEndTimestampLocal", "sleepEnd"],
    "deep_sleep_seconds": ["deepSleepSeconds", "deepSleep"],
    "light_sleep_seconds": ["lightSleepSeconds", "lightSleep"],
    "rem_sleep_seconds": ["remSleepSeconds", "remSleep"],
    "awake_sleep_seconds": ["awakeSleepSeconds", "awakeSeconds", "awakeSleep"],
    "sleep_window_confirmation_type": ["sleepWindowConfirmationType", "confirmationType"],
    "average_respiration": ["averageRespiration", "avgRespiration"],
    "lowest_respiration": ["lowestRespiration", "minRespiration"],
    "highest_respiration": ["highestRespiration", "maxRespiration"],
    "average_spo2": ["averageSpO2Value", "avgSpO2", "averageSpo2"],
    "lowest_spo2": ["lowestSpO2Value", "minSpO2", "lowestSpo2"],
    "average_sleep_hr": ["avgSleepHeartRate", "averageHeartRate", "avgHR"],
    "sleep_score": ["sleepScore", "overallSleepScore"],
    "calendar_date": ["calendarDate", "date"]
}


# ============================================================================
# Daily Summary Field Mappings
# ============================================================================

DAILY_SUMMARY_FIELD_MAPPINGS = {
    "calendar_date": ["calendarDate", "date"],
    "step_count": ["totalSteps", "steps", "stepCount"],
    "calories_burned": ["totalKilocalories", "calories", "totalCalories"],
    "distance_meters": ["totalDistanceMeters", "distanceMeters", "distance"],
    "floors_climbed": ["floorsAscended", "floorsClimbed", "floors"],
    "active_minutes": ["activeKilocalories", "activeMinutes"],
    "sedentary_minutes": ["sedentaryKilocalories", "sedentaryMinutes"],
    "min_heart_rate": ["minHeartRate", "minHR"],
    "max_heart_rate": ["maxHeartRate", "maxHR"],
    "resting_heart_rate": ["restingHeartRate", "restingHR", "restingHr"],
    "avg_heart_rate": ["averageHeartRate", "avgHeartRate", "avgHR"],
    "stress_avg": ["averageStressLevel", "avgStress", "stressAvg"],
    "stress_max": ["maxStressLevel", "maxStress"],
    "stress_min": ["restStressLevel", "minStress"],
    "body_battery_charged": ["bodyBatteryChargedValue", "bodyBatteryCharged"],
    "body_battery_drained": ["bodyBatteryDrainedValue", "bodyBatteryDrained"],
    "body_battery_start": ["bodyBatteryHighestValue", "bodyBatteryStart", "bodyBatteryMax"],
    "body_battery_end": ["bodyBatteryLowestValue", "bodyBatteryEnd", "bodyBatteryMin"],
    "intensity_minutes_moderate": ["moderateIntensityMinutes", "moderateMinutes"],
    "intensity_minutes_vigorous": ["vigorousIntensityMinutes", "vigorousMinutes"]
}


# ============================================================================
# HRV Field Mappings
# ============================================================================

HRV_FIELD_MAPPINGS = {
    "hrv_value": ["hrvValue", "rmssd", "weeklyAvg", "lastNightAvg"],
    "measurement_type": ["measurementType", "type"],
    "calendar_date": ["calendarDate", "date", "createTimeStamp"]
}


# ============================================================================
# Stress Field Mappings
# ============================================================================

STRESS_FIELD_MAPPINGS = {
    "calendar_date": ["calendarDate", "date"],
    "avg_stress": ["avgStressLevel", "averageStressLevel", "avgStress"],
    "max_stress": ["maxStressLevel", "maxStress"],
    "min_stress": ["restStressLevel", "minStress"],
    "rest_stress": ["restStressDuration", "restDuration"],
    "activity_stress": ["activityStressDuration", "activityDuration"],
    "low_stress_duration": ["lowStressDuration"],
    "medium_stress_duration": ["mediumStressDuration"],
    "high_stress_duration": ["highStressDuration"]
}


# ============================================================================
# Activity Field Mappings
# ============================================================================

ACTIVITY_FIELD_MAPPINGS = {
    "activity_id": ["activityId", "id"],
    "start_time": ["startTimeGMT", "startTimeLocal", "beginTimestamp"],
    "activity_type": ["activityType", "sport", "activityName"],
    "duration_seconds": ["duration", "elapsedDuration", "totalTimeSeconds"],
    "distance_meters": ["distance", "totalDistance"],
    "avg_hr": ["averageHR", "avgHR", "averageHeartRate"],
    "max_hr": ["maxHR", "maxHeartRate"],
    "training_load": ["trainingLoad", "aerobicTrainingEffect"],
    "training_effect_aerobic": ["aerobicTrainingEffect", "trainingEffect"],
    "training_effect_anaerobic": ["anaerobicTrainingEffect"],
    "calories": ["calories", "totalCalories"]
}


# ============================================================================
# Fitness Assessment Field Mappings
# ============================================================================

FITNESS_ASSESSMENT_FIELD_MAPPINGS = {
    "assessment_date": ["calendarDate", "date", "createDate"],
    "vo2_max_value": ["vo2MaxValue", "vo2Max"],
    "fitness_age": ["fitnessAge"],
    "max_met": ["maxMet"],
    "sport": ["sport"],
    "sub_sport": ["subSport"],
    "calibrated_data": ["calibratedData"]
}


# ============================================================================
# Hydration Field Mappings
# ============================================================================

HYDRATION_FIELD_MAPPINGS = {
    "log_date": ["calendarDate", "date"],
    "timestamp_gmt": ["timestampGMT", "timestamp"],
    "value_ml": ["valueInML", "value", "hydrationValueInML"],
    "estimated_sweat_loss_ml": ["estimatedSweatLoss", "sweatLoss"],
    "hydration_source": ["source"],
    "activity_id": ["activityId"]
}


# ============================================================================
# Body Composition Field Mappings
# ============================================================================

BODY_COMPOSITION_FIELD_MAPPINGS = {
    "measurement_date": ["timestampGMT", "date", "samplePk"],
    "weight_kg": ["weight", "weightInKG"],
    "body_fat_percentage": ["bodyFat", "bodyFatPercentage"],
    "muscle_mass_kg": ["muscleMass", "muscleMassInKG"],
    "bone_mass_kg": ["boneMass", "boneMassInKG"],
    "water_percentage": ["bodyWater", "bodyWaterPercentage"],
    "visceral_fat_rating": ["visceralFatRating"],
    "metabolic_age": ["metabolicAge"],
    "bmi": ["bmi", "BMI"],
    "measurement_source": ["sourceType"]
}


# ============================================================================
# Menstrual Cycle Field Mappings
# ============================================================================

MENSTRUAL_CYCLE_FIELD_MAPPINGS = {
    "cycle_start_date": ["startDate", "cycleStartDate"],
    "cycle_end_date": ["endDate", "cycleEndDate"],
    "cycle_length_days": ["cycleLengthInDays", "cycleLength"],
    "period_start_date": ["periodStartDate"],
    "period_end_date": ["periodEndDate"],
    "period_length_days": ["periodLengthInDays", "periodLength"],
    "cycle_confirmed": ["confirmed"],
    "fertility_window_start": ["fertilityWindowStartDate"],
    "fertility_window_end": ["fertilityWindowEndDate"],
    "ovulation_estimated_date": ["estimatedOvulationDate"],
    "hormonal_contraception": ["hormonalContraception"],
    "skin_temperature_enabled": ["skinTemperatureEnabled"]
}


# ============================================================================
# Helper Functions
# ============================================================================

def get_field_value(data: Dict[str, Any], field_mappings: List[str], default=None) -> Any:
    """
    Get field value trying multiple field name variations

    Args:
        data: Source data dictionary
        field_mappings: List of possible field names to try
        default: Default value if none found

    Returns:
        Field value or default
    """
    for field_name in field_mappings:
        if field_name in data and data[field_name] is not None:
            return data[field_name]
    return default


def map_sleep_record(json_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Map GDPR sleep JSON to Foldline schema

    Args:
        json_data: Raw GDPR sleep data

    Returns:
        Mapped sleep record
    """
    mapped = {}

    for db_field, json_fields in SLEEP_FIELD_MAPPINGS.items():
        value = get_field_value(json_data, json_fields)
        if value is not None:
            mapped[db_field] = value

    return mapped


def map_daily_summary_record(json_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Map GDPR daily summary JSON to Foldline schema

    Args:
        json_data: Raw GDPR daily summary data

    Returns:
        Mapped daily summary record
    """
    mapped = {}

    for db_field, json_fields in DAILY_SUMMARY_FIELD_MAPPINGS.items():
        value = get_field_value(json_data, json_fields)
        if value is not None:
            mapped[db_field] = value

    return mapped


def map_hrv_record(json_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Map GDPR HRV JSON to Foldline schema

    Args:
        json_data: Raw GDPR HRV data

    Returns:
        Mapped HRV record
    """
    mapped = {}

    for db_field, json_fields in HRV_FIELD_MAPPINGS.items():
        value = get_field_value(json_data, json_fields)
        if value is not None:
            mapped[db_field] = value

    # Determine measurement type if not explicitly provided
    if "measurement_type" not in mapped:
        if "rmssd" in json_data or "weeklyAvg" in json_data:
            mapped["measurement_type"] = "rmssd"
        else:
            mapped["measurement_type"] = "unknown"

    return mapped


def map_stress_record(json_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Map GDPR stress JSON to Foldline schema

    Args:
        json_data: Raw GDPR stress data

    Returns:
        Mapped stress record
    """
    mapped = {}

    for db_field, json_fields in STRESS_FIELD_MAPPINGS.items():
        value = get_field_value(json_data, json_fields)
        if value is not None:
            mapped[db_field] = value

    return mapped


def map_activity_record(json_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Map GDPR activity JSON to Foldline schema

    Args:
        json_data: Raw GDPR activity data

    Returns:
        Mapped activity record
    """
    mapped = {}

    for db_field, json_fields in ACTIVITY_FIELD_MAPPINGS.items():
        value = get_field_value(json_data, json_fields)
        if value is not None:
            mapped[db_field] = value

    return mapped


def map_fitness_assessment_record(json_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Map GDPR fitness assessment JSON to Foldline schema

    Args:
        json_data: Raw GDPR fitness assessment data

    Returns:
        Mapped fitness assessment record
    """
    mapped = {}

    for db_field, json_fields in FITNESS_ASSESSMENT_FIELD_MAPPINGS.items():
        value = get_field_value(json_data, json_fields)
        if value is not None:
            mapped[db_field] = value

    return mapped


def map_hydration_record(json_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Map GDPR hydration JSON to Foldline schema

    Args:
        json_data: Raw GDPR hydration data

    Returns:
        Mapped hydration record
    """
    mapped = {}

    for db_field, json_fields in HYDRATION_FIELD_MAPPINGS.items():
        value = get_field_value(json_data, json_fields)
        if value is not None:
            mapped[db_field] = value

    return mapped


def map_body_composition_record(json_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Map GDPR body composition JSON to Foldline schema

    Args:
        json_data: Raw GDPR body composition data

    Returns:
        Mapped body composition record
    """
    mapped = {}

    for db_field, json_fields in BODY_COMPOSITION_FIELD_MAPPINGS.items():
        value = get_field_value(json_data, json_fields)
        if value is not None:
            mapped[db_field] = value

    return mapped


def map_menstrual_cycle_record(json_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Map GDPR menstrual cycle JSON to Foldline schema

    Args:
        json_data: Raw GDPR menstrual cycle data

    Returns:
        Mapped menstrual cycle record
    """
    mapped = {}

    for db_field, json_fields in MENSTRUAL_CYCLE_FIELD_MAPPINGS.items():
        value = get_field_value(json_data, json_fields)
        if value is not None:
            mapped[db_field] = value

    return mapped


def parse_date(date_str: str) -> Optional[date]:
    """
    Parse various date formats found in Garmin JSON files

    Args:
        date_str: Date string to parse

    Returns:
        date object or None if parsing fails
    """
    if not date_str:
        return None

    # Common formats: "2024-01-15", "2024-01-15T08:30:00.0"
    try:
        if 'T' in date_str:
            return datetime.fromisoformat(date_str.replace('Z', '')).date()
        else:
            return datetime.fromisoformat(date_str).date()
    except (ValueError, TypeError):
        logger.warning(f"Could not parse date: {date_str}")
        return None


def parse_timestamp(ts_str: str) -> Optional[datetime]:
    """
    Parse timestamp formats found in Garmin JSON files

    Args:
        ts_str: Timestamp string to parse

    Returns:
        datetime object or None if parsing fails
    """
    if not ts_str:
        return None

    try:
        # Handle both with and without timezone
        if ts_str.endswith('Z'):
            ts_str = ts_str[:-1] + '+00:00'
        return datetime.fromisoformat(ts_str.replace('Z', ''))
    except (ValueError, TypeError):
        logger.warning(f"Could not parse timestamp: {ts_str}")
        return None
