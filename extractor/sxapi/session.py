# For logging
import logging

# For application settings
from core.config import APP_NAME
from core.config import settings


class SpaceXAPI:
    def __init__(self):
        logger = logging.getLogger(f"{APP_NAME}.{__name__}")
        self.url: str = settings.SPACEX_API_URL
        logger.debug(f"Setting transport with url: {self.url}")


connection = SpaceXAPI()
