import logging
import scripts.etl.locations_etl as locations
import scripts.etl.weather_etl as weather
import scripts.utils.database as database

"""
-In dit bestand de etl file centraal maken en deze als main gebruiken
-pushen naar git (met nieuwe versie en documentatie)
"""

if __name__ == "__main__": 
    database.create_tables()

    logging.info("Run locations ETL")
    locations.run_locations_etl()

    logging.info("Run weather ETL")
    weather.run_weather_etl()
