# For logging
import logging
from sqlalchemy.orm import Session
from pprint import pformat

# For logging
from core.config import APP_NAME
from core.config import settings
from db.models.mission import *
from db.session import session as db
from db.repository.entity_base import EntityBase
from db.database import table_empty
# from sxapi.mission import get_missions
from sxapi.mission import *


def fill_missions(missions: list) -> str | None:
    logger = logging.getLogger(f"{APP_NAME}.{__name__}")
    # Check if we have no data
    if not missions or not len(missions):
        return "Missions is empty"
    db_missions = []
    for item in missions:
        if item:
            try:
                db_missions.append(
                    Mission(
                        name=item['mission_name'],
                        external_object_id=item['mission_id'],
                    )
                )
            except KeyError as e:
                logger.warning(f"Wrong data in: {item}")
    logger.debug(f"Going to insert: {len(db_missions)} records")
    db.add_all(db_missions)
    db.commit()


def update_data():
    pass


class EntityMission(EntityBase):
    table_order: list

    def __init__(self):
        logger = logging.getLogger(f"{APP_NAME}.{__name__}")
        try:
            # logger.debug(f"settings.db['schema']: {pformat(settings.db['schema'])}")
            logger.debug(f"Setting self.table_order")
            self.table_order = settings.db['schema']['mission']['order']
            logger.debug(f"Set: {self.table_order}")
            self.model_order = [self.db_class_name(i) for i in self.table_order]
            logger.debug(f"Set: {self.model_order}")
        except Exception as e:
            logger.critical(f"Failed to init: {e}")

    def get_data_and_save(self):
        #   tables = entity.get_tables_order()
        #   for table in tables:
        #       if table_empty(table):
        #           append_or_update(table, data)
        #       else:
        #           create_table(table)
        #           append_data(table, data)
        logger = logging.getLogger(f"{APP_NAME}.{__name__}")
        logger.debug(f"model_order: {self.model_order}")
        for model_name in self.model_order:
            class_type = globals()[model_name]
            # model_instance = class_type()
            err, check = table_empty(db=db, table_model=class_type)
            if not err and check:  # Table is empty
                # Inserting data
                logger.debug(f"Going to fill the table ...")
                self.fill_table(
                    table_model=class_type,
                    db_class_name=model_name,)
                pass
            else:  # Table isn't empty
                # Already has data. Appending or updating data
                # IT'S NOT IMPLEMENTED
                logger.critical(f"It's not implemented. Doing nothing")
                pass

    @staticmethod
    def fill_table(table_model: Base, db_class_name: str):
        logger = logging.getLogger(f"{APP_NAME}.{__name__}")
        sxapi_class_name = "Sxapi" + db_class_name
        sxapi_class_type = globals()[sxapi_class_name]
        logger.debug(f"Instantiating: {sxapi_class_name}")
        sxapi_class_instance = sxapi_class_type()
        logger.debug(f"Calling {sxapi_class_name}.get_data()")
        err, sxapi_data = sxapi_class_instance.get_data()
        db_data = []
        # Making a list of object of sqlalchemy models (type db.model.Class)
        for item in sxapi_data:
            # Unpacking dict to arguments of Class (db.model.Class) initializator
            db_data.append(table_model(**item))
        logger.debug(f"Going to insert: {len(db_data)} records")
        db.add_all(db_data)
        db.commit()
        logger.debug(f"OK, inserted")


