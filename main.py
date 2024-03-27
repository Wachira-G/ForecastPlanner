#!/usr/bin/env python3

"""Main module running our app."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from database import engine, Base
from routes import user_routes, auth_routes, weather_routes


def create_tables() -> None:
    """
    Create database tables.

    This function creates the necessary tables in the database using SQLAlchemy's
    `create_all` method and the specified database engine.

    Returns:
        None
    """
    Base.metadata.create_all(bind=engine)


def start_application() -> FastAPI:
    """
    Start a FastAPI application.

    This function initializes a FastAPI application with the specified title and version.
    It also adds middleware for handling CORS and includes the routers for authentication,
    user management, and weather data.

    Returns:
        FastAPI: The initialized FastAPI application.
    """
    app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)
    create_tables()
    origins = [
        "*",  # introduces security vulnerability
    ]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(auth_routes.router, tags=["auth"], prefix="/api/v1/auth")
    app.include_router(user_routes.router, tags=["users"], prefix="/api/v1")
    app.include_router(weather_routes.router, tags=["weather"], prefix="/api/v1")
    return app


app = start_application()
