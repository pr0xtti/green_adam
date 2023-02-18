# For logging
import logging
import time

# For application settings
from core.config import APP_NAME, settings
from db.mart.database import create_database_tables_if_needed
from db.repository.publication import PublicationEntity


def make_mart_publication():
    logger = logging.getLogger(f"{APP_NAME}.{__name__}")
    logger.debug(f"Will create database and tables if needed")
    create_database_tables_if_needed()

    publication = PublicationEntity()
    while True:
        if publication.data_available():
            logger.debug(f"Some data is available in source database")
            break
        else:
            sleep_time = 10
            logger.warning(f"Data still isn't available. "
                           f"Sleeping {sleep_time} sec ...")
        time.sleep(sleep_time)

    logger.debug(f"Mart: {publication}")
    err, rows_affected = publication.get_data_and_save()
    logger.info(f"Mart: {publication}. Appended or changed {rows_affected} rows")
    if not err:
        logger.info(f"Mart: {publication}. Appended or changed {rows_affected} rows")
    else:
        logger.critical(f"Mart: {publication}. Failed to add tables")


def data_available():
    logger = logging.getLogger(f"{APP_NAME}.{__name__}")
    logger.debug(f"Checking availability ...")
    publication = PublicationEntity()
    return publication.data_available()

def make_nap(sleep_time: int = settings.SLEEP_TIME_MARTMAKER):
    logger = logging.getLogger(f"{APP_NAME}.{__name__}")
    logger.debug(f"Sleeping for {sleep_time} sec")
    time.sleep(sleep_time)

