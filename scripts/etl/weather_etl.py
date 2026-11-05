import logging
import pandas as pd
from sqlalchemy.dialects.postgresql import insert as pg_insert
import scripts.utils.api_weather as api
import scripts.utils.database as database



def extract_weather_data(latitude : float, longitude : float) -> list[any]:
    params = api.get_weather_params(latitude, longitude)
    try:
        responses: list[any] = api.openmeteo.weather_api(api.url, params = params)
        return responses
    except Exception as error:
        logging.error(f"API connection error: {error}")
        return[]

def transform_weather_data(response : any, location_id : int) -> pd.DataFrame:
    hourly = response.Hourly()
    hourly_data = {
        "date": pd.date_range(
                start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
                end =  pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
                freq = pd.Timedelta(seconds = hourly.Interval()),
                inclusive = "left"
            ).tz_convert(response.Timezone().decode())
        }
    for index, (api_name, db_name) in enumerate(api.WEATHER_COLUMNS_MAPPING.items()):
        hourly_data[db_name] = hourly.Variables(index).ValuesAsNumpy()

    hourly_dataframe = pd.DataFrame(data = hourly_data)
    hourly_dataframe["location_id"] = location_id

    return hourly_dataframe

def load_weather_data(df : pd.DataFrame) -> None:
    try:
        with database.engine.connect() as connection:
            with connection.begin():
                stmt = pg_insert(database.weather)
                stmt_on_conflict = stmt.on_conflict_do_update(
                    index_elements=['date', 'location_id'],
                    set_={
                        'temperature': stmt.excluded.temperature,
                        'precipitation': stmt.excluded.precipitation,
                        'humidity': stmt.excluded.humidity
                    }
                )
                connection.execute(
                    stmt_on_conflict,
                    df.to_dict(orient="records")
                )
    except Exception as error:
        logging.error(f"ETL error during insert: {error}")

def run_weather_etl(locations : pd.DataFrame) -> None: 
    ##locations_etl
    for location in locations.itertuples(index=False):

        location_id = location.id
        latitude = location.latitude
        longitude = location.longitude


        raw_responses = extract_weather_data(latitude, longitude)

        for response in raw_responses:
            transformed_df  = transform_weather_data(response, location_id)
            load_weather_data(transformed_df)

    logging.info("--- Weather ETL pipline completed ---")