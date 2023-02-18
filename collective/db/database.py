# For logging
import logging
from sqlalchemy_utils import database_exists
from sqlalchemy import inspect, event, DDL, text
# from sqlalchemy.orm import Session

# For logging
from core.config import APP_NAME
from core.config import settings
from db.base_class import Base, metadata
from typing import Any
from db.session import Session, engine
#, session as db


def check_database_exists():
    logger = logging.getLogger(f"{APP_NAME}.{__name__}")
    db_name = settings.POSTGRES_DB
    logger.debug(f"Checking if database: {db_name} exists ...")
    if database_exists(url=settings.DATABASE_URL):
        logger.debug(f"True, database {db_name} exists")
        return True
    else:
        logger.debug(f"False, database {db_name} doesn't exist")
        return False


def check_database_availability():
    logger = logging.getLogger(f"{APP_NAME}.{__name__}")
    db = Session()
    try:
        db.execute(text('SELECT 1'))
        logger.debug(f"Available")
        db.close()
        return True
    except Exception as e:
        logger.critical(f"Database unreachable: {e}")
        db.close()
        return False


def create_database_tables_if_needed() -> str | None:
    logger = logging.getLogger(f"{APP_NAME}.{__name__}")
    schema = settings.POSTGRES_SCHEMA_STAGING
    schemas = inspect(engine).get_schema_names()
    logger.debug(f"Schemas: {schemas}")

    logger.debug("Creating all tables ...")
    event.listen(
        Base.metadata,
        'before_create',
        DDL(f"CREATE SCHEMA IF NOT EXISTS {schema}"),
    )
    Base.metadata.create_all(bind=engine)


def create_tables():
    Base.metadata.create_all(bind=engine, checkfirst=True)


def table_empty(table_model: Base | Any) -> tuple[str | None, bool | None]:
    logger = logging.getLogger(f"{APP_NAME}.{__name__}")
    logger.debug(f"Going db.query().first() ...")
    db = Session()
    try:
        result = db.query(table_model).first()
        db.close()
        if not result:
            logger.debug(f"True, empty result")
            return None, True
        else:
            logger.debug(f"False, not empty result")
            return None, False
    except Exception as e:
        err = f"Failed: {e}"
        logger.debug(err)
        db.close()
        return err, None


def delete_all_tables():
    logger = logging.getLogger(f"{APP_NAME}.{__name__}")
    db_name = f"{settings.POSTGRES_DB}.{settings.POSTGRES_SCHEMA_STAGING}"
    if database_exists(url=settings.DATABASE_URL):
        logger.debug(f"Database {db_name} exists. Deleting all tables ...")
        try:
            Base.metadata.drop_all(bind=engine)
            logger.debug(f"OK, deleted")
        except Exception as e:
            err = f"Failed delete tables: {e}"
            logger.critical(err)
            return err
    else:
        logger.debug(f"Database doesn't exists")
