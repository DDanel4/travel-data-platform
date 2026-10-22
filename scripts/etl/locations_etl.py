import logging
import requests
import pandas as pd
from sqlalchemy.dialects.postgresql import insert as pg_insert
import scripts.utils.api_location as api
import scripts.utils.database as database


def extract_locations() -> pd.DataFrame:
    locations = []

    for place,country in api.places.items():
        params = {
            "name": place,
            "count": 1,
            "language": "en",
            "format": "json",
            "countryCode" : country,
        }
        try:
            response = requests.get(api.endpoint, 
                                    params=params,
                                    timeout=30,
                                )
            response.raise_for_status()
            data = response.json()
            
            results = data.get("results", [])

            if not results:
                logging.warning("No results found for %s", place)
                continue

            result = results[0]

            locations.append({
                "id": result["id"],
                "name": result["name"],                
                "country": result.get("country"),
                "country_code": result.get("country_code"),
                "latitude": result["latitude"],
                "longitude": result["longitude"],
                "timezone": result.get("timezone"),
            })

        except (requests.RequestException, ValueError, KeyError) as error:
            logging.error(
                "Extract %s fails: %s",
                place,
                error,
            )

    return pd.DataFrame(locations)

def transform_locations(df : pd.DataFrame) -> pd.DataFrame: 
    #Transform
    if df.empty:
        return df

    df = df.drop_duplicates(subset=["id"]).copy()

    df["name"] = df["name"].str.strip()
    df = df.dropna(
        subset=["id", "name", "latitude", "longitude"]
    )

    return df

def load_locations(df : pd.DataFrame) -> None:
    if df.empty:
        return 
    
    try:
        records = df.to_dict(orient="records")

        with database.engine.connect() as connection:
            with connection.begin():
                stmt = pg_insert(database.place)
                stmt_on_conflict = stmt.on_conflict_do_update(
                    index_elements=["id"],
                    set_={
                        "name": stmt.excluded.name,
                        "country": stmt.excluded.country,
                        "country_code": stmt.excluded.country_code,
                        "latitude": stmt.excluded.latitude,
                        "longitude": stmt.excluded.longitude,
                        "timezone": stmt.excluded.timezone,
                    },
                )

                connection.execute(
                                    stmt_on_conflict,
                                    df.to_dict(orient="records")
                                )
    except Exception as error:
        logging.error(f"ETL error during insert: {error}")

def run_locations_etl() -> None:
    df = extract_locations()
    df = transform_locations(df)
    load_locations(df)

