"""Unit tests for config module."""

import unittest
import json
from pathlib import Path
import tempfile
from trip_planning_assistant.config import (
    UserPreferences,
    TripInputs,
    TravelStyle,
    AccommodationPreference
)


class TestUserPreferences(unittest.TestCase):
    """Test UserPreferences dataclass."""

    def test_user_preferences_creation(self):
        """Test creating a UserPreferences instance."""
        prefs = UserPreferences(
            name="John Doe",
            profession="Engineer",
            home_location="San Francisco"
        )
        
        self.assertEqual(prefs.name, "John Doe")
        self.assertEqual(prefs.profession, "Engineer")
        self.assertEqual(prefs.home_location, "San Francisco")

    def test_user_preferences_defaults(self):
        """Test UserPreferences default values."""
        prefs = UserPreferences(name="Jane")
        
        self.assertEqual(prefs.travel_styles, [])
        self.assertEqual(prefs.interests, [])
        self.assertIsNone(prefs.profession)

    def test_to_dict(self):
        """Test converting UserPreferences to dictionary."""
        prefs = UserPreferences(
            name="John",
            interests=["hiking", "museums"]
        )
        
        d = prefs.to_dict()
        self.assertIsInstance(d, dict)
        self.assertEqual(d['name'], "John")
        self.assertEqual(d['interests'], ["hiking", "museums"])

    def test_to_prompt_string(self):
        """Test converting UserPreferences to prompt string."""
        prefs = UserPreferences(
            name="John Doe",
            profession="Engineer",
            interests=["AI", "travel"]
        )
        
        prompt = prefs.to_prompt_string()
        self.assertIn("John Doe", prompt)
        self.assertIn("Engineer", prompt)
        self.assertIn("AI", prompt)

    def test_from_json_file(self):
        """Test loading UserPreferences from JSON file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump({
                "name": "Alice",
                "profession": "Doctor",
                "interests": ["medicine", "travel"]
            }, f)
            temp_file = f.name
        
        try:
            prefs = UserPreferences.from_file(temp_file)
            self.assertEqual(prefs.name, "Alice")
            self.assertEqual(prefs.profession, "Doctor")
            self.assertIn("medicine", prefs.interests)
        finally:
            Path(temp_file).unlink()

    def test_from_text_file(self):
        """Test loading UserPreferences from text file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write("User name is Bob.\n")
            f.write("User is based in New York.\n")
            temp_file = f.name
        
        try:
            prefs = UserPreferences.from_file(temp_file)
            self.assertEqual(prefs.name, "Bob")
            self.assertEqual(prefs.home_location, "New York")
        finally:
            Path(temp_file).unlink()

    def test_file_not_found(self):
        """Test error handling for missing file."""
        with self.assertRaises(FileNotFoundError):
            UserPreferences.from_file("nonexistent_file.json")


class TestTripInputs(unittest.TestCase):
    """Test TripInputs dataclass."""

    def setUp(self):
        """Set up test data."""
        self.trip_data = {
            'destination': 'Paris',
            'origin': 'New York',
            'start_date': '2026-06-01',
            'end_date': '2026-06-10',
            'budget': 5000,
            'travelers_count': 2,
            'preferences': 'cultural sites'
        }

    def test_trip_inputs_creation(self):
        """Test creating a TripInputs instance."""
        trip = TripInputs(**self.trip_data)
        
        self.assertEqual(trip.destination, 'Paris')
        self.assertEqual(trip.budget, 5000)

    def test_to_crew_inputs(self):
        """Test converting TripInputs to crew inputs."""
        trip = TripInputs(**self.trip_data)
        crew_inputs = trip.to_crew_inputs()
        
        self.assertIn('destination', crew_inputs)
        self.assertEqual(crew_inputs['destination'], 'Paris')

    def test_from_json(self):
        """Test loading TripInputs from JSON string."""
        json_str = json.dumps(self.trip_data)
        trip = TripInputs.from_json(json_str)
        
        self.assertEqual(trip.destination, 'Paris')
        self.assertEqual(trip.budget, 5000)

    def test_from_json_invalid(self):
        """Test error handling for invalid JSON."""
        with self.assertRaises(json.JSONDecodeError):
            TripInputs.from_json("invalid json")


if __name__ == '__main__':
    unittest.main()
