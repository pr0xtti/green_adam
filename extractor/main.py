# For logging
import logging
# For loading logging config
import logging.config
import yaml

from core.config import APP_NAME
from core.config import LOGGING_CONFIG_FILE
from core.config import LOGGING_DEFAULT_LEVEL


def main():
    try:
        with open(LOGGING_CONFIG_FILE, 'r') as f:
            config = yaml.safe_load(f.read())
            logging.config.dictConfig(config)
        logger = logging.getLogger(APP_NAME)
        logger.debug('Logging config loaded')
    # Failed configuration from file, setting defaults
    except Exception as e:
        logging.basicConfig(level=LOGGING_DEFAULT_LEVEL)
        logger = logging.getLogger(APP_NAME)
        logger.warning(f"Logging set from default. Failed to load logging config: {e}")

    logger.debug('Logging started')
    logger.info('Application started')

    logger.info('Application finished')


if __name__ == '__main__':
    main()