# For logging
import logging
# For loading logging config
import logging.config
import time

import yaml

# For logging
from core.config import APP_NAME
from core.config import LOGGING_CONFIG_FILE
from core.config import LOGGING_DEFAULT_LEVEL
from db.database import check_database_availability

# Business logic
from service.common import make_nap
from service.mart import make_mart_publication, data_available


def setup_logging():
    try:
        with open(LOGGING_CONFIG_FILE, 'r') as f:
            config = yaml.safe_load(f.read())
            logging.config.dictConfig(config)
        logger = logging.getLogger(APP_NAME)
        logger.debug('Logging config loaded')
        logger.debug('Logging started')
    # Failed configuration from file, setting defaults
    except Exception as e:
        logging.basicConfig(level=LOGGING_DEFAULT_LEVEL)
        logger = logging.getLogger(APP_NAME)
        logger.warning(f"Logging set from default. Failed to load logging config: {e}")
    return logger


def main():
    logger = setup_logging()
    logger.info('Application started')
    while True:
        if check_database_availability():
            break
        sleep_time = 5
        logger.info(f"Database isn't available. Sleeping for {sleep_time} sec ...")
        make_nap(sleep_time)

    while True:
        if data_available():
            logger.info(f"Making a publication mart ...")
            make_mart_publication()
        else:
            sleep_time = 10
            logger.warning("Source database is empty. Sleeping ...")
            make_nap(sleep_time)
        err = None
        if not err:
            logger.info(f"OK. Sleeping till next update ...")
        else:
            logger.critical("Failed to get data. Sleeping till next retry ...")
        sleep_time = 30
        make_nap(sleep_time)

if __name__ == '__main__':
    main()
