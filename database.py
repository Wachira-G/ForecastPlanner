#!/usr/bin/env python3

"""Module to initialize the database."""

import os
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import settings


# if postgress is the db:
if settings.DATABASE_URL.startswith("postgres"):
    engine = create_engine(settings.DATABASE_URL)
elif settings.DATABASE_URL.startswith('sqlite'):
    engine = create_engine(
        settings.DATABASE_URL, connect_args={"check_same_thread": False}
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
