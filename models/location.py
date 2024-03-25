#!/usr/bin/env python3

"""Module for various modules that contain our app."""

import httpx
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    DECIMAL,
    Enum,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import relationship
from database import Base
from sqlalchemy.orm import Query, Session

from config import settings


class Location(Base):
    """Define a location."""

    __tablename__ = "location"

    location_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=True)
    latitude = Column(DECIMAL(10, 6), nullable=True)
    longitude = Column(DECIMAL(10, 6), nullable=True)
    city_name = Column(String(255), nullable=True)
    country = Column(String(255), nullable=True)
    location_type = Column(
        Enum("country", "city", name="location_type_enum"), nullable=True
    )


async def get_or_create_location(location: str, db: Session) -> Location:
    """Fetch or create a location."""
    location = location.strip().lower()
    if db is None:
        raise ValueError("Database session is not provided")
    if "," in location:
        latitude, longitude = location.split(",")
        existing_location = (
            db.query(Location)
            .filter(Location.latitude == latitude)
            .filter(Location.longitude == longitude)
            .first()
        )
    else:
        existing_location = db.query(Location).filter(Location.name == location).first()
    if existing_location:
        return existing_location

    # Create a new location
    location_attributes = await get_city_coordinates(location)
    if location_attributes:
        new_location = Location(
            name=location,
            latitude=location_attributes[0],
            longitude=location_attributes[1],
            city_name=location_attributes[2],
            country=location_attributes[3],
        )
    else:
        new_location = existing_location
    db.add(new_location)
    db.commit()
    db.refresh(new_location)

    return new_location


async def get_city_coordinates(name: str):
    if not name:
        print("City name cannot be empty")
        return

    API_KEY = settings.OPENWEATHERMAP_API_KEY

    api_url = f"https://api.openweathermap.org/geo/1.0/direct?q={name}&limit=1&appid={API_KEY}"
    async with httpx.AsyncClient() as client:
        response = await client.get(api_url)
    response.raise_for_status()
    data = response.json()

    if not data:
        print(f"No coordinates found for {name}")
        return

    latitude, longitude, name, country = (
        data[0]["lat"],
        data[0]["lon"],
        data[0]["name"],
        data[0]["country"],
    )
    return latitude, longitude, name, country
