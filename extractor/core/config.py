# For logging
import logging
# For environment variables
import os
from pathlib import Path
from dotenv import load_dotenv
# For connection string
from urllib.parse import quote_plus


# Make a connection string
def make_connection_string(
        user: str,
        password: str,
        server: str,
        port: str,
        db: str,
) -> str:
    return (
        f"postgresql://{quote_plus(user)}:"
        f"{quote_plus(password)}@"
        f"{server}:{port}/{db}"
    )


# Application name
APP_NAME: str = "extractor"
# Logging configuration file
LOGGING_CONFIG_FILE: str = "logging.yaml"
# Default level for logging
LOGGING_DEFAULT_LEVEL: int = logging.DEBUG
logger = logging.getLogger(f"{APP_NAME}.{__name__}")


class Settings:

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_SERVER: str
    POSTGRES_PORT: str
    POSTGRES_DB: str
    DATABASE_URL: str

    def __init__(self):
        # Trying to get vars from environment than file
        for step in ["env", "file"]:
            if step == "file":
                env_path = Path(".") / ".env"
                load_dotenv(dotenv_path=env_path)
            try:
                self.POSTGRES_USER: str = os.getenv("POSTGRES_USER")
                self.POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD")
                self.POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "localhost")
                self.POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", 5432)
                self.POSTGRES_DB: str = os.getenv("POSTGRES_DB", "")
            except Exception as e:
                logger.warning(f"Failed to get variables from {step}")

        self.DATABASE_URL = make_connection_string(
            user=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            server=self.POSTGRES_SERVER,
            port=self.POSTGRES_PORT,
            db=self.POSTGRES_DB,
        )


settings = Settings
