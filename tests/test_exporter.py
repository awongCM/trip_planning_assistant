"""Unit tests for exporter module."""

import unittest
import json
from pathlib import Path
import tempfile
from trip_planning_assistant.exporter import TripExporter


class TestTripExporter(unittest.TestCase):
    """Test TripExporter functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.trip_plan = "Day 1: Arrive in Paris\nDay 2: Visit Eiffel Tower"
        self.trip_params = {
            'destination': 'Paris',
            'origin': 'New York',
            'start_date': '2026-06-01',
            'end_date': '2026-06-10',
            'budget': 5000,
            'travelers_count': 2,
            'preferences': 'cultural sites'
        }

    def tearDown(self):
        """Clean up test files."""
        import shutil
        if Path(self.temp_dir).exists():
            shutil.rmtree(self.temp_dir)

    def test_export_to_json(self):
        """Test JSON export."""
        output_file = f"{self.temp_dir}/test_output.json"
        result = TripExporter.export_to_json(
            {"trip": self.trip_plan},
            output_file
        )
        
        self.assertTrue(Path(result).exists())
        
        with open(result, 'r') as f:
            data = json.load(f)
        self.assertIn('trip', data)

    def test_export_to_markdown(self):
        """Test Markdown export."""
        output_file = f"{self.temp_dir}/test_output.md"
        result = TripExporter.export_to_markdown(
            self.trip_plan,
            output_file
        )
        
        self.assertTrue(Path(result).exists())
        
        with open(result, 'r') as f:
            content = f.read()
        self.assertIn(self.trip_plan, content)
        self.assertIn('#', content)

    def test_export_to_html(self):
        """Test HTML export."""
        output_file = f"{self.temp_dir}/test_output.html"
        result = TripExporter.export_to_html(
            self.trip_plan,
            output_file
        )
        
        self.assertTrue(Path(result).exists())
        
        with open(result, 'r') as f:
            content = f.read()
        self.assertIn('<!DOCTYPE html>', content)
        self.assertIn(self.trip_plan, content)

    def test_export_to_csv(self):
        """Test CSV export."""
        data = [
            {'day': 1, 'activity': 'Arrive', 'location': 'Paris'},
            {'day': 2, 'activity': 'Sightseeing', 'location': 'Eiffel Tower'}
        ]
        output_file = f"{self.temp_dir}/test_output.csv"
        result = TripExporter.export_to_csv(data, output_file)
        
        self.assertTrue(Path(result).exists())
        
        with open(result, 'r') as f:
            content = f.read()
        self.assertIn('day', content)
        self.assertIn('activity', content)

    def test_export_to_csv_invalid_data(self):
        """Test CSV export with invalid data."""
        with self.assertRaises(ValueError):
            TripExporter.export_to_csv([], f"{self.temp_dir}/test.csv")

    def test_create_summary_report(self):
        """Test creating comprehensive summary report."""
        results = TripExporter.create_summary_report(
            self.trip_params,
            self.trip_plan,
            self.temp_dir
        )
        
        self.assertIn('markdown', results)
        self.assertIn('html', results)
        self.assertIn('json', results)
        
        # Verify all files exist
        for file_path in results.values():
            self.assertTrue(Path(file_path).exists())

    def test_json_export_without_filename(self):
        """Test JSON export with auto-generated filename."""
        result = TripExporter.export_to_json(
            {"test": "data"},
            None
        )
        
        self.assertTrue(Path(result).exists())
        self.assertIn('.json', result)

    def test_markdown_export_without_filename(self):
        """Test Markdown export with auto-generated filename."""
        result = TripExporter.export_to_markdown(
            self.trip_plan,
            None
        )
        
        self.assertTrue(Path(result).exists())
        self.assertIn('.md', result)


if __name__ == '__main__':
    unittest.main()
