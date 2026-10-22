# Setup the Open-Meteo API client with cache and retry on error
import openmeteo_requests
import scripts.utils.database as database 
from scripts.utils.config import WEATHER_COLUMNS_MAPPING


openmeteo = openmeteo_requests.Client()
url = "https://api.open-meteo.com/v1/forecast"

def get_weather_params() -> dict:
    locations = database.load_locations(database.engine)

    if locations.empty:
        raise ValueError("No locations found in database")
    
    return {
        "latitude" : locations["latitude"].tolist(),
        "longitude" : locations["longitude"].tolist(),
        "hourly": list(WEATHER_COLUMNS_MAPPING.keys()), 
        "timezone" : "auto",
    }