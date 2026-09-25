"""Integration tests for the Trip Planning Assistant."""

import unittest
import json
import tempfile
from pathlib import Path
from trip_planning_assistant.config import TripInputs, UserPreferences
from trip_planning_assistant.utils import validate_inputs
from trip_planning_assistant.exporter import TripExporter


class TestIntegration(unittest.TestCase):
    """Integration tests for core functionality."""

    def setUp(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.sample_trip = {
            'destination': 'Tokyo, Japan',
            'origin': 'San Francisco, USA',
            'start_date': '2026-07-15',
            'end_date': '2026-07-25',
            'budget': 6000,
            'travelers_count': 2,
            'preferences': 'technology museums, anime culture, local cuisine'
        }

    def tearDown(self):
        """Clean up test files."""
        import shutil
        if Path(self.temp_dir).exists():
            shutil.rmtree(self.temp_dir)

    def test_trip_inputs_with_validation(self):
        """Test creating trip inputs and validating them."""
        trip = TripInputs(**self.sample_trip)
        self.assertTrue(validate_inputs(self.sample_trip))

    def test_trip_inputs_with_user_preferences(self):
        """Test trip inputs with user preferences."""
        user_prefs = UserPreferences(
            name="Alice",
            profession="Software Engineer",
            interests=["AI", "travel", "food"],
            travel_styles=["cultural", "adventure"]
        )
        
        trip = TripInputs(user_preferences=user_prefs, **self.sample_trip)
        crew_inputs = trip.to_crew_inputs()
        
        self.assertIn('user_context', crew_inputs)
        self.assertIn('Alice', crew_inputs['user_context'])

    def test_export_workflow(self):
        """Test complete export workflow."""
        trip_plan = """
# Tokyo Trip Itinerary

## Day 1-2: Arrival & Shinjuku
- Explore Shinjuku district
- Visit teamLab Digital Art Museum

## Day 3-5: Akihabara & Technology
- Anime shops in Akihabara
- Tokyo Science Museum

## Day 6-8: Temples & Traditional
- Senso-ji Temple in Asakusa
- Traditional Japanese cuisine

## Day 9-10: Departure
- Last-minute shopping
- Depart for San Francisco
"""
        
        results = TripExporter.create_summary_report(
            self.sample_trip,
            trip_plan,
            self.temp_dir
        )
        
        # Verify all exports are created
        for format_type, file_path in results.items():
            self.assertTrue(Path(file_path).exists(), 
                          f"{format_type} export not found")

    def test_json_round_trip(self):
        """Test JSON serialization and deserialization."""
        json_data = json.dumps(self.sample_trip)
        trip = TripInputs.from_json(json_data)
        
        self.assertEqual(trip.destination, self.sample_trip['destination'])
        self.assertEqual(trip.budget, self.sample_trip['budget'])

    def test_user_preferences_integration(self):
        """Test user preferences with trip planning."""
        # Create user preferences
        user_prefs = UserPreferences(
            name="Bob",
            home_location="New York",
            profession="Photographer",
            interests=["photography", "architecture", "street food"],
            travel_styles=["cultural"],
            accommodation_preferences=["boutique hotels"]
        )
        
        # Create trip with preferences
        trip = TripInputs(user_preferences=user_prefs, **self.sample_trip)
        
        # Get crew inputs
        crew_inputs = trip.to_crew_inputs()
        
        # Verify context is properly formatted
        context = crew_inputs.get('user_context', '')
        self.assertIn('Bob', context)
        self.assertIn('photography', context)
        self.assertIn('boutique', context)

    def test_invalid_trip_dates_integration(self):
        """Test integration with invalid trip dates."""
        invalid_trip = self.sample_trip.copy()
        invalid_trip['end_date'] = '2026-07-10'  # Before start_date
        
        self.assertFalse(validate_inputs(invalid_trip))

    def test_invalid_budget_integration(self):
        """Test integration with invalid budget."""
        invalid_trip = self.sample_trip.copy()
        invalid_trip['budget'] = -1000
        
        self.assertFalse(validate_inputs(invalid_trip))


if __name__ == '__main__':
    unittest.main()
