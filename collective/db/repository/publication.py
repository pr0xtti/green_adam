# For logging
import logging
from pprint import pformat

from core.config import APP_NAME

# from ..extractor.db.database import table_empty
from db.session import session as db
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
        logger.debug(f"Adding or updating: {len(publications)} items")
        # Add or update
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
            db.commit()
            logger.debug(f"Updated")
        else:
            # Adding
            try:
                db.add_all(publications)
                db.commit()
            except Exception as e:
                err = f"Failed to merge: {e}"
                logger.critical(err)
                return err, None
            logger.debug(f"Added")
        return None, f"len(publications)"
