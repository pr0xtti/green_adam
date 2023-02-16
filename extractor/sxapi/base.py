# For logging
import logging
import requests
# For development
from pprint import pformat

# For logging
from core.config import APP_NAME
# For connection to API
from sxapi.session import connection


class SxapiBase:
    query: str = ""
    result_template: list[str] = []

    @staticmethod
    def make_dict_list_uniq(src_list: list[dict]) -> list[dict] | None:
        """Making a list of dict {name: type} with unique dicts"""
        if not src_list:
            return None
        new_list = [
            dict(t) for t in set(
                [tuple(d.items()) for d in src_list]
            )
        ]
        return new_list

    def get_data_from_query_result(self, query_result: dict | list) \
            -> list[dict]:
        """Extracts data from json"""
        def extract_by_template(data: dict, keys: list):
            """Extracts data by template hierarchy"""
            key, *rest = keys
            if rest:
                return extract_by_template(data.get(key, {}), rest)
            return data.get(key)

        logger = logging.getLogger(f"{APP_NAME}.{__name__}")
        result = extract_by_template(query_result, self.result_template)
        logger.debug(f"OK, parsed. Returning: {len(result)} count")
        return result

    def query_exec(self):
        """Executes a self.query with remote API call using requests.post()"""
        logger = logging.getLogger(f"{APP_NAME}.{__name__}")
        payload = {"query": self.query}
        logger.debug(f"Querying remote API: {pformat(self.query)}")
        try:
            result = requests.post(connection.url, json=payload)
            logger.debug(f"OK, result is not empty")
            logger.debug(f"Parsing ...")
            result_data = self.get_data_from_query_result(result.json())
            return None, result_data
        except Exception as e:
            err = f"Failed to query API: {e}"
            logger.critical(err)
            return err, None

    def get_data_dim_uniq(self) -> tuple[str | None, list | None]:
        """Gets a data for dimension with selecting only unique values.
            - executes query
            - extracts unique results
            returns list of dicts with data for a table"""
        logger = logging.getLogger(f"{APP_NAME}.{__name__}")
        logger.debug(f"Going to get data ...")
        err, result_data = self.query_exec()
        if err:
            logger.critical(f"Failed: {err}")
            return err, None
        # logger.debug(f"Result: {pformat(result_data).count('name')}")
        logger.debug(f"Data: {pformat(result_data)}")
        # Making a list of dict {name: type} with unique dicts
        data = self.make_dict_list_uniq(result_data)
        logger.debug(f"Prepared data: {pformat(data)}")
        logger.debug(f"Returning: {len(data)} count")
        return None, data

