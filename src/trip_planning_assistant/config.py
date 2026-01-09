"""User preferences and travel configuration module."""

from dataclasses import dataclass, asdict
from typing import Optional, List
from enum import Enum
import json
from pathlib import Path


class TravelStyle(Enum):
    """Enumeration of travel styles."""
    LUXURY = "luxury"
    COMFORT = "comfort"
    BUDGET = "budget"
    ADVENTURE = "adventure"
    RELAXATION = "relaxation"
    CULTURAL = "cultural"


class AccommodationPreference(Enum):
    """Enumeration of accommodation preferences."""
    HOTEL = "hotel"
    AIRBNB = "airbnb"
    RESORT = "resort"
    BOUTIQUE = "boutique"
    HOSTEL = "hostel"


@dataclass
class UserPreferences:
    """User travel preferences configuration."""
    name: str
    profession: Optional[str] = None
    home_location: Optional[str] = None
    travel_styles: List[str] = None
    accommodation_preferences: List[str] = None
    dietary_restrictions: List[str] = None
    interests: List[str] = None
    mobility_requirements: Optional[str] = None
    traveling_with: Optional[str] = None  # e.g., "family", "partner", "solo"

    def __post_init__(self):
        if self.travel_styles is None:
            self.travel_styles = []
        if self.accommodation_preferences is None:
            self.accommodation_preferences = []
        if self.dietary_restrictions is None:
            self.dietary_restrictions = []
        if self.interests is None:
            self.interests = []

    def to_dict(self) -> dict:
        """Convert preferences to dictionary."""
        return asdict(self)

    def to_prompt_string(self) -> str:
        """Convert preferences to a natural language prompt string for agents."""
        prompt_parts = []
        
        if self.name:
            prompt_parts.append(f"Traveler: {self.name}")
        if self.profession:
            prompt_parts.append(f"Profession: {self.profession}")
        if self.home_location:
            prompt_parts.append(f"Based in: {self.home_location}")
        if self.traveling_with:
            prompt_parts.append(f"Traveling with: {self.traveling_with}")
        if self.travel_styles:
            prompt_parts.append(f"Travel style preferences: {', '.join(self.travel_styles)}")
        if self.interests:
            prompt_parts.append(f"Interests: {', '.join(self.interests)}")
        if self.accommodation_preferences:
            prompt_parts.append(f"Accommodation preferences: {', '.join(self.accommodation_preferences)}")
        if self.dietary_restrictions:
            prompt_parts.append(f"Dietary restrictions: {', '.join(self.dietary_restrictions)}")
        if self.mobility_requirements:
            prompt_parts.append(f"Accessibility needs: {self.mobility_requirements}")
        
        return "\n".join(prompt_parts)

    @staticmethod
    def from_file(filepath: str) -> "UserPreferences":
        """Load user preferences from a JSON or text file."""
        path = Path(filepath)
        
        if not path.exists():
            raise FileNotFoundError(f"User preferences file not found: {filepath}")
        
        if path.suffix == '.json':
            with open(path, 'r') as f:
                data = json.load(f)
            return UserPreferences(**data)
        else:
            # Parse simple text format (for backward compatibility with existing files)
            preferences = {
                "name": "Traveler",
                "interests": [],
                "travel_styles": []
            }
            
            with open(path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    
                    if "name is" in line.lower():
                        preferences["name"] = line.split("is")[-1].strip().rstrip(".")
                    elif "interested in" in line.lower():
                        interests = line.split("interested in")[-1].strip().rstrip(".")
                        preferences["interests"].extend([i.strip() for i in interests.split(",")])
                    elif "based in" in line.lower() or "based" in line.lower():
                        preferences["home_location"] = line.split("based in")[-1].strip().rstrip(".")
                    elif "profession" in line.lower() or "engineer" in line.lower() or "job" in line.lower():
                        if "profession" not in line.lower():
                            preferences["profession"] = line.strip().rstrip(".")
            
            return UserPreferences(**preferences)


@dataclass
class TripInputs:
    """Trip planning input parameters."""
    destination: str
    origin: str
    start_date: str  # YYYY-MM-DD format
    end_date: str    # YYYY-MM-DD format
    budget: float
    travelers_count: int
    preferences: str
    user_preferences: Optional[UserPreferences] = None

    def to_crew_inputs(self) -> dict:
        """Convert to crew inputs dictionary."""
        inputs = {
            'destination': self.destination,
            'origin': self.origin,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'budget': self.budget,
            'travelers_count': self.travelers_count,
            'preferences': self.preferences,
        }
        
        if self.user_preferences:
            inputs['user_context'] = self.user_preferences.to_prompt_string()
        
        return inputs

    @staticmethod
    def from_json(json_string: str) -> "TripInputs":
        """Parse trip inputs from JSON string."""
        data = json.loads(json_string)
        user_prefs = None
        
        if 'user_preferences' in data:
            user_prefs = UserPreferences(**data.pop('user_preferences'))
        
        return TripInputs(user_preferences=user_prefs, **data)
