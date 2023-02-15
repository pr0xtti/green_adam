# For logging
import logging
# For GraphQL
# from gql import gql, Client
import requests
# For development
from pprint import pprint
from pprint import pformat

# For logging
from core.config import APP_NAME
# For connection to API
from sxapi.session import connection


def get_missions():
    logger = logging.getLogger(f"{APP_NAME}.{__name__}")
    query = """
        query Launches {
          launches {
            mission_name
            mission_id
          }
        }
    """
    payload = {"query": query}
    logger.debug(f"Querying remote API: {pformat(query)}")
    try:
        result = requests.post(connection.url, json=payload)
        if result:
            result_data = result.json()
            # logger.debug(f"Result: {pformat(result_data).count('mission_name')}")
            # logger.debug(f"Result: {pformat(result_data)}")
            logger.debug(f"OK, result is not empty")
        else:
            err = "Received empty data"
            logger.critical(err)
            return err, None

        missions = result_data['data']['launches']
        return None, missions

    except Exception as e:
        logger.critical(f"Failed to query API: {e}")

