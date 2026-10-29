# Setup database connection
import logging
import pandas as pd
import scripts.utils.environment as env
from scripts.utils.config import WEATHER_COLUMNS_MAPPING, AIR_QUALITY_COLUMNS_MAPPING
from sqlalchemy import  (Column, DateTime, inspect, Float, Table, MetaData, Integer, 
                         String, UniqueConstraint, create_engine, text)

database_url = f"postgresql+psycopg2://{env.user}:{env.password}@localhost:5432/travel_db"

try:
    engine = create_engine(database_url)
except Exception as error:
    logging.error(f"Error during database connection: {error}")

metadata = MetaData()

def create_base_columns() -> list:
    return [
        Column("id", Integer, primary_key=True, autoincrement=True),
        Column("date", DateTime(timezone=True)),
        Column("latitude", Float),     
        Column("longitude", Float),
        ]

def create_dynamic_columns(mapping) -> list:
    return [
        Column(db_name, Float) 
        for db_name in mapping.values()
        ]

def create_constraints(name) -> list:
    return [
        UniqueConstraint('date', 'latitude', 'longitude', name=name)
        ]

weather = Table(
    "weather", 
    metadata,
    *create_base_columns(),
    *create_dynamic_columns(WEATHER_COLUMNS_MAPPING),
    *create_constraints("uq_weather_date_location")
)

air_quality = Table(
    "air_quality",
    metadata,
    *create_base_columns(),
    *create_dynamic_columns(AIR_QUALITY_COLUMNS_MAPPING),
    *create_constraints("uq_air_quality_date_location")
)

base_columns_places  = [
    Column("id", Integer, primary_key=True),
    Column("name", String(255)),
    Column("country", String(255)),
    Column("country_code", String(3)),
    Column("latitude", Float),     
    Column("longitude", Float),
    Column("timezone", String(255)),
]

constraints_places = [
        UniqueConstraint('id', name='uq_places_id')
]

place = Table(
    "place",
    metadata,
    *base_columns_places,
    *constraints_places
)



def create_tables() -> None:
    inspector = inspect(engine)
    existing_tables = inspector.get_table_names()

    tables_to_create = [
        table
        for table in metadata.sorted_tables
        if table.name not in existing_tables
    ]

    if not tables_to_create:
        logging.info(f"Table ({len(existing_tables)} already exists).")
        return

    logging.info(
        "Creating tables: %s",
        ", ".join(table.name for table in tables_to_create)
    )

    try:
        metadata.create_all(engine)
        logging.info("Tables created!")
    except Exception as error:
        logging.error(f"Table(s) not created: {error}")


def load_locations(engine):
    query = text("""
                SELECT latitude, longitude, name
                FROM place
                    """)
    with engine.connect() as connection:
        return pd.read_sql(query, connection)