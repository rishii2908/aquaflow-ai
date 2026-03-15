from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    APP_NAME: str = "AquaFlow AI"
    DEBUG: bool = False

    DATABASE_URL: str = "sqlite+aiosqlite:///./aquaflow.db"

    SECRET_KEY: str = "change-me-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    ALLOWED_ORIGINS: List[str] = ["http://localhost:5173", "http://localhost:3000"]

    # Anomaly detection thresholds
    PRESSURE_MIN_BAR: float = 1.5
    PRESSURE_MAX_BAR: float = 8.0
    FLOW_RATE_MIN: float = 0.0
    FLOW_RATE_MAX: float = 500.0
    ANOMALY_ZSCORE_THRESHOLD: float = 3.0

    class Config:
        env_file = ".env"


settings = Settings()
