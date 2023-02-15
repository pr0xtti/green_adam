# For logging
import logging
# For sleep
import time

# For application settings
from core.config import APP_NAME
from core.config import settings
#
from sxapi.launch import get_launches
from sxapi.mission import get_missions
from db.database import create_database_tables_if_needed
from db.repository.mission import fill_missions


def get_data_from_space():
    logger = logging.getLogger(f"{APP_NAME}.{__name__}")
    logger.debug(f"Going to get data from SpaceX API ...")
    # Get missions
    err, missions = get_missions()
    if err:
        logger.critical(f"Couldn't get missions: {err}")
        return err

    # Create database and tables
    err = create_database_tables_if_needed()
    if err:
        logger.critical(f"Couldn't create database and tables: {err}")
        return err

    # Fill missions
    err = fill_missions(missions)


def make_nap():
    logger = logging.getLogger(f"{APP_NAME}.{__name__}")
    logger.debug(f"Sleeping for {settings.SLEEP_TIME} sec")
    time.sleep(settings.SLEEP_TIME)
