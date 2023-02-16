# For logging
import logging
import requests
# For development
from pprint import pprint
from pprint import pformat

# For logging
from core.config import APP_NAME
# For connection to API
from sxapi.session import connection


class SxapiRocketType:
    query: str = """
        query Launches {
          rockets {
            name: type
          }
        }
    """

    def get_data(self) -> tuple[str | None, list | None]:
        logger = logging.getLogger(f"{APP_NAME}.{__name__}")
        payload = {"query": self.query}
        logger.debug(f"Querying remote API: {pformat(self.query)}")
        try:
            result = requests.post(connection.url, json=payload)
            if result:
                result_data = result.json()
                # logger.debug(f"Result: {pformat(result_data).count('rocket_name')}")
                logger.debug(f"Result: {pformat(result_data)}")
                logger.debug(f"OK, result is not empty")
            else:
                err = "Received empty data"
                logger.critical(err)
                return err, None

            # Making a list of dict {name: type} with unique dicts
            rocket_types = [
                dict(t) for t in set(
                    [tuple(d.items()) for d in result_data['data']['rockets']]
                )
            ]
            logger.debug(f"list: {pformat(rocket_types)}")
            logger.debug(f"Returning: {len(rocket_types)} count")
            return None, rocket_types

        except Exception as e:
            err = f"Failed to query API: {e}"
            logger.critical(err)
            return err, None


# class SxapiRocket:
#     def get_data(self):
#         logger = logging.getLogger(f"{APP_NAME}.{__name__}")
#         query = """
#             query Launches {
#               launches {
#                 name: rocket_name
#                 external_object_id: rocket_id
#               }
#             }
#         """
#         payload = {"query": query}
#         logger.debug(f"Querying remote API: {pformat(query)}")
#         try:
#             result = requests.post(connection.url, json=payload)
#             if result:
#                 result_data = result.json()
#                 # logger.debug(f"Result: {pformat(result_data).count('rocket_name')}")
#                 # logger.debug(f"Result: {pformat(result_data)}")
#                 logger.debug(f"OK, result is not empty")
#             else:
#                 err = "Received empty data"
#                 logger.critical(err)
#                 return err, None
#
#             rockets = result_data['data']['launches']
#             logger.debug(f"Returning: {len(rockets)} count")
#             return None, rockets
#
#         except Exception as e:
#             logger.critical(f"Failed to query API: {e}")
