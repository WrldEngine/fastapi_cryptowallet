from pydantic_settings import BaseSettings
from sqlalchemy import URL


class Settings(BaseSettings):
    DB_ECHO: bool
    PROJECT_NAME: str
    VERSION: str
    DEBUG: bool
    CORS_ALLOWED_ORIGINS: str

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str

    JWT_USER_SECRET_KEY: str
    JWT_VERIFY_SECRET_KEY: str
    JWT_RESET_PASSWORD_SECRET_KEY: str
    REFRESH_TOKEN_EXPIRE_MINUTES: int
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    ALGORITHM: str

    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_DATABASE: str

    EMAIL_SERVER: str
    EMAIL_PORT: int
    EMAIL_PASSWORD: str
    EMAIL_USER: str

    def build_postgres_dsn(self) -> URL:
        return URL.create(
            "postgresql+asyncpg",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_HOST,
            database=self.POSTGRES_DB,
        )

    def build_redis_dsn(self) -> str:
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DATABASE}"

    class Config:
        env_file = ".env"


settings = Settings()
