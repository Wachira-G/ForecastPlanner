#!/usr/bin/env python3

"""Pydantic models (schemas) module."""


from datetime import datetime
from decimal import Decimal
from enum import Enum
from pydantic import BaseModel, EmailStr, Field
from typing import Dict, List, Optional, Union


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
    TomorrowIO = "TomorrowIO"


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
    start_time: datetime
    end_time: datetime
    temperature: Optional[Decimal] = None
    humidity: Optional[Decimal] = None
    wind_speed: Optional[Decimal] = None
    precipitation_probability: Optional[Decimal] = None

    class Config:
        from_attributes = True


class WeatherRecommenderData(BaseModel):
    temperature: float | int
    humidity: float | int
    precipitation_probability: float | int


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


class Recommendation(BaseModel):
    description: str
    suggestions: List[str]
    weather_descriptions: Dict[str, str]


class Location(BaseModel):
    location_id: Optional[int] = None
    name: Optional[str] = None
    latitude: Optional[Decimal] = None
    longitude: Optional[Decimal] = None
    city_name: Optional[str] = None
    country: Optional[str] = None
    location_type: Optional[LocationTypeEnum] = None

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


class TokenBlocklist(BaseModel):
    """Pydantic Token Blocklist model."""

    jti: str
    token_type: str
    exp: datetime

    class Config:
        from_attributes = True
