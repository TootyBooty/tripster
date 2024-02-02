from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # secret
    SECRET_KEY: str = "secret_key"

    # database
    POSTGRES_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/tripster"

    # jwt_auth
    TOKEN_URL: str = "api/v1/auth/token"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 300
    ALGORITHM: str = "HS256"

    class Config:
        env_file = ".env"


Config = Settings()
