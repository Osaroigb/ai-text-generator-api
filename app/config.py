import os
import logging
from dotenv import load_dotenv
from colorlog import ColoredFormatter

# Load environment variables from .env file
load_dotenv()

# Constants for environment variable names
APP_PORT_VAR = "APP_PORT"
APP_HOST_VAR = "APP_HOST"
APP_NAME_VAR = "APP_NAME"
APP_ENV_VAR = "APP_ENV"
JWT_SECRET_KEY_VAR = "JWT_SECRET_KEY"
DATABASE_URL_VAR = "DATABASE_URL"
JWT_EXPIRY_IN_SECONDS_VAR = "JWT_EXPIRY_IN_SECONDS"
OPENAI_API_KEY_VAR = "OPENAI_API_KEY"

# Configuration class
class Config:
    APP_PORT: int = int(os.getenv(APP_PORT_VAR))
    APP_HOST: str = os.getenv(APP_HOST_VAR)
    APP_NAME: str = os.getenv(APP_NAME_VAR)
    APP_ENV: str = os.getenv(APP_ENV_VAR)
    JWT_SECRET_KEY: str = os.getenv(JWT_SECRET_KEY_VAR)
    DATABASE_URL: str = os.getenv(DATABASE_URL_VAR)
    JWT_EXPIRY_IN_SECONDS: int = int(os.getenv(JWT_EXPIRY_IN_SECONDS_VAR))
    OPENAI_API_KEY: str = os.getenv(OPENAI_API_KEY_VAR)

    @classmethod
    def validate_env(cls):
        required_vars = [
            DATABASE_URL_VAR,
            JWT_EXPIRY_IN_SECONDS_VAR,
            OPENAI_API_KEY_VAR,
            APP_NAME_VAR,
            APP_ENV_VAR,
            JWT_SECRET_KEY_VAR,
            APP_PORT_VAR,
            APP_HOST_VAR
        ]

        missing_vars = [var for var in required_vars if not os.getenv(var)]

        if missing_vars:
            raise EnvironmentError(f"Missing required environment variables: {', '.join(missing_vars)}")

# Define color format for log messages
formatter = ColoredFormatter(
    "%(log_color)s%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    log_colors={
        "INFO": "green",
        "WARNING": "yellow",
        "ERROR": "red",
    },
)

# Set up logging with color formatter
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logging.basicConfig(level=logging.INFO, handlers=[handler])