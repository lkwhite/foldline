"""
Steps/Activity Metrics

Functions to query and analyze step count data
"""

from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


def get_steps_heatmap(
    db_connection,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Get daily step counts for heatmap

    Returns:
        List of {date, value} where value is step count
    """
    logger.info(f"Fetching steps heatmap data: {start_date} to {end_date}")

    # TODO: Query daily_steps table
    # TODO: Return as list of {date, step_count}

    return []
