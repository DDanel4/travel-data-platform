import logging
import scripts.etl.locations_etl as locations
import scripts.etl.weather_etl as weather
import scripts.etl.air_quality_etl as air_quality
import scripts.utils.database as database
##python -m scripts.etl.pipeline



if __name__ == "__main__": 
    database.create_tables()

    logging.info("Run locations ETL")
    locations.run_locations_etl()

    all_locations = database.load_locations(database.engine)

    logging.info("Run weather ETL")
    weather.run_weather_etl(all_locations)

    logging.info("Run air quality ETL")
    air_quality.run_air_quality_etl(all_locations)
    