# For logging
import logging

from pprint import pformat

from core.config import APP_NAME, DETAILS
from sxapi.base import SxapiBase


class SxapiLaunch(SxapiBase):
    query: str = """
        query Launches {
          launches {
            external_object_id: id
            details
            is_tentative
            launch_date_utc
            launch_success
            id_mission: mission_id
            rocket {
              rocket {
                id_rocket: id
              }
            }
            static_fire_date_utc
            telemetry {
              flight_club
            }
            tentative_max_precision
            upcoming
          }
        }
    """
    result_template: list = ['data', 'launches']

    def get_data(self) -> tuple[str | None, list | None]:
        """Gets a data for the table.
            returns list of dicts with data for the table"""
        logger = logging.getLogger(f"{APP_NAME}.{__name__}")
        logger.debug(f"Going to get data ...")
        err, result_data = self.query_exec()
        if err:
            logger.critical(f"Failed: {err}")
            return err, None
        # logger.debug(f"Result: {pformat(result_data).count('name')}")
        logger.log(DETAILS, "Data: {pformat(result_data)}")
        logger.debug(f"Filling data ...")
        data = [
                {
                    'external_object_id': item['external_object_id'],
                    'details': item.get('details'),
                    'is_tentative': item.get('is_tentative'),
                    'launch_date_utc': item.get('launch_date_utc'),
                    'launch_success': item.get('launch_success'),
                    'id_mission': item['id_mission'][0],
                    'id_rocket': item['rocket']['rocket']['id_rocket'],
                    'static_fire_date_utc': item.get('static_fire_date_utc'),
                    'telemetry_flight_club': None if not item.get('telemetry')
                    else item.get('telemetry', {}).get('flight_club'),
                    'tentative_max_precision': item.get('tentative_max_precision'),
                    'upcoming': item['upcoming'],

                } for item in result_data
        ]

        logger.log(DETAILS, f"Prepared data: {pformat(data)}")
        logger.debug(f"Returning: {len(data)} count")
        return None, data
