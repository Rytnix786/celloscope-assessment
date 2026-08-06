from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    ADAPTER_MODE: str = "mock"
    PORT: int = 8000
    LOG_LEVEL: str = "INFO"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
