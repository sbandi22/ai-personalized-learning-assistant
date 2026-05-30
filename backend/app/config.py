"""Application configuration via environment variables."""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "AI Personalized Learning Assistant"
    api_version: str = "1.0.0"
    # Use SQLite by default; override with a PostgreSQL URL in production.
    database_url: str = "sqlite:///./learning_assistant.db"
    secret_key: str = "CHANGE_ME_IN_PRODUCTION"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
