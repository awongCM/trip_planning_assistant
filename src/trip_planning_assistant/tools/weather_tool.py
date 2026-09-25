from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import os
import json

class WeatherInput(BaseModel):
    """Input schema for weather lookup."""
    location: str = Field(..., description="Location/city name for weather forecast")
    date: str = Field(..., description="Date in YYYY-MM-DD format for weather forecast")

class WeatherTool(BaseTool):
    name: str = "get_weather"
    description: str = (
        "Get weather forecast for a destination using SerpAPI. Returns temperature, "
        "conditions, humidity, and other weather data. Requires SERPAPI_API_KEY environment variable."
    )
    args_schema: Type[BaseModel] = WeatherInput

    def _run(self, location: str, date: str) -> str:
        """Fetch weather data via SerpAPI."""
        try:
            import serpapi
        except ImportError:
            return json.dumps({
                "error": "serpapi package not installed. Install with: pip install google-search-results",
                "weather": {}
            })

        api_key = os.getenv("SERPAPI_API_KEY")
        if not api_key:
            return json.dumps({
                "error": "SERPAPI_API_KEY environment variable not set",
                "weather": {}
            })

        try:
            params = {
                "engine": "google_weather",
                "q": location,
                "api_key": api_key
            }

            search = serpapi.search(params)
            
            weather_data = {
                "location": location,
                "date": date,
                "current": search.get("current", {}),
                "forecast": search.get("forecast", [])
            }

            # Extract relevant forecast for the given date
            if "forecast" in search:
                for forecast in search["forecast"]:
                    if forecast.get("date") == date:
                        weather_data["forecast_for_date"] = forecast
                        break
            
            return json.dumps({
                "location": location,
                "date": date,
                "weather": weather_data,
                "search_metadata": search.get("search_metadata", {})
            }, indent=2)

        except Exception as e:
            return json.dumps({
                "error": f"Weather lookup failed: {str(e)}",
                "weather": {}
            })
