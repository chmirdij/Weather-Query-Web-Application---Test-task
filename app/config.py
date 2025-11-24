from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_HOST: str | None = None
    DB_PORT: int | None = None
    DB_USER: str | None = None
    DB_PASS: str | None = None
    DB_NAME: str | None = None

    @computed_field
    @property
    def database_url(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(
        env_file=".env.sample",
        env_file_encoding="utf-8",
    )


settings = Settings()