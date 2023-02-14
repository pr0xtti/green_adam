# For logging
import logging
# For sleep
import time

# For application settings
from core.config import APP_NAME
from core.config import settings


def get_data_from_space():
    logger = logging.getLogger(f"{APP_NAME}.{__name__}")
    logger.debug(f"Going to get data from SpaceX API ...")
    pass


def make_nap():
    logger = logging.getLogger(f"{APP_NAME}.{__name__}")
    logger.debug(f"Sleeping ...")
    time.sleep(10)
    pass
