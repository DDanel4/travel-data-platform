import time
import dagster as dg
import pandas as pd
from scripts.etl.weather_etl import (
    extract_weather_data,
    transform_weather_data,
    load_weather_data,
)



@dg.asset
def weather_data(context : dg.AssetExecutionContext) -> pd.DataFrame:
    start_time = time.time()
    responses = extract_weather_data()

    if not responses:
        raise RuntimeError("No weather data received from API")

    elapsed_time = round(time.time() - start_time, 2)

    df = transform_weather_data(responses[0])

    context.add_output_metadata({
        "dagster/row_count": len(df),
        "runtime_seconds": elapsed_time,
    })

    return df

@dg.asset
def load_weather(context : dg.AssetExecutionContext, weather_data : pd.DataFrame) -> None:
    start_time = time.time()

    load_weather_data(weather_data)

    elapsed_time = round(time.time() - start_time, 2)

    context.add_output_metadata({
            "dagster/row_count": len(weather_data),
            "runtime_seconds": elapsed_time,
    })