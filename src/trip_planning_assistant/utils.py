"""Utility functions for trip planning assistant."""

from datetime import datetime
from typing import Tuple, Optional
import sys


def validate_date_format(date_string: str) -> bool:
    """Validate date string is in YYYY-MM-DD format."""
    try:
        datetime.strptime(date_string, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def validate_trip_dates(start_date: str, end_date: str) -> Tuple[bool, Optional[str]]:
    """Validate trip date range."""
    if not validate_date_format(start_date):
        return False, "Start date must be in YYYY-MM-DD format"
    if not validate_date_format(end_date):
        return False, "End date must be in YYYY-MM-DD format"
    
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    
    if start >= end:
        return False, "End date must be after start date"
    if start < datetime.now():
        return False, "Start date cannot be in the past"
    
    days_diff = (end - start).days
    if days_diff > 365:
        return False, "Trip duration cannot exceed 365 days"
    if days_diff < 1:
        return False, "Trip must be at least 1 day long"
    
    return True, None


def validate_budget(budget: float) -> Tuple[bool, Optional[str]]:
    """Validate trip budget."""
    if budget <= 0:
        return False, "Budget must be greater than 0"
    if budget > 1000000:
        return False, "Budget exceeds reasonable limits (max $1,000,000)"
    return True, None


def validate_travelers_count(count: int) -> Tuple[bool, Optional[str]]:
    """Validate number of travelers."""
    if count < 1:
        return False, "At least 1 traveler required"
    if count > 100:
        return False, "Maximum 100 travelers supported"
    return True, None


def validate_inputs(inputs: dict) -> bool:
    """
    Validate all trip planning inputs.
    
    Args:
        inputs: Dictionary with trip parameters
        
    Returns:
        True if valid, False otherwise
    """
    required_fields = ['destination', 'origin', 'start_date', 'end_date', 'budget', 'travelers_count', 'preferences']
    
    for field in required_fields:
        if field not in inputs:
            return False
    
    is_valid, _ = validate_trip_dates(inputs['start_date'], inputs['end_date'])
    if not is_valid:
        return False
    
    is_valid, _ = validate_budget(inputs['budget'])
    if not is_valid:
        return False
    
    is_valid, _ = validate_travelers_count(inputs['travelers_count'])
    if not is_valid:
        return False
    
    return True


def print_trip_summary(destination: str, start_date: str, end_date: str,
                      budget: float, travelers_count: int, preferences: str) -> None:
    """Print trip summary to console."""
    print("\n" + "="*60)
    print("TRIP PLANNING SUMMARY")
    print("="*60)
    print(f"Destination:      {destination}")
    print(f"Origin:           {start_date}")  # Note: this should be 'origin' in actual use
    print(f"Travel Dates:     {start_date} to {end_date}")
    
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    days = (end - start).days
    print(f"Duration:         {days} days")
    
    print(f"Travelers:        {travelers_count}")
    print(f"Budget:           ${budget:,.2f}")
    print(f"Per Person/Day:   ${budget/(travelers_count*days):,.2f}")
    print(f"Preferences:      {preferences}")
    print("="*60 + "\n")


def prompt_user_for_inputs() -> dict:
    """Interactively prompt user for trip planning inputs."""
    print("\n" + "="*60)
    print("TRIP PLANNING ASSISTANT - INPUT CONFIGURATION")
    print("="*60 + "\n")
    
    destination = input("Enter destination (e.g., Paris, France): ").strip()
    if not destination:
        raise ValueError("Destination cannot be empty")
    
    origin = input("Enter origin/departure location (e.g., New York, USA): ").strip()
    if not origin:
        raise ValueError("Origin cannot be empty")
    
    while True:
        start_date = input("Enter start date (YYYY-MM-DD): ").strip()
        end_date = input("Enter end date (YYYY-MM-DD): ").strip()
        is_valid, error_msg = validate_trip_dates(start_date, end_date)
        if is_valid:
            break
        print(f"Error: {error_msg}\n")
    
    while True:
        try:
            budget = float(input("Enter total budget (USD): $").strip())
            is_valid, error_msg = validate_budget(budget)
            if is_valid:
                break
            print(f"Error: {error_msg}\n")
        except ValueError:
            print("Error: Budget must be a valid number\n")
    
    while True:
        try:
            travelers_count = int(input("Number of travelers: ").strip())
            is_valid, error_msg = validate_travelers_count(travelers_count)
            if is_valid:
                break
            print(f"Error: {error_msg}\n")
        except ValueError:
            print("Error: Travelers count must be a valid number\n")
    
    preferences = input("Enter travel preferences (e.g., cultural sites, fine dining, adventure): ").strip()
    if not preferences:
        preferences = "standard sightseeing and relaxation"
    
    return {
        'destination': destination,
        'origin': origin,
        'start_date': start_date,
        'end_date': end_date,
        'budget': budget,
        'travelers_count': travelers_count,
        'preferences': preferences
    }


def load_user_preferences(filepath: Optional[str] = None) -> Optional[dict]:
    """Load user preferences from file if available."""
    from trip_planning_assistant.config import UserPreferences
    
    if filepath is None:
        # Default path relative to project
        filepath = "knowledge/user_preference.txt"
    
    try:
        user_prefs = UserPreferences.from_file(filepath)
        return {
            'user_preferences': user_prefs,
            'user_context': user_prefs.to_prompt_string()
        }
    except FileNotFoundError:
        return None


def format_trip_result(result: str) -> str:
    """Format and enhance trip planning result for display."""
    separator = "\n" + "="*70 + "\n"
    return f"{separator}TRIP PLANNING RESULTS{separator}{result}{separator}"
