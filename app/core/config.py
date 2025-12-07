from functools import lru_cache
import os

from dotenv import load_dotenv
from pydantic import BaseModel

# Load .env file
load_dotenv()


class Settings(BaseModel):
    app_name: str = os.getenv("APP_NAME", "CodeCrew Backend")
    environment: str = os.getenv("ENVIRONMENT", "dev")
    database_url: str = os.getenv(
        "DATABASE_URL",
        "sqlite:///./codecrew_dev.db",
    )
    secret_key: str = os.getenv("SECRET_KEY", "change-me")
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))


@lru_cache
def get_settings() -> Settings:
    return Settings()
