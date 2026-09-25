from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import os
import json

class FlightSearchInput(BaseModel):
    """Input schema for flight search."""
    origin: str = Field(..., description="Origin airport code or city (e.g., 'JFK', 'New York')")
    destination: str = Field(..., description="Destination airport code or city (e.g., 'CDG', 'Paris')")
    departure_date: str = Field(..., description="Departure date in YYYY-MM-DD format")
    return_date: str = Field(..., description="Return date in YYYY-MM-DD format")
    passengers: int = Field(default=1, description="Number of passengers")

class FlightSearchTool(BaseTool):
    name: str = "flight_search"
    description: str = (
        "Search for flights using SerpAPI. Returns flight options with prices, durations, "
        "airlines, and departure/arrival times. Requires SERPAPI_API_KEY environment variable."
    )
    args_schema: Type[BaseModel] = FlightSearchInput

    def _run(self, origin: str, destination: str, departure_date: str, 
             return_date: str, passengers: int = 1) -> str:
        """Search for flights via SerpAPI Google Flights integration."""
        try:
            import serpapi
        except ImportError:
            return json.dumps({
                "error": "serpapi package not installed. Install with: pip install google-search-results",
                "flights": []
            })

        api_key = os.getenv("SERPAPI_API_KEY")
        if not api_key:
            return json.dumps({
                "error": "SERPAPI_API_KEY environment variable not set",
                "flights": []
            })

        try:
            params = {
                "engine": "google_flights",
                "departure_id": origin,
                "arrival_id": destination,
                "outbound_date": departure_date,
                "return_date": return_date,
                "currency": "USD",
                "hl": "en",
                "api_key": api_key
            }

            search = serpapi.search(params)
            
            flights = []
            if "best_flights" in search:
                for flight in search["best_flights"][:5]:
                    flights.append({
                        "airline": flight.get("airline", "Unknown"),
                        "price": flight.get("price", "N/A"),
                        "duration": flight.get("duration", "N/A"),
                        "departure_time": flight.get("departure_time", "N/A"),
                        "arrival_time": flight.get("arrival_time", "N/A"),
                        "stops": flight.get("stops", 0),
                        "layover_duration": flight.get("layover_duration", "N/A")
                    })
            
            return json.dumps({
                "origin": origin,
                "destination": destination,
                "departure_date": departure_date,
                "return_date": return_date,
                "passengers": passengers,
                "flights": flights,
                "search_metadata": search.get("search_metadata", {})
            }, indent=2)

        except Exception as e:
            return json.dumps({
                "error": f"Flight search failed: {str(e)}",
                "flights": []
            })
