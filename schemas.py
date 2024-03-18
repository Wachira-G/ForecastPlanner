#!/usr/bin/env python3

"""Pydantic models (schemas) module."""


from datetime import datetime
from decimal import Decimal
from enum import Enum
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Union


class GenderEnum(str, Enum):
    male = "male"
    female = "female"
    other = "other"


class PreferredUnitsEnum(str, Enum):
    Celsius = "Celsius"
    Fahrenheit = "Fahrenheit"


class WeatherProviderNameEnum(str, Enum):
    OpenWeatherMap = "OpenWeatherMap"
    Weatherstack = "Weatherstack"
    Weatherbit = "Weatherbit"
    AccuWeather_API = "AccuWeather API"
    ClimaCell = "ClimaCell"


class LocationTypeEnum(str, Enum):
    country = "country"
    city = "city"
    # Add other types as needed


class EventTypeEnum(str, Enum):
    meeting = "meeting"
    wedding = "wedding"
    trip = "trip"
    concert = "concert"
    # Add other event types as needed


class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    phone: str
    gender: Optional[GenderEnum] = None


class UserCreate(UserBase):
    password: str = Field(..., min_length=4)

    class Config:
        from_attributes = True


class UserShow(UserBase):
    user_id: int


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    gender: Optional[GenderEnum] = None
    password: Optional[str] = Field(None, min_length=4)


class UserPreferences(BaseModel):
    preference_id: int
    user_id: int
    preferred_units: Optional[PreferredUnitsEnum] = None
    favorite_locations: Optional[str] = None
    notification_settings: Optional[bool] = None

    class Config:
        from_attributes = True


class WeatherForecast(BaseModel):
    forecast_id: int
    location_id: int
    date_time: datetime
    temperature: Optional[Decimal] = None
    humidity: Optional[Decimal] = None
    wind_speed: Optional[Decimal] = None
    precipitation_chance: Optional[Decimal] = None

    class Config:
        from_attributes = True


class WeatherReport(WeatherForecast):
    report_id: int

    class Config:
        from_attributes = True


class WeatherProvider(BaseModel):
    provider_id: int
    api_key: str
    provider_name: WeatherProviderNameEnum
    api_endpoint: Optional[str] = None

    class Config:
        from_attributes = True


class Location(BaseModel):
    location_id: int
    name: str
    latitude: Decimal
    longitude: Decimal
    city_name: str
    country: str
    location_type: LocationTypeEnum

    class Config:
        from_attributes = True


class Events(BaseModel):
    event_id: int
    type: EventTypeEnum
    start_time: Optional[datetime] = None
    duration: Optional[datetime] = None

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str
    refresh_token: str


class TokenData(BaseModel):
    username: Union[str, None] = None
