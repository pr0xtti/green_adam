# For logging
import logging
# from sqlalchemy.orm import Session
# from pprint import pformat

# For logging
from core.config import APP_NAME
from core.config import settings
from db.models.rocket import *
from db.session import session as db
from db.repository.entity_base import EntityBase
from db.database import table_empty
from sxapi.rocket import *


class EntityRocket(EntityBase):
    name: str = "rocket"
    table_order: list

    def __init__(self):
        logger = logging.getLogger(f"{APP_NAME}.{__name__}")
        try:
            # logger.debug(f"settings.db['schema']: {pformat(settings.db['schema'])}")
            logger.debug(f"Setting self.table_order")
            self.table_order = settings.db['schema']['rocket']['order']
            logger.debug(f"Set: {self.table_order}")
            self.model_order = [self.db_class_name(i) for i in self.table_order]
            logger.debug(f"Set: {self.model_order}")
        except Exception as e:
            logger.critical(f"Failed to init: {e}")

    def __str__(self):
        return self.name

    def get_data_and_save(self) -> tuple[str | None, int | None]:
        logger = logging.getLogger(f"{APP_NAME}.{__name__}")
        tables_affected: int = 0  # Counter
        logger.debug(f"Iterating through models: {self.model_order} ...")
        # Iterating through models/tables list
        for model_name in self.model_order:
            logger.debug(f"Model: {model_name}")
            # Getting class type for a SQLAlchemy Model by class name
            class_type = globals()[model_name]
            err, check = table_empty(db=db, table_model=class_type)
            if not err and check:  # Table is empty
                # Inserting data
                logger.debug(f"Going to fill the table ...")
                # Getting class type for a SxapiTableClass by class name
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

