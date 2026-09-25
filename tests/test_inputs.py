from pathlib import Path

import pytest

from trip_planning_assistant.inputs import (
    build_kickoff_inputs,
    load_trip_request,
    merge_cli_overrides,
    parse_args,
    render_travelers_summary,
    validate_trip_request,
)


def test_render_travelers_summary_includes_child_age():
    summary = render_travelers_summary(
        [{"role": "adult", "name": "A"}, {"role": "child", "name": "B", "age": 8}]
    )
    assert "age 8" in summary
    assert "A" in summary


def test_validate_rejects_end_before_start():
    data = {
        "destination": "Tokyo",
        "start_date": "2026-04-20",
        "end_date": "2026-04-10",
        "home_airport": "SFO",
        "budget": 1000,
        "budget_currency": "USD",
        "pace": "moderate",
        "interests": ["food"],
        "travelers": [{"role": "adult"}],
    }
    with pytest.raises(ValueError, match="end_date"):
        validate_trip_request(data)


def test_cli_override_destination_only():
    data = {
        "destination": "Tokyo",
        "start_date": "2026-04-10",
        "end_date": "2026-04-20",
        "home_airport": "SFO",
        "budget": 12000,
        "budget_currency": "USD",
        "pace": "moderate",
        "interests": ["food"],
        "travelers": [{"role": "adult"}],
        "trip_notes": "",
    }
    args = parse_args(["--destination", "Kyoto"])
    merged = merge_cli_overrides(data, args)
    assert merged["destination"] == "Kyoto"
    assert merged["start_date"] == "2026-04-10"


def test_load_default_trip_request():
    data = load_trip_request()
    assert data["destination"] == "Tokyo"
    inputs = build_kickoff_inputs(data)
    assert "food" in inputs["interests"]
    assert inputs["pace"] == "moderate"


def test_missing_required_field():
    with pytest.raises(ValueError, match="Missing required field"):
        validate_trip_request({"destination": "X"})


def test_example_yaml_exists():
    example = Path(__file__).resolve().parents[1] / "src/trip_planning_assistant/config/trip_request.example.yaml"
    assert example.is_file()
