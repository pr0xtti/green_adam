# For logging
import logging

# For application settings
from core.config import APP_NAME
from db.mart.database import create_database_tables_if_needed
from db.repository.publication import PublicationEntity


def make_mart_publication():
    logger = logging.getLogger(f"{APP_NAME}.{__name__}")
    logger.debug(f"Will create database and tables if needed")
    create_database_tables_if_needed()

    publication = PublicationEntity()
    logger.debug(f"Mart: {publication}")
    err, rows_affected = publication.get_data_and_save()
    logger.info(f"Mart: {publication}. Appended or changed {rows_affected} rows")
    if not err:
        logger.info(f"Mart: {publication}. Appended or changed {rows_affected} rows")
    else:
        logger.critical(f"Mart: {publication}. Failed to add tables")

