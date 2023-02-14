# For logging
import logging
# For GraphQL
# from gql import gql, Client
import requests
# For development
from pprint import pprint
from pprint import pformat


from core.config import APP_NAME
from sxapi.session import connection


def get_launches():
    logger = logging.getLogger(f"{APP_NAME}.{__name__}")
    query = """query Launches {
        launches {
            id
            launch_date_utc
        }
    }
    """
    payload = {"query": query}
    logger.debug(f"Querying for launches")
    try:
        # result = connection.client.execute(query)
        result = requests.post(connection.url, json=payload)
        if result:
            result_data = result.json()
            pprint(result_data)
            # launches = result['launches']
            # for launch in launches:
            #     print(launch)
        else:
            logger.critical(f"Received empty data")

    except Exception as e:
        logger.critical(f"Failed to query API: {e}")

