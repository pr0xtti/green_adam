# For logging
import logging
from pprint import pformat

# For logging
from core.config import APP_NAME, DETAILS
from db.models.launch import Launch, LaunchLinks
from db.session import session as db
from db.repository.entity_base import EntityBase
from db.repository.mission import EntityMission  # In use!
from db.repository.rocket import EntityRocket  # In use!
from db.database import table_empty
from sxapi.launch import *


class EntityLaunch(EntityBase):
    name: str = "launch"
    table_order: list

    def __init__(self):
        super(EntityLaunch, self).__init__()

    def get_data_and_save(self) -> tuple[str | None, int | None]:
        logger = logging.getLogger(f"{APP_NAME}.{__name__}")
        tables_affected: int = 0  # Counter
        logger.debug(f"Iterating through models: {self.model_order} ...")
        err, check = table_empty(db=db, table_model=Launch)
        if not err and check:  # Table is empty
            # Inserting data
            logger.debug(f"Going to fill the table ...")
            sxapi_launch = SxapiLaunch()
            err, sxapi_data = sxapi_launch.get_data()
            if not err:
                logger.debug(f"OK, we have data: {len(sxapi_data)} count")
            db_data = []
            logger.debug(f"Making list of instances of Model ...")
            # Making a list of object of sqlalchemy models (type db.model.Class)
            ids_dict = {'id_mission': {}, 'id_rocket': {}}
            for item in sxapi_data:
                for id_name in ids_dict.keys():
                    ext_id = item[id_name]
                    if ext_id not in ids_dict[id_name].keys():
                        entity_name = "Entity" + id_name[3:].title()
                        logger.debug(f"entity_name: {entity_name}")
                        entity_type = globals()[entity_name]
                        logger.debug(f"entity_type: {entity_type}")
                        entity: EntityBase = entity_type()
                        ids_dict[id_name][ext_id] = entity.get_id_by_ext_id(ext_id)
                    item[id_name] = ids_dict[id_name][ext_id]

                logger.log(DETAILS, f"item: {pformat(item)}")
                logger.debug(
                    f"Prepared launch: "
                    f"external_object_id: {item['external_object_id']}, "
                )
                # launch_links table
                launch_links_dict = item.pop('launch_links')
                try:
                    launch = Launch(**item)
                    # launch_links table
                    # launch_links = LaunchLinks(**launch_links_dict, id_launch=launch.id)
                    launch_links = LaunchLinks(**launch_links_dict, launch=launch)
                    db_data.append(launch)
                    db_data.append(launch_links)
                except Exception as e:
                    logger.critical(f"Failed to create instance of Lunch model: {e}")

            logger.debug(f"Going to insert: {len(db_data)} records")
            db.add_all(db_data)
            try:
                db.commit()
            except Exception as e:
                err = f"Failed to insert: {e}"
                logger.critical(err)
                return err, None
            logger.debug(f"OK, inserted")
            tables_affected += 1
        else:  # Table isn't empty
            # Already has data. Appending or updating data
            # IT'S NOT IMPLEMENTED
            pass
            logger.critical(f"It's not implemented. Doing nothing")

        logger.debug(f"Tables: affected: {tables_affected}")
        return None, tables_affected

