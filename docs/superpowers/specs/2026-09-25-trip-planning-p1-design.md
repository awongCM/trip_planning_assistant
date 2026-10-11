# Trip Planning Assistant — P1 Design

**Date:** 2026-09-25  
**Status:** Approved in brainstorming (Sections 1–4)  
**Scope:** Planning-only MVP — multi-agent crew produces `trip_plan.md` (no travel APIs, no booking).

---

## 1. Goals & scope

### Goals (P1)

- From one command (`crewai run` or `uv run trip_planning_assistant`), produce **`trip_plan.md`** for a trip described in `src/trip_planning_assistant/config/trip_request.yaml`, with CLI flags overriding YAML fields when explicitly provided.
- Agents use **family knowledge** (`knowledge/user_preference.txt`), **per-trip YAML**, and **Serper web search** on research/budget agents so the plan is grounded and family-aware.
- Final document includes: trip overview, family fit & logistics, day-by-day itinerary, budget estimate, packing & health, links & sources, open questions & next steps.

### Non-goals (P1)

- No flight/hotel/travel APIs, payments, or confirmed bookings.
- No web UI, database, or user accounts.
- No email/Slack notifications.
- No automated multi-destination comparison (single primary `destination` in schema; comparisons only as prose if noted in `trip_notes`).

### Environment

| Variable | Required | Purpose |
|----------|----------|---------|
| `OPENAI_API_KEY` | Yes | CrewAI LLM backend |
| `SERPER_API_KEY` | Yes | `SerperDevTool` for web search |
| `TRIP_PLANNING_LOG_LEVEL` | No | Default `INFO`; optional `DEBUG` |

- **`.env.example`** documents required keys (no secrets in git).
- **Fail fast** before `kickoff` if required env vars are missing.

### Implementation approach (selected)

**Extend the current CrewAI YAML crew (Approach 1):** `@CrewBase` in `crew.py`, five agents/tasks in YAML, Serper on research and budget agents, CrewAI knowledge from `user_preference.txt`, YAML + CLI merge in `main.py`, final task writes `trip_plan.md`.

Not in P1: hierarchical manager process; full intermediate artifact pipeline (optional `itinerary_draft` file only if debugging needs it during implementation).

### Repo cleanup (in scope)

- Remove or replace stale `LatestAiDevelopmentCrew` in `src/trip_planning_assistant/__init__.py`.
- Update `README.md` and `TODO.md` for P1 behavior.
- Remove `topic: AI LLMs` / `report.md` demo behavior from `main.py`.

---

## 2. Agent roster & task pipeline

**Process:** `Process.sequential`. Task outputs flow as context to subsequent tasks.

**Crew knowledge:** Attach `knowledge/user_preference.txt` via CrewAI knowledge API on the `Crew` in `crew.py`.

```
trip_request.yaml + CLI overrides
         │
         ▼
┌────────────────────┐
│ 1. trip_strategist │  Planning brief
└─────────┬──────────┘
          ▼
┌────────────────────┐     Serper
│ 2. destination_    │◄───────┐
│    researcher      │        │
└─────────┬──────────┘        │
          ▼                   │
┌────────────────────┐        │
│ 3. itinerary_      │  (no tools in P1)
│    architect       │
└─────────┬──────────┘
          ▼
┌────────────────────┐     Serper
│ 4. budget_and_     │◄───────┐
│    links_analyst   │        │
└─────────┬──────────┘
          ▼
┌────────────────────┐
│ 5. family_trip_    │  No tools — unify → trip_plan.md
│    editor          │
└─────────┬──────────┘
          ▼
     trip_plan.md
```

### Agents (`agents.yaml` keys)

| Key | Role | Responsibility |
|-----|------|----------------|
| `trip_strategist` | Trip strategist | Merge family knowledge + trip request into a planning brief: goals, constraints, pace, budget, traveler needs. |
| `destination_researcher` | Destination researcher | Grounded destination research for trip dates: areas, weather, events, family activities, transport basics. |
| `itinerary_architect` | Itinerary architect | Day-by-day schedule from brief + research; realistic pacing and transit. |
| `budget_and_links_analyst` | Budget & links analyst | Cost breakdown and actionable search/booking *links* (no purchases). |
| `family_trip_editor` | Family trip editor | Final `trip_plan.md`; enforce sections; resolve contradictions; strengthen family logistics. |

### Tasks (`tasks.yaml` keys, order)

| Task key | Agent | Output |
|----------|--------|--------|
| `planning_brief_task` | `trip_strategist` | Markdown planning brief |
| `destination_research_task` | `destination_researcher` | Research memo with URLs from Serper |
| `itinerary_draft_task` | `itinerary_architect` | Day-by-day itinerary markdown |
| `budget_and_links_task` | `budget_and_links_analyst` | Budget table + categorized links |
| `finalize_trip_plan_task` | `family_trip_editor` | **`trip_plan.md`** (sole `output_file`) |

### Tools

- **`SerperDevTool`:** `destination_researcher`, `budget_and_links_analyst`.
- All other agents: no tools in P1.

### Kickoff interpolation

Python builds `inputs` dict for `kickoff(inputs=...)`:

- From merged trip request: `destination`, `start_date`, `end_date`, `home_airport`, `budget`, `budget_currency`, `pace`, `interests`, `trip_notes`, `travelers_summary`.
- `current_year` from runtime (tasks must use trip dates, not a hardcoded year in YAML).

---

## 3. Trip request schema & CLI

### Files

| Path | Purpose |
|------|---------|
| `src/trip_planning_assistant/config/trip_request.yaml` | Default trip for runs and smoke test |
| `src/trip_planning_assistant/config/trip_request.example.yaml` | Committed template (optional duplicate of default) |
| `knowledge/user_preference.txt` | Long-lived family profile (not CLI-overridden in P1) |

### Loader

- Module `trip_planning_assistant/inputs.py`: `load_trip_request(path) -> dict`, validation, `travelers_summary` rendering.

### Required YAML fields

| Field | Type | Notes |
|-------|------|--------|
| `destination` | string | Single primary focus |
| `start_date` | `YYYY-MM-DD` | |
| `end_date` | `YYYY-MM-DD` | Must be ≥ `start_date` |
| `home_airport` | string | IATA or free text |
| `budget` | number | > 0 |
| `budget_currency` | string | e.g. `USD` |
| `pace` | string | `relaxed` \| `moderate` \| `packed` |
| `interests` | list[string] | |
| `travelers` | list[object] | Each: `role` required; `name`, `age` optional (age recommended for children) |
| `trip_notes` | string | Optional, default `""` |

### CLI (`argparse` in `main.py`)

All flags optional; **only override YAML when the flag is explicitly passed** (no argparse defaults that erase YAML).

| Flag | YAML key |
|------|----------|
| `--request-path` | Alternate YAML path |
| `--destination` | `destination` |
| `--start-date` | `start_date` |
| `--end-date` | `end_date` |
| `--home-airport` | `home_airport` |
| `--budget` | `budget` |
| `--budget-currency` | `budget_currency` |
| `--pace` | `pace` |
| `--interests` | Comma-separated → list |
| `--trip-notes` | `trip_notes` |

### Pre-kickoff validation

- Required fields after merge; date order; `pace` enum; `budget > 0`.
- Missing env vars vs invalid YAML vs bad dates — distinct error messages.

---

## 4. Output, errors, testing

### `trip_plan.md` required headings

1. `# Trip overview`
2. `## Family fit & logistics`
3. `## Day-by-day itinerary` (subsections `### Day N — <weekday, date>`)
4. `## Budget estimate`
5. `## Packing & health`
6. `## Links & sources`
7. `## Open questions & next steps`

Editor task instructions: markdown only; no “already booked” claims; use “search”, “verify availability”, “consider”.

**Output location:** project root (`trip_plan.md`).

### Error handling

| Case | Behavior |
|------|----------|
| Missing API keys | Exit before crew; point to `.env.example` |
| Invalid trip input | Exit before kickoff; field-level errors |
| Crew/runtime failure | Log and exit non-zero |
| Thin Serper data | Editor notes gaps under Open questions |

### Logging

- `logging` in `main.py` and `inputs.py`; level from `TRIP_PLANNING_LOG_LEVEL` (default INFO).
- Crew/agents remain `verbose=True`.

### Smoke test (P1 complete)

1. Valid `.env` with OpenAI + Serper.
2. `uv sync` / `crewai install`.
3. `uv run trip_planning_assistant`.
4. `trip_plan.md` exists with all seven sections.
5. CLI override smoke: `--destination Kyoto` reflected in overview.

### Automated tests

- **Unit tests** for `inputs.py` only (load, merge, validation, `travelers_summary`) — no live LLM in CI.
- Manual full crew run documented in README.

---

## 5. Dependencies & stack

- Existing: `crewai[tools]==1.7.2`, UV, Python `>=3.10,<3.14`.
- Serper via `crewai_tools.SerperDevTool` (included in tools extra).

---

## 6. Brainstorming decisions log

| Question | Choice |
|----------|--------|
| P1 outcome | A — `trip_plan.md`, no travel APIs |
| Research | A — Serper required |
| Trip inputs | A + C — YAML + CLI overrides |
| Family prefs | A — knowledge file + per-trip YAML |
| Crew size | C — 5 agents sequential |
| Document style | B — family-focused pack |
