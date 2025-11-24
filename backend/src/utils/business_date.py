"""
Business date utility functions for SLA calculations.

This module provides functions to calculate business time (excluding weekends)
for SLA calculations. The system supports 24/7 monitoring but pauses counting
during weekends to prevent false breaches.

Note: Holidays are not yet implemented, but the design anticipates adding them
in the future by extending the is_business_day function.
"""

from datetime import datetime, timedelta, timezone


# Business weekdays: Monday=0, Tuesday=1, ..., Friday=4
BUSINESS_WEEKDAYS = {0, 1, 2, 3, 4}


def is_weekend(dt: datetime) -> bool:
    """
    Check if a datetime falls on a weekend (Saturday or Sunday).
    
    Args:
        dt: The datetime to check
        
    Returns:
        bool: True if the datetime is on a weekend, False otherwise
    """
    return dt.weekday() not in BUSINESS_WEEKDAYS


def is_business_day(dt: datetime) -> bool:
    """
    Check if a datetime falls on a business day.
    
    Currently only excludes weekends. Holidays can be added in the future
    by extending this function.
    
    Args:
        dt: The datetime to check
        
    Returns:
        bool: True if the datetime is on a business day, False otherwise
    """
    return not is_weekend(dt)


def normalize_datetime(dt: datetime) -> datetime:
    """
    Normalize a datetime to UTC naive format for consistent calculations.
    
    Args:
        dt: The datetime to normalize (can be timezone-aware or naive)
        
    Returns:
        datetime: Naive datetime in UTC
    """
    if dt.tzinfo is not None:
        return dt.astimezone(timezone.utc).replace(tzinfo=None)
    return dt


def business_seconds_between(start: datetime, end: datetime) -> int:
    """
    Calculate the number of business seconds between two datetimes.
    
    This function excludes weekends from the calculation. It iterates day by day
    and only counts time that falls on business days (Monday-Friday).
    
    Args:
        start: Start datetime (inclusive)
        end: End datetime (exclusive for calculation purposes)
        
    Returns:
        int: Number of business seconds between start and end
    """
    # Normalize to UTC naive datetimes
    start_utc = normalize_datetime(start)
    end_utc = normalize_datetime(end)
    
    # Handle edge cases
    if start_utc >= end_utc:
        return 0
    
    total_seconds = 0
    current = start_utc
    
    # Iterate day by day
    while current < end_utc:
        # Get the start and end of the current day
        day_start = current.replace(hour=0, minute=0, second=0, microsecond=0)
        day_end = day_start + timedelta(days=1)
        
        # Determine the actual start and end times for this day's calculation
        actual_start = max(current, day_start)
        actual_end = min(end_utc, day_end)
        
        # Only count if this is a business day
        if is_business_day(current):
            # Calculate seconds in this day's portion
            day_seconds = int((actual_end - actual_start).total_seconds())
            total_seconds += day_seconds
        
        # Move to the start of the next day
        current = day_end
    
    return total_seconds


def add_business_seconds(start: datetime, seconds: int) -> datetime:
    """
    Add business seconds to a datetime, skipping weekends.
    
    This function adds the specified number of business seconds to the start
    datetime, excluding any time that falls on weekends.
    
    Args:
        start: Starting datetime
        seconds: Number of business seconds to add (must be non-negative)
        
    Returns:
        datetime: Resulting datetime after adding business seconds
    """
    if seconds < 0:
        raise ValueError("seconds must be non-negative")
    
    if seconds == 0:
        return normalize_datetime(start)
    
    # Normalize to UTC naive datetime
    current = normalize_datetime(start)
    remaining_seconds = seconds
    
    # Iterate day by day, adding business seconds
    while remaining_seconds > 0:
        # Get the start and end of the current day
        day_start = current.replace(hour=0, minute=0, second=0, microsecond=0)
        day_end = day_start + timedelta(days=1)
        
        # Calculate how many seconds are left in the current day
        seconds_in_day = int((day_end - current).total_seconds())
        
        # Only count business days
        if is_business_day(current):
            # If we can fit all remaining seconds in this day, add them and return
            if remaining_seconds <= seconds_in_day:
                return current + timedelta(seconds=remaining_seconds)
            
            # Otherwise, use up all the business seconds in this day
            remaining_seconds -= seconds_in_day
        
        # Move to the start of the next day
        current = day_end
    
    return current

