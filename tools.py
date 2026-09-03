"""Tool schemas and env-backed settings for the AI-BOT chatbot."""

import os
from dotenv import load_dotenv

load_dotenv()

# Prefer uppercase names from .env.example; fall back to legacy lowercase keys.
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY") or os.getenv("weather_api_key")
WEATHER_URL = os.getenv("WEATHER_API_URL") or os.getenv("weather_api_url")

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
                        "description": "City name",
                    }
                },
                "required": ["city"],
            },
        },
    }
]
