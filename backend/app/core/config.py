from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "AI Tools Compare API"
    API_V1_PREFIX: str = "/api/v1"

    DATABASE_URL: str = "postgresql+asyncpg://aitc:aitc_secret@localhost:5433/aitc_db"

    model_config = {"env_file": ".env", "extra": "ignore"}


settings = Settings()
