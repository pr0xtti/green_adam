# For logging
import logging
# For sleep
import time

# For application settings
from core.config import APP_NAME
from core.config import settings
#
from db.database import create_database_tables_if_needed, check_database_exists
from db.repository.entity_base import EntityBase
from db.repository.mission import EntityMission
from db.repository.rocket import EntityRocket
from db.repository.launch import EntityLaunch


def make_nap(sleep_time: int = settings.SLEEP_TIME):
    logger = logging.getLogger(f"{APP_NAME}.{__name__}")
    logger.info(f"Sleeping for {sleep_time} sec ...")
    time.sleep(sleep_time)


def get_space_data_save_into_db() -> str | None:
    """
    Iterate through entities and get and save data
    """
    logger = logging.getLogger(f"{APP_NAME}.{__name__}")
    logger.debug(f"Will create database and tables if needed")
    create_database_tables_if_needed()

    entities: list[EntityBase] = []
    mission = EntityMission()
    entities.append(mission)
    rocket = EntityRocket()
    entities.append(rocket)
    launch = EntityLaunch()
    entities.append(launch)
    logger.info(f"Iterating entities ...")
    for entity in entities:
        logger.info(f"Entity: {entity}: processing ...")
        err, affected = entity.get_data_and_save()
        if not err:
            logger.info(f"Entity: {entity}: OK, appended or changed")
        else:
            logger.critical(f"Entity: {entity}: Failed to add tables")
