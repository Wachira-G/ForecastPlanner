#!/usr/bin/env python3

"""Module to set the app configuration."""

import os
from typing import Any, Container, Mapping
from dotenv import load_dotenv
from pathlib import Path


env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)


class Settings:
    """Configure some settings on the app."""

    PROJECT_NAME: str = "Forecast Planner API"
    PROJECT_VERSION: str = "0.0.1"

    if os.getenv('POSTGRES_DB'):
        POSTGRES_USER: None | str = os.getenv("POSTGRES_USER")
        POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
        POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "localhost")
        POSTGRES_PORT: str | int = os.getenv(
            "POSTGRES_PORT",
            5432
        )  # default postgres port is 5432
        POSTGRES_DB: str = os.getenv("POSTGRES_DB", "forecast_planner")
        DATABASE_URL = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"
    else:
        DATABASE_URL = "sqlite:///./forecast-planner.db"

    SECRET_KEY: str | bytes | Mapping[str, Any] | Any = os.getenv("SECRET_KEY")
    if SECRET_KEY is None:
        raise ValueError("SECRET_KEY must be set")
    ALGORITHM: str | Container[str] | None = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
    REFRESH_TOKEN_EXPIRE_DAYS: int = int(os.getenv("REFRESH_TOKEN", 1))


settings = Settings()
