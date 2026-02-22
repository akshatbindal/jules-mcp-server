import os
import logging
from google.cloud import secretmanager
from pydantic_settings import BaseSettings

logger = logging.getLogger(__name__)

class Settings(BaseSettings):
    project_id: str = os.getenv("GOOGLE_CLOUD_PROJECT", "")
    jules_api_key_secret_name: str = "JULES_API_KEY"
    jules_api_key: str = "" # Can be provided directly for local testing

    model_config = {
        "env_file": ".env",
        "extra": "ignore"
    }

settings = Settings()

def get_jules_api_key() -> str:
    """Retrieves the Jules API key from Secret Manager or environment."""
    if settings.jules_api_key:
        return settings.jules_api_key

    if not settings.project_id:
        logger.warning("GOOGLE_CLOUD_PROJECT not set, and jules_api_key not provided.")
        return ""

    try:
        client = secretmanager.SecretManagerServiceClient()
        name = f"projects/{settings.project_id}/secrets/{settings.jules_api_key_secret_name}/versions/latest"
        response = client.access_secret_version(request={"name": name})
        return response.payload.data.decode("UTF-8")
    except Exception as e:
        logger.error(f"Failed to retrieve secret {settings.jules_api_key_secret_name}: {e}")
        return ""
