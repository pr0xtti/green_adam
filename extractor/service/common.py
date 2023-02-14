# For logging
import logging
# For sleep
import time

# For application settings
from core.config import APP_NAME
from core.config import settings
#
from sxapi.launch import get_launches


def get_data_from_space():
    logger = logging.getLogger(f"{APP_NAME}.{__name__}")
    logger.debug(f"Going to get data from SpaceX API ...")

    get_launches()


def make_nap():
    logger = logging.getLogger(f"{APP_NAME}.{__name__}")
    logger.debug(f"Sleeping for {settings.SLEEP_TIME} sec")
    time.sleep(settings.SLEEP_TIME)
