import dagster as dg
from scripts.etl.weather_etl import (
    extract_weather_data,
    transform_weather_data,
    load_weather_data,
)



@dg.asset
def weather_data():
    responses = extract_weather_data()

    if not responses:
        raise RuntimeError("No weather data received from API")

    return transform_weather_data(responses[0])

@dg.asset
def load_weather(weather_data):
    load_weather_data(weather_data)
