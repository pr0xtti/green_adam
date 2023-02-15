# For logging
import logging
# For loading logging config
import logging.config
import yaml
# For sleep
import time

# For logging
from core.config import APP_NAME
from core.config import LOGGING_CONFIG_FILE
from core.config import LOGGING_DEFAULT_LEVEL
# Tmp
from db.database import delete_all_tables
# Business logic
from service.common import get_data_from_space, make_nap, get_space_data_save_into_db


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
    logger.debug('Clearing database ...')
    delete_all_tables()
    while True:
        logger.info('Going to get SpaceX data ...')
        # err = get_data_from_space()
        err = get_space_data_save_into_db()
        if not err:
            # Temporary breaking here
            break
            make_nap()
        else:
            logger.critical('Failed to get data')


if __name__ == '__main__':
    main()
