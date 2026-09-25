# Trip Planning Assistant Crew

Multi-agent family trip planner powered by [CrewAI](https://crewai.com). Five agents work in sequence to research a destination, draft an itinerary, estimate budget and links, and produce **`trip_plan.md`**.

## Prerequisites

- Python >=3.10, <3.14
- [UV](https://docs.astral.sh/uv/) (recommended) or `crewai install`

## Setup

1. Install dependencies:

```bash
pip install uv
uv sync
```

2. Copy environment template and add API keys:

```bash
cp .env.example .env
```

Set **`OPENAI_API_KEY`** and **`SERPER_API_KEY`** in `.env`.

3. Edit trip inputs:

- **Per trip:** `src/trip_planning_assistant/config/trip_request.yaml`
- **Family profile:** `knowledge/user_preference.txt`

## Run

```bash
uv run trip_planning_assistant
```

CLI overrides (only flags you pass replace YAML values):

```bash
uv run trip_planning_assistant --destination Kyoto --pace relaxed
```

Alternative:

```bash
crewai run
```

Note: For CLI overrides, prefer `uv run trip_planning_assistant` so arguments are passed to `main.py`.

## Output

- **`trip_plan.md`** in the project root (gitignored by default)

## Tests

```bash
uv sync
uv pip install pytest
uv run pytest
```

Unit tests cover trip input loading and validation only (no live LLM calls).

## Design docs

- Spec: `docs/superpowers/specs/2026-09-25-trip-planning-p1-design.md`
- Plan: `docs/superpowers/plans/2026-09-25-trip-planning-p1-implementation.md`

## Cost note

Each run uses OpenAI and Serper API credits; full crew runs can take several minutes.
