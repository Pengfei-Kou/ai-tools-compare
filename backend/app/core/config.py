from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "AI Tools Compare API"
    API_V1_PREFIX: str = "/api/v1"

    DATABASE_URL: str = "postgresql+asyncpg://aitc:aitc_secret@localhost:5432/aitc_db"
    ADMIN_API_KEY: str = "change_me_in_production"
    ALLOWED_ORIGINS: str = "https://ai-compare.duckdns.org"

    model_config = {"env_file": ".env", "extra": "ignore"}


settings = Settings()
