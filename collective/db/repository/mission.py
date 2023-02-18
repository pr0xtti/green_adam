# For logging
import logging
from pprint import pformat

from core.config import APP_NAME
from core.config import settings
from db.session import Session
from db.database import table_empty
from db.models.mission import *
from db.repository.entity_base import EntityBase
from sxapi.mission import *


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
            err, check = table_empty(table_model=class_type)
            if not err and check:  # Table is empty
                # Inserting data
                logger.debug(f"Going to fill the table ...")
                sxapi_class_type = globals()["Sxapi" + model_name]
                self.fill_table(
                    # db=db,
                    table_model=class_type,
                    sxapi_class_type=sxapi_class_type,
                    # db_class_name=model_name,
                )
                tables_affected += 1
            else:  # Table isn't empty
                # Already has data. Appending or updating data
                # IT'S NOT IMPLEMENTED
                pass
                logger.critical(f"It's not implemented. Doing nothing")

            logger.debug(f"Affected: {tables_affected}")
            return None, tables_affected

    @staticmethod
    def get_id_by_ext_id(ext_id: str):
        logger = logging.getLogger(f"{APP_NAME}.{__name__}")
        logger.debug(f"Executing db query ...")
        db = Session()
        try:
            mission = db.query(Mission).filter_by(
                external_object_id=ext_id
            ).first()
            db.close()
            if mission:
                logger.debug(f"OK, got result")
                return mission.id
            else:
                logger.warning(f"Not found")
        except Exception as e:
            logger.critical(f"Failed: {e}")
            db.close()

    def articles_count(self) -> int | None:
        logger = logging.getLogger(f"{APP_NAME}.{__name__}")
        result = 0
        logger.debug(f"Source unknown. Always returning {result}")
        return result

    def wikipedia_count(self) -> int | None:
        logger = logging.getLogger(f"{APP_NAME}.{__name__}")
        result = 0
        logger.debug(f"Source unknown. Always returning {result}")
        return result
