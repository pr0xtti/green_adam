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
from db.database import create_database_tables_if_needed, check_database_exists
from db.repository.mission import fill_missions
from db.repository.mission import EntityBase, EntityMission


def get_data_from_space():
    logger = logging.getLogger(f"{APP_NAME}.{__name__}")
    logger.debug(f"Going to get data from SpaceX API ...")
    # Get missions
    err, missions = get_missions()
    if err:
        logger.critical(f"Couldn't get missions: {err}")
        return err

    # if database_tables_exists:
    #   update_data()
    # else:
    #   create_database_tables()

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


def get_space_data_save_into_db() -> str | None:
    """
    """
    logger = logging.getLogger(f"{APP_NAME}.{__name__}")
    logger.debug(f"Going to check if database exists ...")
    if not check_database_exists():
        logger.info(f"Database doesn't exist. Creating ...")
        create_database_tables_if_needed()
        logger.info(f"Created")

    entities: list[EntityBase] = []
    mission = EntityMission()
    entities.append(mission)
    # rocket = EntityRocket()
    # entities.append(rocket)
    # launch = EntityLaunch()
    # entities.append(launch)
    logger.info(f"Iterating entities ...")
    for entity in entities:
        logger.info(f"Entity: {entity}")
        entity.get_data_and_save()
        #   tables = entity.get_tables_order()
        #   for table in tables:
        #       if tables_exists(table):
        #           append_or_update(table, data)
        #       else:
        #           create_table(table)
        #           append_data(table, data)


