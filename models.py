"""Pydantic models and helpers used by the AI-BOT application.

This module exposes:
- ChatRequest: request model for the /chat endpoint
- ChatResponse: response model for the /chat endpoint
- WeatherAPIError: exception raised for weather-related failures
- weather(city): lightweight helper that returns current weather data for a city

Note: The weather() helper is intentionally minimal and returns mocked data so
that the application can run without an external weather API. Replace with a
real implementation as needed.
"""
from typing import Optional, Dict

from pydantic import BaseModel


class ChatRequest(BaseModel):
    """Request body for the /chat endpoint."""

    user_input: str


class ChatResponse(BaseModel):
    """Response body for the /chat endpoint."""

    reply: str


class WeatherAPIError(Exception):
    """Exception raised when a weather lookup fails."""


def weather(city: Optional[str]) -> Dict[str, str]:
    """Return a simple mocked weather result for the given city.

    This is a placeholder implementation. In production replace this with a
    call to a real weather API (OpenWeatherMap, Meteo, etc.) and raise
    WeatherAPIError on failures.

    Args:
        city: City name to look up. If None or empty, a WeatherAPIError is raised.

    Returns:
        A dict containing basic weather information.
    """
    if not city:
        raise WeatherAPIError("city is required for weather lookups")

    # Mocked response — replace with real API call as needed
    return {
        "location": city,
        "temperature": "20°C",
        "wind": "5 km/h",
        "condition": "Partly cloudy",
    }
