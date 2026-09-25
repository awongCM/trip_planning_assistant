from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import json
from datetime import datetime

class CurrencyConversionInput(BaseModel):
    """Input schema for currency conversion."""
    amount: float = Field(..., description="Amount to convert")
    from_currency: str = Field(..., description="Source currency code (e.g., 'USD', 'EUR')")
    to_currency: str = Field(..., description="Target currency code (e.g., 'EUR', 'GBP')")

class CurrencyConversionTool(BaseTool):
    name: str = "convert_currency"
    description: str = (
        "Convert currency amounts using real-time exchange rates. "
        "Provides conversion rates and equivalent amounts in target currency."
    )
    args_schema: Type[BaseModel] = CurrencyConversionInput

    def _run(self, amount: float, from_currency: str, to_currency: str) -> str:
        """Convert currency using exchange rates."""
        try:
            import requests
        except ImportError:
            return json.dumps({
                "error": "requests package not installed",
                "conversion": {}
            })

        if from_currency == to_currency:
            return json.dumps({
                "amount": amount,
                "from_currency": from_currency,
                "to_currency": to_currency,
                "converted_amount": amount,
                "exchange_rate": 1.0,
                "note": "Same currency, no conversion needed"
            })

        try:
            # Try using exchangerate-api.com (free tier available)
            api_url = f"https://api.exchangerate-api.com/v4/latest/{from_currency}"
            response = requests.get(api_url, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                exchange_rate = data.get("rates", {}).get(to_currency)
                
                if exchange_rate:
                    converted_amount = round(amount * exchange_rate, 2)
                    return json.dumps({
                        "amount": amount,
                        "from_currency": from_currency,
                        "to_currency": to_currency,
                        "converted_amount": converted_amount,
                        "exchange_rate": exchange_rate,
                        "timestamp": datetime.now().isoformat(),
                        "source": "exchangerate-api.com"
                    }, indent=2)
                else:
                    return json.dumps({
                        "error": f"Currency {to_currency} not supported",
                        "conversion": {}
                    })
            else:
                # Fallback with mock rates for demo
                mock_rates = {
                    "USD": {"EUR": 0.92, "GBP": 0.79, "JPY": 149.5, "CAD": 1.35, "AUD": 1.53},
                    "EUR": {"USD": 1.09, "GBP": 0.86, "JPY": 162.5, "CAD": 1.47, "AUD": 1.66},
                    "GBP": {"USD": 1.27, "EUR": 1.16, "JPY": 189, "CAD": 1.71, "AUD": 1.93},
                    "JPY": {"USD": 0.0067, "EUR": 0.0062, "GBP": 0.0053, "CAD": 0.0090, "AUD": 0.0102},
                    "CAD": {"USD": 0.74, "EUR": 0.68, "GBP": 0.58, "JPY": 111, "AUD": 1.13},
                    "AUD": {"USD": 0.65, "EUR": 0.60, "GBP": 0.52, "JPY": 98, "CAD": 0.89}
                }
                
                exchange_rate = mock_rates.get(from_currency, {}).get(to_currency, None)
                
                if exchange_rate:
                    converted_amount = round(amount * exchange_rate, 2)
                    return json.dumps({
                        "amount": amount,
                        "from_currency": from_currency,
                        "to_currency": to_currency,
                        "converted_amount": converted_amount,
                        "exchange_rate": exchange_rate,
                        "timestamp": datetime.now().isoformat(),
                        "source": "mock_rates (demo)",
                        "note": "Using cached rates for demonstration"
                    }, indent=2)
                else:
                    return json.dumps({
                        "error": f"Conversion from {from_currency} to {to_currency} not available",
                        "conversion": {}
                    })

        except Exception as e:
            return json.dumps({
                "error": f"Currency conversion failed: {str(e)}",
                "conversion": {}
            })
