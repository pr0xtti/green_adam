# For logging
import logging
from sqlalchemy.orm import Session
from pprint import pformat

from core.config import APP_NAME
from core.config import settings
from db.models.mission import *
from db.session import session as db
from db.repository.entity_base import EntityBase
from db.database import table_empty
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
    name: str = "mission"
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

    def __str__(self):
        return self.name

    def get_data_and_save(self) -> tuple[str | None, int | None]:
        logger = logging.getLogger(f"{APP_NAME}.{__name__}")
        logger.debug(f"model_order: {self.model_order}")
        tables_affected: int = 0
        for model_name in self.model_order:
            class_type = globals()[model_name]
            err, check = table_empty(db=db, table_model=class_type)
            if not err and check:  # Table is empty
                # Inserting data
                logger.debug(f"Going to fill the table ...")
                sxapi_class_type = globals()["Sxapi" + model_name]
                self.fill_table(
                    db=db,
                    table_model=class_type,
                    sxapi_class_type=sxapi_class_type,
                    db_class_name=model_name,
                )
                tables_affected += 1
            else:  # Table isn't empty
                # Already has data. Appending or updating data
                # IT'S NOT IMPLEMENTED
                pass
                logger.critical(f"It's not implemented. Doing nothing")

            logger.debug(f"Tables: affected: {tables_affected}, "
                         f"total: {len(self.model_order)}")
            return None, tables_affected

    @staticmethod
    def get_id_by_ext_id(ext_id: str):
        logger = logging.getLogger(f"{APP_NAME}.{__name__}")
        logger.debug(f"Executing db query ...")
        try:
            mission = db.query(Mission).filter_by(
                external_object_id=ext_id
            ).first()
            if mission:
                logger.debug(f"OK, got result")
                return mission.id
            else:
                logger.warning(f"Not found")
        except Exception as e:
            logger.critical(f"Failed: {e}")

    def articles_count(self) -> int | None:
        logger = logging.getLogger(f"{APP_NAME}.{__name__}")
        result = 0
        logger.warning(f"Source unknown. Always returning {result}")
        return result

    def wikipedia_count(self) -> int | None:
        logger = logging.getLogger(f"{APP_NAME}.{__name__}")
        result = 0
        logger.warning(f"Source unknown. Always returning {result}")
        return result
