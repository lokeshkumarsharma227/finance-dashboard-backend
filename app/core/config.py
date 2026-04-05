from pydantic_settings import BaseSettings, SettingsConfigDict
# Reads all environment variables from .env file into a single Settings object.
# Every other file imports 'settings' from here — one source of truth for config.

class Settings(BaseSettings):
    APP_NAME: str
    DEBUG: bool
    SECRET_KEY: str
    DATABASE_URL: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    ALGORITHM: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
# Single instance imported everywhere — never instantiate Settings() again
