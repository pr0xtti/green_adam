# For logging
import logging
# For GraphQL
import requests
# For development
from pprint import pformat

# For logging
from core.config import APP_NAME, DETAILS
# For connection to API
from sxapi.session import connection
from sxapi.base import SxapiBase


class SxapiMission(SxapiBase):
    query: str = """
        query Launches {
          launches {
            name: mission_name
            external_object_id: mission_id
          }
        }
    """
    result_template: list = ['data', 'launches']

    def get_data(self) -> tuple[str | None, list | None]:
        logger = logging.getLogger(f"{APP_NAME}.{__name__}")
        logger.debug(f"Going to get data ...")
        err, result_data = self.query_exec()
        if err:
            logger.critical(f"Failed: {err}")
            return err, None
        logger.log(DETAILS, "Data: {pformat(result_data)}")
        data = [
            {
                'name': item['name'],
                'external_object_id': item['external_object_id'][0],
            } for item in result_data
        ]

        logger.log(DETAILS, f"Prepared data: {pformat(data)}")
        logger.debug(f"Returning data: {len(data)} count")
        return None, data
