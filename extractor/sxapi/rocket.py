# For logging
import logging
from pprint import pformat

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


class SxapiRocketEnginesType(SxapiBase):
    query: str = """
        query Launches {
          rockets {
            engines {
              name: type
            }
          }
        }    
    """
    result_template: list = ['data', 'rockets']
    result_template_nested: list = ['engines']

    def get_data(self) -> tuple[str | None, list | None]:
        logger = logging.getLogger(f"{APP_NAME}.{__name__}")
        logger.debug(f"Calling get_data_dim_uniq()")
        return self.get_data_dim_uniq()


class SxapiRocket(SxapiBase):
    query: str = """
        query Launches {
          rockets {
            active
            boosters
            company
            cost_per_launch
            country
            description
            diameter {
              meters
            }
            first_flight
            height {
              meters
            }
            id
            landing_legs {
              number
              material
            }
            mass {
              kg
            }
            name
            success_rate_pct
            type
            wikipedia
          }
        }
    """
    result_template: list = ['data', 'rockets']

    def get_data(self) -> tuple[str | None, list | None]:
        """Gets a data for the table.
                - executes query
                - extracts unique results
            returns list of dicts with data for the table"""
        logger = logging.getLogger(f"{APP_NAME}.{__name__}")
        logger.debug(f"Going to get data ...")
        err, result_data = self.query_exec()
        if err:
            logger.critical(f"Failed: {err}")
            return err, None
        # logger.debug(f"Result: {pformat(result_data).count('name')}")
        logger.debug(f"Data: {pformat(result_data)}")
        data = [
                {
                    'active': item['active'],
                    'boosters': item['boosters'],
                    'company': item['company'],
                    'cost_per_launch': item['cost_per_launch'],
                    'country': item['country'],
                    'description': item['description'],
                    'diameter_meters': item['diameter']['meters'],
                    'first_flight': item['first_flight'],
                    'height_meters': item['height']['meters'],
                    'external_object_id': item['id'],
                    'landing_legs_number': item['landing_legs']['number'],
                    'landing_legs_material': item['landing_legs']['material'],
                    'mass_kg': item['mass']['kg'],
                    'name': item['name'],
                    'success_rate_pct': item['success_rate_pct'],
                    'wikipedia': item['wikipedia'],
                    'type': item['type'],
                    # 2. 'id_rocket_type': id_rocket_type,
                } for item in result_data
        ]

        logger.debug(f"Prepared data: {pformat(data)}")
        logger.debug(f"Returning: {len(data)} count")
        return None, data




