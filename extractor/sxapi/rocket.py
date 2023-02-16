# For logging
import logging

# For logging
from core.config import APP_NAME
from sxapi.base import SxapiBase


class SxapiRocketType(SxapiBase):
    query: str = """
        query Launches {
          rockets {
            name: type
          }
        }
    """
    result_template: list = ['data', 'rockets']

    def get_data(self) -> tuple[str | None, list | None]:
        logger = logging.getLogger(f"{APP_NAME}.{__name__}")
        logger.debug(f"Calling get_data_dim_uniq()")
        return self.get_data_dim_uniq()
