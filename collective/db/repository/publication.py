# For logging
import logging
from pprint import pformat

from core.config import APP_NAME

from db.session import Session
from db.database import table_empty
from db.models.rocket import Rocket
from db.models.launch import Launch, LaunchLinks
from db.models.publication import Publication
from db.repository.launch import EntityLaunch
from db.repository.rocket import EntityRocket
from db.repository.mission import EntityMission

class PublicationEntity:
    name: str = "publication"

    def __str__(self):
        return self.name

    def prepare_data(self) -> list[dict]:
        logger = logging.getLogger(f"{APP_NAME}.{__name__}")
        publications_dict = []
        entity_launch = EntityLaunch()
        entity_rocket = EntityRocket()
        entity_mission = EntityMission()
        entities = [entity_launch, entity_rocket, entity_mission]
        for entity in entities:
            result = entity.articles_count()
            articles = result
            result = entity.wikipedia_count()
            wikipedia = result
            record = {
                'entity': entity.name,
                'articles': articles,
                'wikipedia': wikipedia,
            }
            logger.debug(f"Prepared record: {record}")
            publications_dict.append(record)

        return publications_dict

    def get_data_and_save(self) -> tuple[str | None, str | None]:
        logger = logging.getLogger(f"{APP_NAME}.{__name__}")
        # Merge: insert or update
        # db = Session()
        publications_dict = self.prepare_data()
        logger.debug(f"Prepared data: {pformat(publications_dict)}")

        publications = [
            Publication(**item) for item in publications_dict
        ]
        logger.debug(f"Data: {publications}")

        # Add or update
        logger.debug(f"Adding or updating: {len(publications)} items")
        err = None
        with Session() as db:
            result = db.query(Publication).count()
            if result:
                # Updating
                for p in publications:
                    db.query(Publication).filter(
                        Publication.entity == p.entity
                    ).update({
                        Publication.articles: p.articles,
                        Publication.wikipedia: p.wikipedia,
                    })
                try:
                    db.commit()
                except:
                    db.rollback()
                logger.debug(f"Updated")
            else:
                # Adding
                try:
                    db.add_all(publications)
                    db.commit()
                    logger.debug(f"Added")
                except Exception as e:
                    db.rollback()
                    err = f"Failed to merge: {e}"
                    logger.critical(err)
        if err:
            return err, None
        return None, len(publications)

    @staticmethod
    def data_available() -> bool:
        logger = logging.getLogger(f"{APP_NAME}.{__name__}")
        logger.debug(f"Checking if database isn't empty ...")
        tables_to_check = [LaunchLinks, Rocket]
        for table_model in tables_to_check:
            err, result = table_empty(table_model=table_model)
            if not err and not result:
                # No error and (some) table has data
                return True
        return False
