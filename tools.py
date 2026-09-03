import os
from dotenv import load_dotenv

load_dotenv()

WEATHER_API_KEY = os.getenv("weather_api_key")

WEATHER_URL = os.getenv("weather_api_url")

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get the current weather conditions for a specific city",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "City name, e.g. 'Hyderabad' or 'London'",
                    }
                },
                "required": ["city"],
            },
        },
    }
]
