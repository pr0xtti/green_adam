# For logging
import logging
from sqlalchemy.orm import Session

# For logging
from core.config import APP_NAME
from db.models.mission import Mission
from db.session import session as db


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

