from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_env: str = "dev"
    database_url: str = "postgresql+psycopg://postgres:postgres@db:5432/incidents"
    redis_url: str = "redis://redis:6379/0"

settings = Settings()
