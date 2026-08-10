# Setup database connection
import logging
import scripts.utils.environment as env
import scripts.utils.api_weather as api
from sqlalchemy import  Column, DateTime, inspect, Float, Table, MetaData, Integer, String, UniqueConstraint, create_engine

database_url = f"postgresql+psycopg2://{env.user}:{env.password}@localhost:5432/travel_db"

try:
    engine = create_engine(database_url)
except Exception as error:
    logging.error(f"Error during database connection: {error}")

metadata = MetaData()

base_columns = [
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("date", DateTime(timezone=True)),
    Column("latitude", Float),     
    Column("longitude", Float),
]

dynamic_columns = [
    Column(db_name, Float) 
    for db_name in api.WEATHER_COLUMNS_MAPPING.values()
]

constraints = [
        UniqueConstraint('date', 'latitude', 'longitude', name='uq_weather_date_location')
]

weather = Table(
    "weather", 
    metadata,
    *base_columns,
    *dynamic_columns,
    *constraints
)

def create_tables() -> None:
    inspector = inspect(engine)
    existing_tables = inspector.get_table_names()
    if not existing_tables:

        print("Tables creating...")
        try:
            metadata.create_all(engine)
            logging.info("Tables created!")
        except Exception as error:
            logging.error(f"Table(s) not created: {error}")
    else:
        logging.info(f"Table ({len(existing_tables)} already exists).")