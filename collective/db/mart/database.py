# For logging
import logging
from sqlalchemy_utils import database_exists
from sqlalchemy import inspect, event, DDL, text
from sqlalchemy.orm import Session

# For logging
from core.config import APP_NAME
from core.config import settings
from db.mart.base_class import BaseMartModel
from db.session import engine


def create_database_tables_if_needed() -> str | None:
    logger = logging.getLogger(f"{APP_NAME}.{__name__}")
    schema = settings.POSTGRES_SCHEMA_MARTS
    schemas = inspect(engine).get_schema_names()
    logger.debug(f"Schemas present in db: {schemas}")
    logger.debug(f"Creating all tables in schema: {schema}")
    event.listen(
        BaseMartModel.metadata,
        'before_create',
        DDL(f"CREATE SCHEMA IF NOT EXISTS {schema}"),
    )
    BaseMartModel.metadata.create_all(bind=engine)
    schemas = inspect(engine).get_schema_names()
    logger.debug(f"Schemas: {schemas}")
