#!/usr/bin/env python3

"""Module for various modules that contain our app."""

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


class Weather_Forecast(Base):
    """
    Define a weather forecast particulars for a location and time.

    Attributes:
        forecast_id (int): The unique identifier for the weather forecast.
        location_id (int): The foreign key referencing the location of the forecast.
        date_time (datetime): The date and time of the forecast.
        start_time (datetime): The start time of the forecast.
        end_time (datetime): The end time of the forecast.
        temperature (float): The temperature for the forecast.
        humidity (float): The humidity for the forecast.
        wind_speed (float): The wind speed for the forecast.
        precipitation_probability (float): The probability of precipitation for the forecast.
        location (Location): The relationship to the Location model.
    """

    __tablename__ = "weather_forecast"

    forecast_id = Column(Integer, primary_key=True, autoincrement=True)
    location_id = Column(Integer, ForeignKey("location.location_id"))
    date_time = Column(DateTime, nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    temperature = Column(DECIMAL(5, 2))
    humidity = Column(DECIMAL(5, 2))
    wind_speed = Column(DECIMAL(5, 2))
    precipitation_probability = Column(DECIMAL(5, 2))

    location = relationship("Location")

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Weather_Report(Base):
    """Define a historical weather report for a parricular location."""

    __tablename__ = "weather_reports"

    report_id = Column(Integer, primary_key=True, autoincrement=True)
    location_id = Column(Integer, ForeignKey("location.location_id"))
    date_time = Column(DateTime, nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    temperature = Column(DECIMAL(5, 2))
    humidity = Column(DECIMAL(5, 2))
    wind_speed = Column(DECIMAL(5, 2))
    precipitation_probability = Column(DECIMAL(5, 2))

    location = relationship("Location")

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Weather_Provider(Base):
    """Define a provider for weather data."""

    __tablename__ = "weather_provider"

    provider_id = Column(Integer, primary_key=True, autoincrement=True)
    api_key = Column(String(255), nullable=False)
    provider_name = Column(
        Enum(
            "OpenWeatherMap",
            "Weatherstack",
            "Weatherbit",
            "AccuWeather API",
            "TomorrowIO",
            name="provider_name_enum"
        ),
        nullable=False,
    )
    api_endpoint = Column(Text)
