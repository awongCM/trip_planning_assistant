# Phase 4: Application Layer Documentation

## Overview
Phase 4 implements a robust application layer with input handling, validation, and user preferences management for the Trip Planning Assistant.

## New Modules

### 1. `config.py` - Configuration Management
Provides data models for user preferences and trip inputs.

**Key Classes:**

#### `UserPreferences`
Manages user travel preferences including:
- **Basic Info:** name, profession, home location
- **Travel Style:** luxury, comfort, budget, adventure, relaxation, cultural
- **Accommodation:** hotel, airbnb, resort, boutique, hostel
- **Interests:** lists of interests and activities
- **Special Needs:** dietary restrictions, mobility requirements, travel companions

**Usage:**
```python
from trip_planning_assistant.config import UserPreferences

# Load from JSON file
user_prefs = UserPreferences.from_file("knowledge/user_preferences.json")

# Or from text file (legacy format)
user_prefs = UserPreferences.from_file("knowledge/user_preference.txt")

# Convert to natural language prompt for agents
context = user_prefs.to_prompt_string()
```

#### `TripInputs`
Encapsulates all trip planning parameters:
- destination, origin, start_date, end_date
- budget, travelers_count
- preferences (text description)
- user_preferences (optional UserPreferences object)

**Usage:**
```python
from trip_planning_assistant.config import TripInputs

# Create from JSON string
trip = TripInputs.from_json('{"destination": "Paris", ...}')

# Convert to crew inputs
crew_inputs = trip.to_crew_inputs()
```

### 2. `utils.py` - Utility Functions
Provides validation, user interaction, and formatting functions.

**Key Functions:**

#### Validation Functions
- `validate_date_format(date_string)` - Check YYYY-MM-DD format
- `validate_trip_dates(start_date, end_date)` - Validate date range
- `validate_budget(budget)` - Check budget is reasonable ($0 - $1M)
- `validate_travelers_count(count)` - Check traveler count (1-100)

#### User Interaction
- `prompt_user_for_inputs()` - Interactive CLI input wizard
- `print_trip_summary()` - Display trip parameters nicely
- `load_user_preferences(filepath)` - Load user preferences from file

#### Output Formatting
- `format_trip_result(result)` - Format results with separators

**Usage:**
```python
from trip_planning_assistant.utils import (
    validate_trip_dates,
    prompt_user_for_inputs,
    load_user_preferences
)

# Validate inputs
is_valid, error = validate_trip_dates("2026-06-01", "2026-06-10")

# Get interactive inputs
inputs = prompt_user_for_inputs()

# Load user context
user_data = load_user_preferences()
```

### 3. `main.py` - Enhanced Entry Points
Completely refactored with improved input handling and user context.

**Available Commands:**

#### 1. `run` (default)
Runs crew with default Paris trip example + loaded user preferences
```bash
python -m trip_planning_assistant.main
# or
trip_planning_assistant
```

#### 2. `run_interactive`
Interactive CLI mode - prompts user for all trip details
```bash
run_interactive
```
Perfect for end-users who want to plan custom trips interactively.

#### 3. `run_with_trigger`
Accepts JSON payload as command argument
```bash
run_with_trigger '{"destination": "Tokyo", "budget": 8000, ...}'
```
Ideal for API/webhook integration.

#### 4. `train`
Train crew on sample data (for model improvement)
```bash
train 5 training_output.json
```

#### 5. `test`
Test crew with evaluation LLM
```bash
test 3 gpt-4
```

#### 6. `replay`
Replay execution from specific task
```bash
replay task_id_123
```

## User Preferences Files

### Format 1: JSON (Recommended)
File: `knowledge/user_preferences.json`
```json
{
  "name": "John Doe",
  "profession": "AI Engineer",
  "home_location": "San Francisco, California",
  "travel_styles": ["cultural", "adventure"],
  "interests": ["AI Agents", "museums", "hiking"],
  "accommodation_preferences": ["boutique hotels", "airbnb"],
  "dietary_restrictions": [],
  "traveling_with": "partner"
}
```

### Format 2: Simple Text (Legacy)
File: `knowledge/user_preference.txt`
```
User name is John Doe.
User is an AI Engineer.
User is interested in AI Agents.
User is based in San Francisco, California.
```

## How User Preferences Integrate

1. **Load on Startup:** User preferences are loaded automatically from `knowledge/user_preference.txt` or `knowledge/user_preferences.json`

2. **Context Injection:** Preferences are converted to natural language and injected as `user_context` in crew inputs

3. **Agent Awareness:** All agents have access to user context and can tailor recommendations based on:
   - Traveler's profession and interests
   - Travel style preferences
   - Accommodation preferences
   - Dietary and accessibility needs

4. **Personalized Output:** Results are customized for the specific user

## Example Usage

### Basic Run (Default Example)
```bash
cd trip_planning_assistant
python -m trip_planning_assistant.main
```

Output:
```
============================================================
TRIP PLANNING SUMMARY
============================================================
Destination:      Paris, France
Travel Dates:     2026-06-01 to 2026-06-10
Duration:         9 days
Travelers:        2
Budget:           $5,000.00
Per Person/Day:   $277.78
Preferences:      cultural sites, museums, fine dining, romantic experiences
============================================================

Starting trip planning assistant...
```

### Interactive Mode
```bash
run_interactive
```

Example flow:
```
Enter destination (e.g., Paris, France): Tokyo, Japan
Enter origin/departure location (e.g., New York, USA): San Francisco, USA
Enter start date (YYYY-MM-DD): 2026-07-15
Enter end date (YYYY-MM-DD): 2026-07-22
Enter total budget (USD): $3000
Number of travelers: 2
Enter travel preferences: tech sites, street food, anime culture

Proceed with trip planning? (yes/no): yes
```

### API/Webhook Integration
```bash
run_with_trigger '{"destination":"Barcelona","origin":"Madrid","start_date":"2026-05-01","end_date":"2026-05-08","budget":4000,"travelers_count":3,"preferences":"beach, nightlife, Gaudi architecture"}'
```

Returns JSON response:
```json
{
  "status": "success",
  "result": "Detailed trip plan..."
}
```

## Input Validation

All inputs are validated:
- **Dates:** Must be YYYY-MM-DD format, future dates only, logical range (max 365 days)
- **Budget:** Must be positive, reasonable limit ($0 - $1,000,000)
- **Travelers:** Must be 1-100 people
- **Preferences:** Text field (required, can be customized)

Validation errors are reported clearly to the user.

## Phase 4 Checklist
- [x] Create `config.py` with UserPreferences and TripInputs models
- [x] Create `utils.py` with validation and utility functions
- [x] Refactor `main.py` with enhanced input handling
- [x] Add interactive mode for end-users
- [x] Integrate user preferences loading and context injection
- [x] Add sample JSON user preferences file
- [x] Add input validation on all entry points
- [x] Create comprehensive documentation

## Next Steps: Phase 5
Phase 5 will focus on:
- End-to-end testing
- Error handling and logging
- API response formatting (JSON exports, PDF generation)
- Documentation and usage examples
