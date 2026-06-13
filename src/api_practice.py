# api_practice.py
# Phase 1 — Exercise: Call a public API, parse JSON, handle errors
# Save this file in: C:\Projects\phase1-python-basics\src\api_practice.py

import httpx
from dotenv import load_dotenv
import os

# ── Load environment variables from .env ──────────────────────────────────────
load_dotenv()

# ── Configuration ─────────────────────────────────────────────────────────────
# We use the Open-Meteo API — 100% free, no API key needed
# It returns weather data for any city coordinates
CITY = "Casablanca"
LATITUDE = 33.5731
LONGITUDE = -7.5898
API_URL = "https://api.open-meteo.com/v1/forecast"


# ── Main function ──────────────────────────────────────────────────────────────
def get_weather(city: str, lat: float, lon: float) -> dict:
    """
    Call the Open-Meteo API and return current weather data.
    
    Args:
        city: City name (for display only)
        lat: Latitude of the city
        lon: Longitude of the city
    
    Returns:
        A dictionary with temperature and wind speed
    """

    # Define the parameters to send with the request
    params = {
        "latitude": lat,
        "longitude": lon,
        "current_weather": True,  # Ask for current conditions
    }

    try:
        # Make the HTTP GET request — timeout after 10 seconds
        response = httpx.get(API_URL, params=params, timeout=10)

        # Raise an error if the status code is not 200 OK
        response.raise_for_status()

        # Parse the JSON response into a Python dictionary
        data = response.json()

        # Extract what we need from the nested JSON
        current = data["current_weather"]

        return {
            "city": city,
            "temperature_c": current["temperature"],
            "wind_speed_kmh": current["windspeed"],
            "weather_code": current["weathercode"],
        }

    except httpx.TimeoutException:
        print(f"Error: Request timed out. Check your internet connection.")
        return {}

    except httpx.HTTPStatusError as e:
        print(f"Error: API returned status {e.response.status_code}")
        return {}

    except KeyError as e:
        print(f"Error: Unexpected response format — missing key {e}")
        return {}

    except Exception as e:
        print(f"Unexpected error: {e}")
        return {}


# ── Display function ───────────────────────────────────────────────────────────
def display_weather(weather: dict) -> None:
    """
    Print the weather data in a readable format.
    
    Args:
        weather: Dictionary returned by get_weather()
    """
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

    # Show raw JSON — good habit when learning APIs
    print("Raw data returned:")
    print(weather_data)
