# api_practice.py
# Phase 1 — Exercise: Call a public API, parse JSON, handle errors
# Save this file in: C:\Projects\phase1-python-basics\src\api_practice.py

import httpx
import os
from dotenv import load_dotenv
from pydantic import BaseModel

# ── Load environment variables from .env ──────────────────────────────────────
load_dotenv()

# ── Configuration ─────────────────────────────────────────────────────────────
CITY = "Casablanca"
LATITUDE = 33.5731
LONGITUDE = -7.5898
API_URL = "https://api.open-meteo.com/v1/forecast"

# 1. Modèles Pydantic (Le Videur)
class CurrentWeather(BaseModel):
    temperature: float
    windspeed: float
    weathercode: int

class WeatherResponse(BaseModel):
    current_weather: CurrentWeather

# 2. Logique métier avec paramètres dynamiques
def get_weather(city: str, lat: float, lon: float) -> dict:
    params = {
        "latitude": lat,
        "longitude": lon,
        "current_weather": "true"
    }
    
    try:
        # Make the HTTP GET request — timeout after 10 seconds
        response = httpx.get(API_URL, params=params, timeout=10)

        # Raise an error if the status code is not 200 OK
        response.raise_for_status()

        # --- NOUVELLE LOGIQUE PYDANTIC ---
        weather = WeatherResponse(**response.json())

        # On retourne un dictionnaire propre pour l'affichage
        return {
            "city": city,
            "temperature_c": weather.current_weather.temperature,
            "wind_speed_kmh": weather.current_weather.windspeed,
            "weather_code": weather.current_weather.weathercode,
        }

    except httpx.TimeoutException:
        print(f"Error: Request timed out. Check your internet connection.")
        return {}
    except httpx.HTTPStatusError as e:
        print(f"Error: API returned status {e.response.status_code}")
        return {}
    except Exception as e:
        print(f"Unexpected error: {e}")
        return {}

# ── Display function ───────────────────────────────────────────────────────────
def display_weather(weather: dict) -> None:
    """Print the weather data in a readable format."""
    if not weather:
        print("No weather data to display.")
        return

    print("\n" + "=" * 40)
    print(f"  Weather for {weather['city']}")
    print("=" * 40)
    print(f"  Temperature : {weather['temperature_c']} °C")
    print(f"  Wind speed  : {weather['wind_speed_kmh']} km/h")
    print(f"  Weather code: {weather['weather_code']}")
    print("=" * 40 + "\n")

# ── Entry point ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print(f"Fetching weather for {CITY}...")

    # Call the function
    weather_data = get_weather(CITY, LATITUDE, LONGITUDE)

    # Display the result
    display_weather(weather_data)