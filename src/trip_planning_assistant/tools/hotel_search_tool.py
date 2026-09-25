from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import os
import json

class HotelSearchInput(BaseModel):
    """Input schema for hotel search."""
    destination: str = Field(..., description="Hotel destination city or area (e.g., 'Paris', 'Manhattan')")
    check_in_date: str = Field(..., description="Check-in date in YYYY-MM-DD format")
    check_out_date: str = Field(..., description="Check-out date in YYYY-MM-DD format")
    rooms: int = Field(default=1, description="Number of rooms needed")
    max_price: float = Field(default=500, description="Maximum price per night in USD")

class HotelSearchTool(BaseTool):
    name: str = "hotel_search"
    description: str = (
        "Search for hotels using SerpAPI. Returns hotel options with prices, ratings, "
        "amenities, and availability. Requires SERPAPI_API_KEY environment variable."
    )
    args_schema: Type[BaseModel] = HotelSearchInput

    def _run(self, destination: str, check_in_date: str, check_out_date: str,
             rooms: int = 1, max_price: float = 500) -> str:
        """Search for hotels via SerpAPI Google Hotels integration."""
        try:
            import serpapi
        except ImportError:
            return json.dumps({
                "error": "serpapi package not installed. Install with: pip install google-search-results",
                "hotels": []
            })

        api_key = os.getenv("SERPAPI_API_KEY")
        if not api_key:
            return json.dumps({
                "error": "SERPAPI_API_KEY environment variable not set",
                "hotels": []
            })

        try:
            params = {
                "engine": "google_hotels",
                "q": destination,
                "check_in_date": check_in_date,
                "check_out_date": check_out_date,
                "currency": "USD",
                "hl": "en",
                "api_key": api_key
            }

            search = serpapi.search(params)
            
            hotels = []
            if "properties" in search:
                for hotel in search["properties"][:5]:
                    price = hotel.get("price", {})
                    price_value = price.get("lowest", 0) if isinstance(price, dict) else 0
                    
                    if price_value > 0 and price_value <= max_price:
                        hotels.append({
                            "name": hotel.get("title", "Unknown Hotel"),
                            "price_per_night": price_value,
                            "rating": hotel.get("rating", "N/A"),
                            "review_count": hotel.get("review_count", 0),
                            "location": hotel.get("location", "N/A"),
                            "amenities": hotel.get("amenities", []),
                            "image": hotel.get("image", ""),
                            "link": hotel.get("link", "")
                        })
            
            return json.dumps({
                "destination": destination,
                "check_in_date": check_in_date,
                "check_out_date": check_out_date,
                "rooms": rooms,
                "max_price": max_price,
                "hotels": hotels,
                "search_metadata": search.get("search_metadata", {})
            }, indent=2)

        except Exception as e:
            return json.dumps({
                "error": f"Hotel search failed: {str(e)}",
                "hotels": []
            })
