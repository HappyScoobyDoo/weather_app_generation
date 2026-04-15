from pathlib import Path

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"

REQUEST_TIMEOUT_SECONDS = 10
CACHE_DURATION_SECONDS = 3600  # 1 ora
CACHE_DIR = Path.home() / ".weather_app_cache"

CURRENT_VARIABLES = [
    "temperature_2m",
    "apparent_temperature",
    "wind_speed_10m",
]

DAILY_VARIABLES = [
    "weather_code",
    "temperature_2m_max",
    "temperature_2m_min",
]