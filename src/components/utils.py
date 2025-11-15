import json
import logging
import re
from datetime import datetime
from typing import Callable, Dict, List, Optional, Tuple, Union

import pytz
from dateutil.parser import parse
from pytz import UnknownTimeZoneError

logger = logging.getLogger(__name__)

def parse_timestamp(timestamp: str) -> datetime:
    """Parse a timestamp in various formats to a datetime object."""
    try:
        return parse(timestamp)
    except ValueError:
        try:
            return datetime.fromisoformat(timestamp)
        except ValueError:
            return datetime.fromtimestamp(float(timestamp))

def validate_timezone(timezone: str) -> bool:
    """Check if a timezone is valid."""
    try:
        pytz.timezone(timezone)
        return True
    except UnknownTimeZoneError:
        return False

def parse_duration(duration: str) -> Tuple[int, int]:
    """Parse a duration in the format 'X days, Y hours, Z minutes, W seconds' to (days, hours, minutes, seconds)."""
    match = re.match(r'(\d+) days, (\d+) hours, (\d+) minutes, (\d+) seconds', duration)
    if match:
        days, hours, minutes, seconds = match.groups()
        return int(days), int(hours), int(minutes), int(seconds)
    raise ValueError('Invalid duration format')

def parse_interval(interval: str) -> Tuple[int, int]:
    """Parse a interval in the format 'X days, Y hours, Z minutes' to (days, hours, minutes)."""
    match = re.match(r'(\d+) days, (\d+) hours, (\d+) minutes', interval)
    if match:
        days, hours, minutes = match.groups()
        return int(days), int(hours), int(minutes)
    raise ValueError('Invalid interval format')

def validate_email_address(email: str) -> bool:
    """Check if an email address is valid."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def flatten_dict(nested_dict: Dict) -> Dict:
    """Flatten a nested dictionary to a single-level dictionary."""
    flat_dict = {}
    for key, value in nested_dict.items():
        if isinstance(value, dict):
            flat_dict.update(flatten_dict(value))
        else:
            flat_dict[key] = value
    return flat_dict

def get_callable_description(callable_: Callable) -> str:
    """Get a string description of a callable."""
    return callable_.__doc__ or callable_.__name__