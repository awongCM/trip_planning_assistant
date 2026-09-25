"""Load and validate trip request YAML and CLI overrides."""

from __future__ import annotations

import argparse
import logging
import os
from datetime import date, datetime
from pathlib import Path
from typing import Any

import yaml

logger = logging.getLogger(__name__)

PACKAGE_DIR = Path(__file__).resolve().parent
DEFAULT_REQUEST_PATH = PACKAGE_DIR / "config" / "trip_request.yaml"

ALLOWED_PACE = frozenset({"relaxed", "moderate", "packed"})
REQUIRED_FIELDS = (
    "destination",
    "start_date",
    "end_date",
    "home_airport",
    "budget",
    "budget_currency",
    "pace",
    "interests",
    "travelers",
)


def check_required_env() -> None:
    missing = [name for name in ("OPENAI_API_KEY", "SERPER_API_KEY") if not os.environ.get(name)]
    if missing:
        names = ", ".join(missing)
        raise RuntimeError(
            f"Missing required environment variable(s): {names}. "
            "Copy .env.example to .env and set your keys."
        )


def load_yaml(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise FileNotFoundError(f"Trip request file not found: {path}")
    with path.open(encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"Trip request YAML must be a mapping: {path}")
    return data


def render_travelers_summary(travelers: list[dict[str, Any]]) -> str:
    if not travelers:
        raise ValueError("travelers must contain at least one traveler")
    lines: list[str] = []
    for traveler in travelers:
        if not isinstance(traveler, dict):
            raise ValueError("each traveler must be a mapping")
        role = traveler.get("role")
        if not role:
            raise ValueError("each traveler must include role")
        name = traveler.get("name") or "Unnamed"
        age = traveler.get("age")
        if age is not None:
            lines.append(f"- {name} ({role}, age {age})")
        else:
            lines.append(f"- {name} ({role})")
    return "\n".join(lines)


def _parse_iso_date(value: str, field: str) -> date:
    try:
        return date.fromisoformat(str(value))
    except ValueError as exc:
        raise ValueError(f"{field} must be ISO date YYYY-MM-DD, got: {value}") from exc


def _format_interests(interests: Any) -> str:
    if isinstance(interests, str):
        return interests
    if isinstance(interests, list):
        return ", ".join(str(item) for item in interests)
    raise ValueError("interests must be a list of strings or a string")


def validate_trip_request(data: dict[str, Any]) -> None:
    for field in REQUIRED_FIELDS:
        if field not in data or data[field] in (None, ""):
            raise ValueError(f"Missing required field: {field}")

    if not isinstance(data["travelers"], list) or not data["travelers"]:
        raise ValueError("travelers must be a non-empty list")

    pace = str(data["pace"]).lower()
    if pace not in ALLOWED_PACE:
        raise ValueError(f"pace must be one of {sorted(ALLOWED_PACE)}, got: {data['pace']}")

    budget = data["budget"]
    if not isinstance(budget, (int, float)) or budget <= 0:
        raise ValueError("budget must be a number greater than 0")

    start = _parse_iso_date(data["start_date"], "start_date")
    end = _parse_iso_date(data["end_date"], "end_date")
    if end < start:
        raise ValueError("end_date must be on or after start_date")

    render_travelers_summary(data["travelers"])
    _format_interests(data["interests"])


def load_trip_request(path: Path | None = None) -> dict[str, Any]:
    request_path = path or DEFAULT_REQUEST_PATH
    data = load_yaml(request_path)
    if "trip_notes" not in data or data["trip_notes"] is None:
        data["trip_notes"] = ""
    validate_trip_request(data)
    return data


def merge_cli_overrides(data: dict[str, Any], args: argparse.Namespace) -> dict[str, Any]:
    merged = dict(data)
    if hasattr(args, "destination"):
        merged["destination"] = args.destination
    if hasattr(args, "start_date"):
        merged["start_date"] = args.start_date
    if hasattr(args, "end_date"):
        merged["end_date"] = args.end_date
    if hasattr(args, "home_airport"):
        merged["home_airport"] = args.home_airport
    if hasattr(args, "budget"):
        merged["budget"] = args.budget
    if hasattr(args, "budget_currency"):
        merged["budget_currency"] = args.budget_currency
    if hasattr(args, "pace"):
        merged["pace"] = args.pace
    if hasattr(args, "interests"):
        merged["interests"] = [s.strip() for s in args.interests.split(",") if s.strip()]
    if hasattr(args, "trip_notes"):
        merged["trip_notes"] = args.trip_notes
    validate_trip_request(merged)
    return merged


def build_kickoff_inputs(data: dict[str, Any]) -> dict[str, str]:
    return {
        "destination": str(data["destination"]),
        "start_date": str(data["start_date"]),
        "end_date": str(data["end_date"]),
        "home_airport": str(data["home_airport"]),
        "budget": str(data["budget"]),
        "budget_currency": str(data["budget_currency"]),
        "pace": str(data["pace"]).lower(),
        "interests": _format_interests(data["interests"]),
        "trip_notes": str(data.get("trip_notes") or ""),
        "travelers_summary": render_travelers_summary(data["travelers"]),
        "current_year": str(datetime.now().year),
    }


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Family trip planning crew")
    parser.add_argument(
        "--request-path",
        type=Path,
        default=argparse.SUPPRESS,
        help=f"Path to trip request YAML (default: {DEFAULT_REQUEST_PATH})",
    )
    parser.add_argument("--destination", default=argparse.SUPPRESS)
    parser.add_argument("--start-date", dest="start_date", default=argparse.SUPPRESS)
    parser.add_argument("--end-date", dest="end_date", default=argparse.SUPPRESS)
    parser.add_argument("--home-airport", dest="home_airport", default=argparse.SUPPRESS)
    parser.add_argument("--budget", type=float, default=argparse.SUPPRESS)
    parser.add_argument("--budget-currency", dest="budget_currency", default=argparse.SUPPRESS)
    parser.add_argument("--pace", choices=sorted(ALLOWED_PACE), default=argparse.SUPPRESS)
    parser.add_argument(
        "--interests",
        help="Comma-separated interests (overrides YAML list)",
        default=argparse.SUPPRESS,
    )
    parser.add_argument("--trip-notes", dest="trip_notes", default=argparse.SUPPRESS)
    return parser.parse_args(argv)


def resolve_request_path(args: argparse.Namespace) -> Path:
    if hasattr(args, "request_path"):
        return args.request_path
    return DEFAULT_REQUEST_PATH


def load_merged_trip_request(args: argparse.Namespace) -> dict[str, Any]:
    path = resolve_request_path(args)
    data = load_trip_request(path)
    return merge_cli_overrides(data, args)
