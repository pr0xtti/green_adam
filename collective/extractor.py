# For logging
import logging
# For loading logging config
import logging.config
import yaml

# For logging
from core.config import APP_NAME
from core.config import LOGGING_CONFIG_FILE
from core.config import LOGGING_DEFAULT_LEVEL
# Tmp
from db.database import delete_all_tables, check_database_availability
# Business logic
from service.common import make_nap, get_space_data_save_into_db


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
        logger.warning(f"Database isn't available. "
                       f"Sleeping for {sleep_time} sec ...")
        make_nap(sleep_time)

    while True:
        # Data append or update hasn't implemented yet
        logger.info('Clearing the database ...')
        delete_all_tables()
        logger.info('Going to get SpaceX data ...')
        err = get_space_data_save_into_db()
        if not err:
            logger.info(f"Done. Data gathered and saved to database")
            logger.info(f"Sleeping till next update ...")
            # Temporary breaking here
        else:
            logger.critical('Failed')
            logger.info('Sleeping till next retry ...')
        make_nap()


if __name__ == '__main__':
    main()
