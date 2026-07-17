import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    OPENROUTER_API_KEY: str = ""
    OPENCODE_API_KEY: str = ""
    OPENCODE_BASE_URL: str = "https://opencode.ai/zen/v1"
    FRONTEND_URL: str = "http://localhost:3000"
    RATE_LIMIT_RPM: int = 20
    RATE_LIMIT_DAILY: int = 50
    MONGODB_URL: str = ""
    GOOGLE_CLIENT_ID: str = ""
    JWT_SECRET: str = "your_super_secret_jwt_key_here_override_in_env"

    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env"),
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
