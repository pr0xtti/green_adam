# For logging
import logging

from core.config import APP_NAME
from core.tool import camel_to_snake, snake_to_camel

# from typing import TYPE_CHECKING
# if TYPE_CHECKING:
from sqlalchemy.orm import Session
from db.base_class import Base


class EntityBase:
    def get_data_and_save(self):
        raise Exception("Calling Base method")

    @staticmethod
    def db_class_name(name):
        return snake_to_camel(name)

    @staticmethod
    def db_table_name(name):
        return camel_to_snake(name)

    @staticmethod
    def sxapi_class_name_from_db_class_name(name):
        return "Sxapi" + name

    @staticmethod
    def fill_table(
            db: Session,
            table_model: Base,
            sxapi_class_type,
            db_class_name: str
    ):
        logger = logging.getLogger(f"{APP_NAME}.{__name__}")
        # sxapi_class_name = "Sxapi" + db_class_name
        # sxapi_class_type = globals()[sxapi_class_name]
        logger.debug(f"Instantiating: {sxapi_class_type}")
        sxapi_class_instance = sxapi_class_type()
        logger.debug(f"Calling {sxapi_class_type}.get_data()")
        err, sxapi_data = sxapi_class_instance.get_data()
        if not err:
            logger.debug(f"OK, we have data: {len(sxapi_data)} count")
        db_data = []
        logger.debug(f"Making list of instances of Model ...")
        # Making a list of object of sqlalchemy models (type db.model.Class)
        for item in sxapi_data:
            # Unpacking dict to arguments of Class (db.model.Class) initializator
            db_data.append(table_model(**item))
        logger.debug(f"OK, made: {len(db_data)}")
        logger.debug(f"Going to insert: {len(db_data)} records")
        db.add_all(db_data)
        db.commit()
        logger.debug(f"OK, inserted")
