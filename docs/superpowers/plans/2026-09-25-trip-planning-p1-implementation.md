# Trip Planning Assistant — P1 Implementation Plan

**Date:** 2026-09-25  
**Design spec:** `docs/superpowers/specs/2026-09-25-trip-planning-p1-design.md`  
**Branch:** `cursor/trip-planning-p1-implementation-4dce` (recommended)

---

## Overview

Transform the CrewAI template into a five-agent sequential trip planner that loads family knowledge + `trip_request.yaml`, supports CLI overrides, uses Serper on research/budget agents, and writes `trip_plan.md`.

**Estimated touchpoints:** ~15 files (create 6, modify 9, delete/clear 1).

---

## Phase 0 — Prerequisites (human / local)

| Step | Action | Verify |
|------|--------|--------|
| 0.1 | Create `.env` from `.env.example` with `OPENAI_API_KEY` and `SERPER_API_KEY` | Keys non-empty |
| 0.2 | `uv sync` or `crewai install` | `uv run python -c "import crewai"` succeeds |

---

## Phase 1 — Config & inputs foundation

### Task 1.1 — `.env.example`

**File:** `.env.example` (new)

```
OPENAI_API_KEY=
SERPER_API_KEY=
# TRIP_PLANNING_LOG_LEVEL=INFO
```

**Acceptance:** README references this file.

### Task 1.2 — Trip request YAML

**Files:**

- `src/trip_planning_assistant/config/trip_request.yaml` (new) — default Tokyo smoke-test trip per spec §3
- `src/trip_planning_assistant/config/trip_request.example.yaml` (new) — copy or alias of template

**Acceptance:** Valid YAML; all required fields present.

### Task 1.3 — Family knowledge template

**File:** `knowledge/user_preference.txt` (modify)

Replace placeholder with fictional example family: dietary, pace, sleep, mobility, flight preferences, loyalty (no real PII).

**Acceptance:** Readable prose; aligns with smoke-test travelers.

### Task 1.4 — `inputs.py`

**File:** `src/trip_planning_assistant/inputs.py` (new)

Implement:

- `DEFAULT_REQUEST_PATH` → package `config/trip_request.yaml` via `importlib.resources` or path relative to package dir
- `load_yaml(path) -> dict`
- `render_travelers_summary(travelers: list) -> str`
- `validate_trip_request(data: dict) -> None` (raises `ValueError` with message)
- `merge_cli_overrides(data: dict, args: argparse.Namespace) -> dict` — only keys present in `vars(args)` that were explicitly set (use `argparse` with `default=argparse.SUPPRESS` on override flags)
- `build_kickoff_inputs(data: dict) -> dict` — flat dict + `current_year`
- `check_required_env() -> None` — `OPENAI_API_KEY`, `SERPER_API_KEY`

**Acceptance:** Unit tests cover load, validation failures, merge, summary rendering.

### Task 1.5 — Unit tests for inputs

**File:** `tests/test_inputs.py` (new)

**File:** `pyproject.toml` — add `[project.optional-dependencies] dev` or use `pytest` in dev deps if not present; document `uv run pytest`.

Cases:

- Missing required field → `ValueError`
- `end_date` before `start_date` → error
- CLI override `destination` only changes destination
- `travelers_summary` includes ages for children

**Acceptance:** `uv run pytest` passes without API keys.

---

## Phase 2 — Agents & tasks (YAML)

### Task 2.1 — `agents.yaml`

**File:** `src/trip_planning_assistant/config/agents.yaml` (replace)

Define five agents with `{destination}`, `{start_date}`, `{end_date}`, `{home_airport}`, `{budget}`, `{budget_currency}`, `{pace}`, `{interests}`, `{trip_notes}`, `{travelers_summary}` in goals/backstories where useful.

Keys: `trip_strategist`, `destination_researcher`, `itinerary_architect`, `budget_and_links_analyst`, `family_trip_editor`.

**Acceptance:** Matches spec §2 roster; no `topic` placeholder.

### Task 2.2 — `tasks.yaml`

**File:** `src/trip_planning_assistant/config/tasks.yaml` (replace)

Five tasks in order:

1. `planning_brief_task` → `trip_strategist`
2. `destination_research_task` → `destination_researcher` — instruct use Serper, cite URLs
3. `itinerary_draft_task` → `itinerary_architect`
4. `budget_and_links_task` → `budget_and_links_analyst` — Serper for link discovery
5. `finalize_trip_plan_task` → `family_trip_editor` — list all seven required headings from spec §4

Remove hardcoded “year is 2025”; reference `{start_date}` / `{end_date}`.

**Acceptance:** `output_file` only on finalize task (`trip_plan.md`).

---

## Phase 3 — Crew wiring (`crew.py`)

### Task 3.1 — Agents with tools

**File:** `src/trip_planning_assistant/crew.py` (modify)

- Replace `researcher` / `reporting_analyst` with five `@agent` methods matching YAML keys.
- Import `SerperDevTool` from `crewai_tools`.
- Attach `tools=[SerperDevTool()]` to `destination_researcher` and `budget_and_links_analyst` only.
- Replace two `@task` methods with five matching task keys.
- Remove duplicate `output_file` on reporting if only YAML sets it (keep one on finalize in code OR yaml only).

### Task 3.2 — Knowledge source

**File:** `src/trip_planning_assistant/crew.py`

Use CrewAI knowledge (per docs):

- e.g. `from crewai.knowledge.source.text_file_knowledge_source import TextFileKnowledgeSource` (verify import path for 1.7.2 at implement time)
- Point to `knowledge/user_preference.txt` (resolve path from repo root: `Path(__file__).resolve().parents[2] / "knowledge" / "user_preference.txt"` or similar)
- Pass `knowledge_sources=[...]` into `Crew(...)`

**Acceptance:** Kickoff logs show knowledge loaded; strategist references family prefs in output.

### Task 3.3 — Cleanup `__init__.py`

**File:** `src/trip_planning_assistant/__init__.py` — remove stale `LatestAiDevelopmentCrew` or export `TripPlanningAssistant` only.

---

## Phase 4 — Entry point (`main.py`)

### Task 4.1 — argparse + kickoff

**File:** `src/trip_planning_assistant/main.py` (modify)

- `parse_args()` with flags from spec §3; `--request-path` default `None` → use `DEFAULT_REQUEST_PATH`.
- `run()`: `check_required_env()` → load YAML → merge CLI → validate → `build_kickoff_inputs()` → log destination/dates → `TripPlanningAssistant().crew().kickoff(inputs=...)`
- Update `train` / `test` / `replay` / `run_with_trigger` to use trip inputs or document as unsupported in P1 (minimal: same `build_kickoff_inputs` for train/test).

**Acceptance:**

```bash
uv run trip_planning_assistant --destination Kyoto
```

Overview in `trip_plan.md` mentions Kyoto after full run.

---

## Phase 5 — Documentation & tracking

### Task 5.1 — README

**File:** `README.md` (modify)

- Purpose: family trip planning crew
- Env vars, `.env` setup
- Edit `trip_request.yaml` + example CLI
- Output: `trip_plan.md`
- Smoke test steps
- Cost note: OpenAI + Serper usage per run

### Task 5.2 — TODO.md

Check off completed phases; leave Phase 5 partial until smoke run done.

### Task 5.3 — `.gitignore`

Optional: add `trip_plan.md` if generated artifacts should not commit (P1: **commit smoke output optional** — prefer gitignore `trip_plan.md` to avoid noise).

---

## Phase 6 — Verification (manual smoke)

| # | Command / check | Expected |
|---|-----------------|----------|
| 6.1 | `uv run pytest` | All pass |
| 6.2 | `uv run trip_planning_assistant` | Completes; `trip_plan.md` exists |
| 6.3 | Section grep | All 7 headings present |
| 6.4 | `uv run trip_planning_assistant --destination Kyoto` | Overview reflects Kyoto |
| 6.5 | Unset `SERPER_API_KEY` | Clear error before kickoff |

---

## Implementation order (single PR)

```
1.1 .env.example
1.2 trip_request YAMLs
1.3 user_preference.txt
1.4 inputs.py
1.5 tests/test_inputs.py + pytest dep
2.1 agents.yaml
2.2 tasks.yaml
3.1–3.3 crew.py + __init__.py
4.1 main.py
5.1–5.3 docs/gitignore
6.x manual smoke (requires user keys)
```

---

## Risks & mitigations

| Risk | Mitigation |
|------|------------|
| CrewAI knowledge API import path differs by version | Pin 1.7.2; verify import in crew.py against installed package |
| `crewai run` may not forward CLI args | Document `uv run trip_planning_assistant`; check `[tool.crewai]` for args passthrough |
| Long/costly crew run | README notes; verbose logging |
| Serper failures | Editor task instructed to note gaps in Open questions |

---

## Out of scope (defer to P2)

- Travel APIs (Amadeus, etc.)
- `travelers` CLI override (complex structure)
- CI job with secrets for live crew test
- Web UI / database
