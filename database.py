#!/usr/bin/env python3

"""Module to initialize the database."""

import os
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import settings

""" user = os.getenv('POSTGRES_USER', None)
password = os.getenv('POSTGRES_PWD', None)
host = os.getenv('POSTGRES_HOST', None)
port = os.getenv('POSTGRES_PORT', None)
db = os.getenv('POSTGRES_DB', None) """

SQLALCHEMY_DATABASE_URL = "sqlite:///./weatherapp.db"  # | settings.DATABASE_URL
# SQLALCHEMY_DATABASE_URL = f"postgresql://{user}:{password}@{host}:{port}/{db}"
# SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg2://weatherapp:password@localhost:5432/weatherapp"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Dependency
def get_db() -> Generator:
    """
    Returns a generator that yields a database session.

    Yields:
        SessionLocal: A database session.

    """
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
