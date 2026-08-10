import os
import logging
from pathlib import Path
from dotenv import load_dotenv

#Root
BASE_DIR = Path(__file__).resolve().parent.parent.parent
env_path = BASE_DIR / '.env'

#User/password
load_dotenv(dotenv_path=env_path)

user = os.getenv("DB_USERNAME")
password = os.getenv("DB_PASSWORD")

#Logging
log_file_path = BASE_DIR / "etl_project.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] (%(filename)s) %(message)s", # Toont nu ook de bestandsnaam!
    handlers=[
        logging.StreamHandler(),                # Terminal output
        logging.FileHandler(log_file_path)      # Centrale logfile
    ]
)


