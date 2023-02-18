# For logging
import logging
# For environment variables
import os
from os import path
import sys
from pathlib import Path
from dotenv import load_dotenv
# For connection string
from urllib.parse import quote_plus
# For settings from config.yaml
import yaml
from pprint import pformat


def get_app_name():
    try:
        return APP_NAME
    except NameError:
        try:
            name = path.abspath(
                str(sys.modules['__main__'].__file__)
            ).split("/")[-1][:-3]
            return name
        except:
            return "service"


# Application name
# APP_NAME: str = "extractor"
APP_NAME: str = get_app_name()


# Make a connection string
def make_connection_string(
        user: str,
        password: str,
        server: str,
        port: str,
        db: str,
) -> str:
    try:
        return (
            f"postgresql://{quote_plus(user)}:"
            f"{quote_plus(password)}@"
            f"{server}:{port}/{db}"
        )
    except Exception as e:
        logger = logging.getLogger(f"{APP_NAME}.{__name__}")
        logger.critical(f"Failed to make a postgres connection string: {e}")


# Logging configuration file
LOGGING_CONFIG_FILE: str = "logging.yaml"
# Default level for logging
LOGGING_DEFAULT_LEVEL: int = logging.DEBUG
DETAILS: int = 5
# Local configuration file name
CONFIG_FILE: str = 'config.yaml'


class Settings:
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_SERVER: str
    POSTGRES_PORT: str
    POSTGRES_DB: str
    POSTGRES_SCHEMA_STAGING: str
    POSTGRES_SCHEMA_MARTS: str
    DATABASE_URL: str
    SLEEP_TIME: int
    SPACEX_API_URL: str

    def __init__(self):
        logger = logging.getLogger(f"{APP_NAME}.{__name__}")

        # Trying to get vars from environment than file
        for step in ["env", "file"]:
            if step == "file":
                env_path = Path(".") / ".env"
                load_dotenv(dotenv_path=env_path)
            try:
                self.POSTGRES_USER: str = os.getenv("POSTGRES_USER")
                self.POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD")
                self.POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "localhost")
                self.POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", 5432)
                self.POSTGRES_DB: str = os.getenv("POSTGRES_DB", "")
                self.POSTGRES_SCHEMA_STAGING: str = os.getenv("POSTGRES_SCHEMA_STAGING")
                self.POSTGRES_SCHEMA_MARTS: str = os.getenv("POSTGRES_SCHEMA_MARTS")
                self.SPACEX_API_URL: str = os.getenv("SPACEX_API_URL")
                logger.debug(f"Set variables from {step}")
            except Exception as e:
                logger.warning(f"Failed to get variables from {step}")

        self.DATABASE_URL = make_connection_string(
            user=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            server=self.POSTGRES_SERVER,
            port=self.POSTGRES_PORT,
            db=self.POSTGRES_DB,
        )

        # Setting other params from local configuration file for the project
        with open(CONFIG_FILE, 'r') as f:
            conf = yaml.safe_load(f.read())
        self.SLEEP_TIME = int(conf['global']['extractor']['sleep_time'])
        self.SLEEP_TIME_MARTMAKER = int(conf['global']['martmaker']['sleep_time'])

        logger.log(DETAILS, f"conf['db']: {pformat(conf['db'])}")
        # print(f"conf['db']: {pformat(conf['db'])}")
        self.db = conf['db']


settings = Settings()
