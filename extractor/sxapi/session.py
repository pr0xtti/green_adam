# For logging
import logging
#
# from gql import gql, Client
# from gql.transport.requests import RequestsHTTPTransport
import requests

# For application settings
from core.config import APP_NAME
from core.config import settings


class SpaceXAPI:
    def __init__(self):
        logger = logging.getLogger(f"{APP_NAME}.{__name__}")
        self.url: str = settings.SPACEX_API_URL
        logger.debug(f"Setting transport with url: {self.url}")
        # self.transport = RequestsHTTPTransport(
        #     url=self.url,
        #     use_json=True,
        # )
        # logger.debug(f"Setting client ...")
        # self.client = Client(
        #     transport=self.transport,
        #     fetch_schema_from_transport=True,
        # )


connection = SpaceXAPI()
