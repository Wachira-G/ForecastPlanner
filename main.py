#!/usr/bin/env python3

"""Main module running our app."""

from fastapi import FastAPI

from config import settings
from database import engine, Base
from routes import user_routes, auth_routes, weather_routes


def create_tables() -> None:
    """Create database tables."""
    Base.metadata.create_all(bind=engine)


def start_application() -> FastAPI:
    """Start a fastAPI application."""
    app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)
    create_tables()
    app.include_router(auth_routes.router, tags=["auth"], prefix="/api/v1/auth")
    app.include_router(user_routes.router, tags=["users"], prefix="/api/v1")
    app.include_router(weather_routes.router, tags=["weather"], prefix="/api/v1")
    return app


app = start_application()
