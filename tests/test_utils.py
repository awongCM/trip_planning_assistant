"""Unit tests for utils module."""

import unittest
from datetime import datetime, timedelta
from trip_planning_assistant.utils import (
    validate_date_format,
    validate_trip_dates,
    validate_budget,
    validate_travelers_count
)


class TestValidation(unittest.TestCase):
    """Test validation functions."""

    def test_validate_date_format_valid(self):
        """Test valid date format."""
        self.assertTrue(validate_date_format("2026-06-01"))
        self.assertTrue(validate_date_format("2025-12-31"))

    def test_validate_date_format_invalid(self):
        """Test invalid date formats."""
        self.assertFalse(validate_date_format("06-01-2026"))
        self.assertFalse(validate_date_format("2026/06/01"))
        self.assertFalse(validate_date_format("invalid"))
        self.assertFalse(validate_date_format("2026-13-01"))  # Invalid month

    def test_validate_trip_dates_valid(self):
        """Test valid trip date range."""
        start = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
        end = (datetime.now() + timedelta(days=40)).strftime("%Y-%m-%d")
        is_valid, error = validate_trip_dates(start, end)
        self.assertTrue(is_valid)
        self.assertIsNone(error)

    def test_validate_trip_dates_invalid_format(self):
        """Test invalid date format."""
        is_valid, error = validate_trip_dates("invalid", "2026-06-10")
        self.assertFalse(is_valid)
        self.assertIsNotNone(error)

    def test_validate_trip_dates_past(self):
        """Test dates in the past."""
        past_date = (datetime.now() - timedelta(days=10)).strftime("%Y-%m-%d")
        future_date = (datetime.now() + timedelta(days=10)).strftime("%Y-%m-%d")
        is_valid, error = validate_trip_dates(past_date, future_date)
        self.assertFalse(is_valid)

    def test_validate_trip_dates_reversed(self):
        """Test end date before start date."""
        start = (datetime.now() + timedelta(days=40)).strftime("%Y-%m-%d")
        end = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
        is_valid, error = validate_trip_dates(start, end)
        self.assertFalse(is_valid)

    def test_validate_trip_dates_too_long(self):
        """Test trip longer than 365 days."""
        start = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
        end = (datetime.now() + timedelta(days=400)).strftime("%Y-%m-%d")
        is_valid, error = validate_trip_dates(start, end)
        self.assertFalse(is_valid)

    def test_validate_budget_valid(self):
        """Test valid budgets."""
        is_valid, error = validate_budget(5000)
        self.assertTrue(is_valid)
        
        is_valid, error = validate_budget(100.50)
        self.assertTrue(is_valid)

    def test_validate_budget_invalid_zero(self):
        """Test zero budget."""
        is_valid, error = validate_budget(0)
        self.assertFalse(is_valid)

    def test_validate_budget_invalid_negative(self):
        """Test negative budget."""
        is_valid, error = validate_budget(-1000)
        self.assertFalse(is_valid)

    def test_validate_budget_too_high(self):
        """Test budget exceeding limit."""
        is_valid, error = validate_budget(2000000)
        self.assertFalse(is_valid)

    def test_validate_travelers_count_valid(self):
        """Test valid traveler counts."""
        is_valid, error = validate_travelers_count(1)
        self.assertTrue(is_valid)
        
        is_valid, error = validate_travelers_count(50)
        self.assertTrue(is_valid)

    def test_validate_travelers_count_zero(self):
        """Test zero travelers."""
        is_valid, error = validate_travelers_count(0)
        self.assertFalse(is_valid)

    def test_validate_travelers_count_too_high(self):
        """Test too many travelers."""
        is_valid, error = validate_travelers_count(101)
        self.assertFalse(is_valid)


if __name__ == '__main__':
    unittest.main()
