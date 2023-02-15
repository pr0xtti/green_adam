# For logging
import logging
from sqlalchemy_utils import create_database, database_exists
from sqlalchemy.schema import CreateSchema
from sqlalchemy import inspect, event
from sqlalchemy.orm import Session

# For logging
from core.config import APP_NAME
from core.config import settings
from db.base_class import Base
from db.session import engine


def check_database_exists():
    logger = logging.getLogger(f"{APP_NAME}.{__name__}")
    db_name = settings.POSTGRES_SCHEMA_STAGING + "." + settings.POSTGRES_DB
    logger.debug(f"Checking if database: {db_name} exists ...")
    if database_exists(url=settings.DATABASE_URL):
        logger.debug(f"True, database {db_name} exists")
        return True
    else:
        logger.debug(f"False, database {db_name} doesn't exist")
        return False


def create_database_tables_if_needed():
    logger = logging.getLogger(f"{APP_NAME}.{__name__}")
    schema = settings.POSTGRES_SCHEMA_STAGING
    if not database_exists(url=settings.DATABASE_URL):
        logger.debug(f"Database {schema}"
                     f".{settings.POSTGRES_DB}"
                     f" doesn't exist. Going to create ...")
        try:
            create_database(url=settings.DATABASE_URL)
            logger.debug("Database created")
        except Exception as e:
            err = f"Failed to create database: {e}"
            logger.critical(err)
            return err
    else:
        logger.debug(f"Database exists")

    schemas = inspect(engine).get_schema_names()
    logger.debug(f"Schemas: {schemas}")

    conn = engine.connect()
    if not conn.dialect.has_schema(conn, schema):
        conn.execute(CreateSchema(schema, if_not_exists=True))
        logger.debug(f"Schema created: {schema}")
    else:
        logger.debug(f"Schema exists: {schema}")

    # Check for schema
    # event.listen(Base.metadata, 'before_create', CreateSchema(schema))
    # Base.metadata.reflect(bind=engine, schema=schema)
    # Base.metadata.create_all(bind=engine, checkfirst=True)
    # logger.debug(f"Schema created: {schema}")

    # Create tables
    # Base.metadata.create_all(bind=engine, checkfirst=True)
    # logger.debug("Tables created")


def create_tables():
    Base.metadata.create_all(bind=engine, checkfirst=True)


def table_empty(db: Session, table_model: Base) -> tuple[str | None, bool | None]:
    logger = logging.getLogger(f"{APP_NAME}.{__name__}")
    logger.debug(f"Going db.query().first() ...")
    try:
        result = db.query(table_model).first()
        if not result:
            logger.debug(f"True, empty result")
            return None, True
        else:
            logger.debug(f"False, not empty result")
            return None, False
    except Exception as e:
        err = f"Failed: {e}"
        logger.debug(err)
        return err, None
