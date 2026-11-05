import openmeteo_requests
import pandas as pd
import scripts.utils.database as database 
from scripts.utils.config import AIR_QUALITY_COLUMNS_MAPPING



openmeteo = openmeteo_requests.Client()

url = "https://air-quality-api.open-meteo.com/v1/air-quality"

def get_air_quality_params(latitude, longitude) -> dict:
    locations = database.load_locations(database.engine)
    if locations.empty:
        raise ValueError("No locations found in database")
    
    return {
        "latitude" : latitude,
        "longitude" : longitude,
        "hourly": list(AIR_QUALITY_COLUMNS_MAPPING.keys()), 
        "timezone" : "auto",
    }