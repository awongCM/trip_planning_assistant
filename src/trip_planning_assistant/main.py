#!/usr/bin/env python
import sys
import warnings
import json
from datetime import datetime
from pathlib import Path

from trip_planning_assistant.crew import TripPlanningAssistant
from trip_planning_assistant.config import UserPreferences, TripInputs
from trip_planning_assistant.utils import (
    validate_trip_dates,
    validate_budget,
    validate_travelers_count,
    print_trip_summary,
    prompt_user_for_inputs,
    load_user_preferences,
    format_trip_result
)

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


def get_default_inputs() -> dict:
    """Return default trip planning inputs."""
    return {
        'destination': 'Paris, France',
        'origin': 'New York (JFK)',
        'start_date': '2026-06-01',
        'end_date': '2026-06-10',
        'budget': 5000,
        'travelers_count': 2,
        'preferences': 'cultural sites, museums, fine dining, romantic experiences'
    }


def validate_inputs(inputs: dict) -> bool:
    """Validate trip planning inputs."""
    required_fields = ['destination', 'origin', 'start_date', 'end_date', 'budget', 'travelers_count', 'preferences']
    
    for field in required_fields:
        if field not in inputs:
            print(f"Error: Missing required field '{field}'")
            return False
    
    is_valid, error_msg = validate_trip_dates(inputs['start_date'], inputs['end_date'])
    if not is_valid:
        print(f"Error: {error_msg}")
        return False
    
    is_valid, error_msg = validate_budget(inputs['budget'])
    if not is_valid:
        print(f"Error: {error_msg}")
        return False
    
    is_valid, error_msg = validate_travelers_count(inputs['travelers_count'])
    if not is_valid:
        print(f"Error: {error_msg}")
        return False
    
    return True


def run():
    """
    Run the crew with trip planning inputs.
    Uses default inputs or prompt user for input.
    """
    try:
        inputs = get_default_inputs()
        
        user_prefs_data = load_user_preferences()
        if user_prefs_data:
            inputs['user_context'] = user_prefs_data['user_context']
        
        print_trip_summary(
            inputs['destination'],
            inputs['start_date'],
            inputs['end_date'],
            inputs['budget'],
            inputs['travelers_count'],
            inputs['preferences']
        )
        
        if not validate_inputs(inputs):
            sys.exit(1)
        
        print("Starting trip planning assistant...\n")
        result = TripPlanningAssistant().crew().kickoff(inputs=inputs)
        
        print(format_trip_result(str(result)))
        
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


def train():
    """
    Train the crew for a given number of iterations.
    """
    if len(sys.argv) < 3:
        raise Exception("Usage: train <iterations> <output_file>")
    
    try:
        inputs = get_default_inputs()
        
        user_prefs_data = load_user_preferences()
        if user_prefs_data:
            inputs['user_context'] = user_prefs_data['user_context']
        
        if not validate_inputs(inputs):
            sys.exit(1)
        
        print(f"Training crew for {sys.argv[1]} iterations...")
        TripPlanningAssistant().crew().train(
            n_iterations=int(sys.argv[1]),
            filename=sys.argv[2],
            inputs=inputs
        )
        print(f"Training complete. Results saved to {sys.argv[2]}")

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")


def replay():
    """
    Replay the crew execution from a specific task.
    """
    if len(sys.argv) < 2:
        raise Exception("Usage: replay <task_id>")
    
    try:
        print(f"Replaying from task: {sys.argv[1]}")
        TripPlanningAssistant().crew().replay(task_id=sys.argv[1])
    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")


def test():
    """
    Test the crew execution and returns the results.
    """
    if len(sys.argv) < 3:
        raise Exception("Usage: test <iterations> <eval_llm>")
    
    try:
        inputs = get_default_inputs()
        
        user_prefs_data = load_user_preferences()
        if user_prefs_data:
            inputs['user_context'] = user_prefs_data['user_context']
        
        if not validate_inputs(inputs):
            sys.exit(1)
        
        print(f"Testing crew with {sys.argv[1]} iterations using {sys.argv[2]}...")
        TripPlanningAssistant().crew().test(
            n_iterations=int(sys.argv[1]),
            eval_llm=sys.argv[2],
            inputs=inputs
        )

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")


def run_with_trigger():
    """
    Run the crew with trigger payload.
    Payload should be JSON with trip planning parameters.
    """
    if len(sys.argv) < 2:
        raise Exception("Usage: run_with_trigger '<json_payload>'")
    
    try:
        trigger_payload = json.loads(sys.argv[1])
    except json.JSONDecodeError:
        raise Exception("Invalid JSON payload provided as argument")
    
    try:
        inputs = {
            'destination': trigger_payload.get('destination', 'Paris, France'),
            'origin': trigger_payload.get('origin', 'New York (JFK)'),
            'start_date': trigger_payload.get('start_date', '2026-06-01'),
            'end_date': trigger_payload.get('end_date', '2026-06-10'),
            'budget': trigger_payload.get('budget', 5000),
            'travelers_count': trigger_payload.get('travelers_count', 2),
            'preferences': trigger_payload.get('preferences', 'cultural sites, museums, fine dining')
        }
        
        user_prefs_data = load_user_preferences()
        if user_prefs_data:
            inputs['user_context'] = user_prefs_data['user_context']
        
        if not validate_inputs(inputs):
            return {"error": "Invalid inputs provided", "inputs": inputs}
        
        print_trip_summary(
            inputs['destination'],
            inputs['start_date'],
            inputs['end_date'],
            inputs['budget'],
            inputs['travelers_count'],
            inputs['preferences']
        )
        
        result = TripPlanningAssistant().crew().kickoff(inputs=inputs)
        return {
            "status": "success",
            "result": str(result)
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }


def run_interactive():
    """
    Run the crew with interactive user input prompts.
    """
    try:
        inputs = prompt_user_for_inputs()
        
        user_prefs_data = load_user_preferences()
        if user_prefs_data:
            inputs['user_context'] = user_prefs_data['user_context']
        
        print_trip_summary(
            inputs['destination'],
            inputs['start_date'],
            inputs['end_date'],
            inputs['budget'],
            inputs['travelers_count'],
            inputs['preferences']
        )
        
        if not validate_inputs(inputs):
            sys.exit(1)
        
        confirm = input("Proceed with trip planning? (yes/no): ").strip().lower()
        if confirm not in ['yes', 'y']:
            print("Trip planning cancelled.")
            return
        
        print("\nStarting trip planning assistant...\n")
        result = TripPlanningAssistant().crew().kickoff(inputs=inputs)
        
        print(format_trip_result(str(result)))
        
    except KeyboardInterrupt:
        print("\n\nTrip planning cancelled by user.")
        sys.exit(0)
    except Exception as e:
        raise Exception(f"An error occurred during interactive mode: {e}")

