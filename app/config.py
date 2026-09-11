from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
from app.constants import ENV_FILE

class Settings(BaseSettings):
    app_name: str
    database_url: str
    aws_region: str
    s3_bucket: str
    sqs_queue_url: str

    model_config = SettingsConfigDict(env_file=ENV_FILE)

@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings()