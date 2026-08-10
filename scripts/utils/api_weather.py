# Setup the Open-Meteo API client with cache and retry on error
import openmeteo_requests

openmeteo = openmeteo_requests.Client()
url = "https://api.open-meteo.com/v1/forecast"

places = {
    (3.5833, 98.6667): "Medan",
}

WEATHER_COLUMNS_MAPPING = {
    "temperature_2m": "temperature",
    "precipitation": "precipitation",
    "relative_humidity_2m": "humidity",
}

latitudes = [coords[0] for coords in places.keys()]
longitudes = [coords[1] for coords in places.keys()]

params = {
    "latitude" : latitudes,
    "longitude" : longitudes,
    "hourly": list(WEATHER_COLUMNS_MAPPING.keys()), 
    "timezone" : "auto",
}