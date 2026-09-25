# Trip Planning Assistant - AI-Powered Travel Planner

A multi-agent AI system powered by [CrewAI](https://crewai.com) that automatically plans comprehensive trips with flights, hotels, itineraries, and personalized recommendations.

## 🌍 Features

### Core Capabilities
✅ **Flight Search Automation** - Find cheapest flights via real-time SerpAPI data  
✅ **Hotel Recommendations** - Search and filter hotels by budget, amenities, ratings  
✅ **Weather Integration** - Get destination weather forecasts  
✅ **Real-Time Currency Conversion** - Convert budgets and costs  
✅ **AI-Powered Itinerary** - Generate day-by-day travel plans with attractions & dining  
✅ **User Preferences** - Personalize recommendations based on traveler profile  
✅ **Multi-Format Export** - Save plans as JSON, HTML, Markdown, CSV  
✅ **Comprehensive Logging** - Debug and monitor execution  
✅ **Full Test Coverage** - 40+ passing unit tests  

### Technology Stack
- **Framework:** [CrewAI 1.7.2](https://crewai.com) - Multi-agent orchestration
- **LLM:** OpenAI (GPT-4/GPT-3.5)
- **APIs:** SerpAPI for flights, hotels, weather
- **Language:** Python 3.10-3.13
- **Testing:** unittest framework
- **Logging:** Built-in Python logging

## 📋 Requirements

- Python >=3.10, <3.14
- [UV](https://docs.astral.sh/uv/) (recommended) or pip
- OpenAI API key
- SerpAPI key (optional, for real-time data)

## 🚀 Quick Start

### 1. Installation

```bash
# Clone the repository
git clone <repo>
cd trip_planning_assistant

# Install dependencies
pip install -e .
# OR with UV:
uv pip install -e .
```

### 2. Environment Setup

Create `.env` file:
```bash
OPENAI_API_KEY=sk-your-api-key-here
SERPAPI_API_KEY=your-serpapi-key-here  # Optional
```

### 3. Run the Assistant

```bash
# Default mode (example: Paris trip)
python -m trip_planning_assistant.main

# Interactive mode (answer prompts)
run_interactive

# With JSON payload
run_with_trigger '{"destination":"Tokyo","budget":8000,"start_date":"2026-07-15","end_date":"2026-07-25","travelers_count":2,"preferences":"tech museums, anime"}'
```

## 📖 Usage Guide

### Default Mode
Runs with pre-configured example trip (Paris for 2 travelers, $5000 budget):

```bash
trip_planning_assistant
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
[CrewAI agents execute and generate itinerary]
```

### Interactive Mode
Prompts user for all trip details:

```bash
run_interactive

# Follow prompts:
Enter destination: Tokyo, Japan
Enter origin: San Francisco, USA
Enter start date (YYYY-MM-DD): 2026-07-15
Enter end date (YYYY-MM-DD): 2026-07-25
Enter total budget (USD): $6000
Number of travelers: 2
Enter travel preferences: tech museums, anime culture, street food

Proceed with trip planning? (yes/no): yes
```

### API/Trigger Mode
For webhook/API integration:

```bash
run_with_trigger '{"destination":"Barcelona","origin":"Madrid","start_date":"2026-05-01","end_date":"2026-05-08","budget":4000,"travelers_count":3,"preferences":"beach, nightlife, Gaudi architecture"}'
```

Returns JSON response:
```json
{
  "status": "success",
  "result": "Comprehensive trip plan with flights, hotels, itinerary..."
}
```

## 🤖 Multi-Agent System

The crew consists of 5 specialized AI agents:

### 1. **Destination Researcher** 🔍
- Analyzes destination climate, culture, and attractions
- Checks visa requirements and safety ratings
- Integrates weather data for planned dates

**Tools:** WeatherTool, LLM reasoning

### 2. **Flight Searcher** ✈️
- Searches real-time flights via SerpAPI
- Filters by price, duration, layovers
- Ranks flights by cost-effectiveness

**Tools:** FlightSearchTool

### 3. **Hotel Finder** 🏨
- Searches real-time hotel availability
- Filters by budget, amenities, location
- Analyzes guest ratings and reviews

**Tools:** HotelSearchTool

### 4. **Currency Converter** 💱
- Provides real-time exchange rates
- Breaks down budget by category
- Suggests cost-saving options

**Tools:** CurrencyConversionTool

### 5. **Itinerary Builder** 📅
- Creates day-by-day detailed schedule
- Recommends must-visit attractions
- Suggests local restaurants and transport
- Balances activities with rest periods

**Tools:** LLM reasoning with structured output

## 📁 Project Structure

```
trip_planning_assistant/
├── src/trip_planning_assistant/
│   ├── config.py              # User preferences & trip inputs
│   ├── crew.py                # CrewAI setup & agents
│   ├── exporter.py            # Export to JSON/HTML/MD/CSV
│   ├── logger.py              # Logging configuration
│   ├── main.py                # Entry points (run, interactive, etc.)
│   ├── utils.py               # Validation & utilities
│   ├── config/
│   │   ├── agents.yaml        # Agent definitions
│   │   └── tasks.yaml         # Task definitions
│   └── tools/
│       ├── flight_search_tool.py
│       ├── hotel_search_tool.py
│       ├── weather_tool.py
│       └── currency_tool.py
├── tests/
│   ├── test_config.py         # Configuration tests (11 tests)
│   ├── test_exporter.py       # Export tests (10 tests)
│   ├── test_integration.py    # Integration tests (8 tests)
│   ├── test_utils.py          # Validation tests (15 tests)
│   └── run_tests.py           # Test runner
├── knowledge/
│   ├── user_preference.txt    # User profile (text format)
│   └── user_preferences.json  # User profile (JSON format)
├── logs/                      # Auto-generated logs
├── reports/                   # Generated trip plans
├── pyproject.toml             # Project configuration
├── README.md                  # This file
├── PHASE1.md                  # Phase 1 documentation
├── PHASE2.md                  # Phase 2 documentation (agents/tasks)
├── PHASE3.md                  # Phase 3 documentation (tools)
├── PHASE4.md                  # Phase 4 documentation (app layer)
└── PHASE5.md                  # Phase 5 documentation (testing)
```

## 🧪 Testing

### Run All Tests
```bash
python -m unittest discover -s tests -p 'test_*.py' -v
```

### Run Specific Test Suite
```bash
# Configuration tests
python -m unittest tests.test_config -v

# Utility/validation tests
python -m unittest tests.test_utils -v

# Export tests
python -m unittest tests.test_exporter -v

# Integration tests
python -m unittest tests.test_integration -v
```

### Test Runner Script
```bash
# Run all tests
python tests/run_tests.py

# Quiet mode
python tests/run_tests.py --quiet

# With coverage report
python tests/run_tests.py --coverage
```

### Test Results
```
Ran 40 tests in 0.019s
OK ✅

Coverage:
- test_config.py: 11 tests
- test_utils.py: 15 tests
- test_exporter.py: 10 tests
- test_integration.py: 8 tests
```

## 📊 Output & Exports

Trip plans are automatically exported to multiple formats:

### JSON Export
```json
{
  "trip_parameters": {
    "destination": "Paris",
    "budget": 5000,
    "start_date": "2026-06-01",
    "end_date": "2026-06-10"
  },
  "trip_plan": "Detailed itinerary...",
  "generated_at": "2026-01-06T02:02:35.610Z"
}
```

### HTML Export
- Professional styled document
- Print-friendly layout
- Responsive design
- Custom CSS included

### Markdown Export
- Headers and sections
- Bullet points
- Clean readable format
- Version control friendly

### CSV Export
- Tabular flight/hotel data
- Spreadsheet-compatible
- Easy to analyze

## 🔧 Configuration

### User Preferences

#### JSON Format (`knowledge/user_preferences.json`)
```json
{
  "name": "John Doe",
  "profession": "AI Engineer",
  "home_location": "San Francisco",
  "travel_styles": ["cultural", "adventure", "comfort"],
  "interests": ["AI", "museums", "hiking", "local cuisine"],
  "accommodation_preferences": ["boutique hotels", "airbnb"],
  "dietary_restrictions": [],
  "traveling_with": "partner"
}
```

#### Text Format (`knowledge/user_preference.txt`)
```
User name is John Doe.
User is an AI Engineer.
User is interested in AI Agents.
User is based in San Francisco, California.
```

### Agent Configuration (`src/trip_planning_assistant/config/agents.yaml`)
```yaml
destination_researcher:
  role: Travel Destination Researcher
  goal: Research and analyze travel destinations
  backstory: Expert with deep knowledge of global destinations

flight_searcher:
  role: Flight Search Specialist
  goal: Find cheapest and most convenient flights
  backstory: Flight expert with access to real-time data
```

### Task Configuration (`src/trip_planning_assistant/config/tasks.yaml`)
```yaml
research_destination_task:
  description: Research destination based on travel dates and preferences
  expected_output: Comprehensive destination brief
  agent: destination_researcher
```

## 📝 Logging

Logs are automatically created in `logs/` directory:

```
logs/
├── trip_planner_20260106_020235.log
├── trip_planner_20260106_020456.log
└── ...
```

### Log Levels
- **DEBUG:** Detailed diagnostic info
- **INFO:** Confirmation messages
- **WARNING:** Unexpected conditions
- **ERROR:** Serious problems
- **CRITICAL:** Cannot continue

### Example Log Output
```
2026-01-06 02:02:35 - trip_planning_assistant.crew - INFO - Initializing crew
2026-01-06 02:02:35 - trip_planning_assistant.tools - DEBUG - FlightSearchTool initialized
2026-01-06 02:02:36 - trip_planning_assistant.crew - INFO - Executing task: search_flights_task
2026-01-06 02:02:45 - trip_planning_assistant.crew - INFO - Trip planning completed successfully
```

## 🔐 Environment Variables

```bash
# Required
OPENAI_API_KEY=sk-your-openai-key

# Optional (for real-time data)
SERPAPI_API_KEY=your-serpapi-key

# Optional (for advanced features)
DEBUG=True  # Enable debug logging
LOG_LEVEL=DEBUG  # Set logging level
```

## 📚 Documentation

- [PHASE1.md](PHASE1.md) - Project setup
- [PHASE2.md](PHASE2.md) - Agent & task configuration
- [PHASE3.md](PHASE3.md) - Tools & API integration
- [PHASE4.md](PHASE4.md) - Application layer & input handling
- [PHASE5.md](PHASE5.md) - Testing & documentation

## 🎯 Validation & Error Handling

All inputs are validated:

**Dates:**
- Must be YYYY-MM-DD format
- Must be future dates
- End date after start date
- Max 365 days duration

**Budget:**
- Positive number
- Max $1,000,000

**Travelers:**
- Between 1-100 people

**Preferences:**
- Non-empty string
- Supports any activity types

## 💡 Example Workflows

### Plan a European City Break
```bash
run_interactive

Destination: Barcelona, Spain
Origin: London, UK
Dates: 2026-05-01 to 2026-05-07
Budget: $3,500
Travelers: 2
Preferences: beaches, architecture, nightlife, tapas
```

### Family Beach Vacation
```bash
run_with_trigger '{
  "destination": "Hawaii",
  "origin": "Los Angeles",
  "start_date": "2026-07-01",
  "end_date": "2026-07-14",
  "budget": 8000,
  "travelers_count": 4,
  "preferences": "family activities, beaches, water sports, restaurants"
}'
```

### Backpacking Adventure
```bash
trip_planning_assistant

# Modify default inputs in main.py or use interactive mode
```

## 🐛 Troubleshooting

### No SERPAPI_API_KEY
System will use mock/cached data:
```
FlightSearchTool: SERPAPI_API_KEY environment variable not set
Using fallback search results
```

### Date Validation Errors
```
Error: Start date cannot be in the past
Error: End date must be after start date
Error: Trip duration cannot exceed 365 days
```

### Budget Validation
```
Error: Budget must be greater than 0
Error: Budget exceeds reasonable limits (max $1,000,000)
```

## 📞 Support & Contributions

- **CrewAI Docs:** [https://docs.crewai.com](https://docs.crewai.com)
- **Issues:** [GitHub Issues](https://github.com/project-repo/issues)
- **Discussions:** [GitHub Discussions](https://github.com/project-repo/discussions)

## 📄 License

[Your License Here]

## 🙏 Acknowledgments

Built with:
- [CrewAI](https://crewai.com) - Multi-agent orchestration framework
- [OpenAI](https://openai.com) - Language models
- [SerpAPI](https://serpapi.com) - Search data
- [Python](https://python.org) - Programming language

---

**Status:** ✅ Production Ready  
**Last Updated:** 2026-01-06  
**Version:** 1.0.0
