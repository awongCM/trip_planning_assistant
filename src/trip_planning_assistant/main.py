#!/usr/bin/env python
import json
import logging
import os
import sys
import warnings
from datetime import datetime

from dotenv import load_dotenv

from trip_planning_assistant.crew import TripPlanningAssistant
from trip_planning_assistant.inputs import (
    build_kickoff_inputs,
    check_required_env,
    load_merged_trip_request,
    load_trip_request,
    parse_args,
)

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

load_dotenv()


def _configure_logging() -> None:
    level_name = os.environ.get("TRIP_PLANNING_LOG_LEVEL", "INFO").upper()
    level = getattr(logging, level_name, logging.INFO)
    logging.basicConfig(level=level, format="%(levelname)s %(name)s: %(message)s")


def _kickoff_inputs_from_args(argv: list[str] | None = None) -> dict[str, str]:
    args = parse_args(argv)
    trip_request = load_merged_trip_request(args)
    return build_kickoff_inputs(trip_request)


def run(argv: list[str] | None = None):
    """Run the crew."""
    _configure_logging()
    check_required_env()
    inputs = _kickoff_inputs_from_args(argv)
    logging.getLogger(__name__).info(
        "Starting trip plan for %s (%s to %s)",
        inputs["destination"],
        inputs["start_date"],
        inputs["end_date"],
    )
    try:
        TripPlanningAssistant().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise RuntimeError(f"An error occurred while running the crew: {e}") from e


def train():
    """Train the crew for a given number of iterations."""
    _configure_logging()
    check_required_env()
    inputs = build_kickoff_inputs(load_trip_request())
    try:
        TripPlanningAssistant().crew().train(
            n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs
        )
    except Exception as e:
        raise RuntimeError(f"An error occurred while training the crew: {e}") from e


def replay():
    """Replay the crew execution from a specific task."""
    _configure_logging()
    check_required_env()
    try:
        TripPlanningAssistant().crew().replay(task_id=sys.argv[1])
    except Exception as e:
        raise RuntimeError(f"An error occurred while replaying the crew: {e}") from e


def test():
    """Test the crew execution and returns the results."""
    _configure_logging()
    check_required_env()
    inputs = build_kickoff_inputs(load_trip_request())
    inputs["current_year"] = str(datetime.now().year)
    try:
        TripPlanningAssistant().crew().test(
            n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs
        )
    except Exception as e:
        raise RuntimeError(f"An error occurred while testing the crew: {e}") from e


def run_with_trigger():
    """Run the crew with trigger payload."""
    if len(sys.argv) < 2:
        raise RuntimeError("No trigger payload provided. Please provide JSON payload as argument.")

    try:
        trigger_payload = json.loads(sys.argv[1])
    except json.JSONDecodeError:
        raise RuntimeError("Invalid JSON payload provided as argument")

    _configure_logging()
    check_required_env()
    base_inputs = build_kickoff_inputs(load_trip_request())
    base_inputs["crewai_trigger_payload"] = trigger_payload

    try:
        return TripPlanningAssistant().crew().kickoff(inputs=base_inputs)
    except Exception as e:
        raise RuntimeError(f"An error occurred while running the crew with trigger: {e}") from e
