#!/usr/bin/env python3

"""Weather related endpoints."""
from datetime import datetime, timedelta, date
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import database
import schemas
from config import settings
from models.location import get_or_create_location
from services.weather_service import query_weather_forecast


router = APIRouter()
units = settings.DEFAULT_UNITS
default_location = settings.DEFAULT_LOCATION
api_key = settings.TOMORROW_IO_API_KEY
fields = []


@router.get("/current_weather", response_model=schemas.WeatherForecast)
async def get_current_weather(
    location_name: str | None = None,
    latitude: float | None = None,
    longitude: float | None = None,
    db: Session = Depends(database.get_db),
):
    """Get the weather forecast for location."""
    try:
        if location_name is not None and location_name != "":
            location = await get_or_create_location(location_name, db)
        elif latitude and longitude:
            location = await get_or_create_location(f"{latitude},{longitude}", db)
        else:
            location = await get_or_create_location(default_location, db)
        forecast = await query_weather_forecast(location, db, "realtime")
        forecast_object = schemas.WeatherForecast(**forecast.__dict__)
        return forecast_object
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Get a five day forecast for a location
@router.get("/five-day_weather", response_model=list[schemas.WeatherForecast])
async def get_five_day_forecast(
    location_name: str | None = None,
    latitude: float | None = None,
    longitude: float | None = None,
    db: Session = Depends(database.get_db),
):
    """Get a five day weather forecast for a location."""
    try:
        if location_name is not None and location_name != "":
            location = await get_or_create_location(location_name, db)
        elif latitude is not None and longitude is not None:
            location = await get_or_create_location(f"{latitude},{longitude}", db)
        else:
            location = default_location
        forecast = await query_weather_forecast(location, db, "5d")
        forecast_objects = [schemas.WeatherForecast(**day.__dict__) for day in forecast]
        return forecast_objects
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Get particular day's weather forecast for a location if within today + 5das else return that it not availble to forecast
@router.get("/a_days_weather", response_model=schemas.WeatherForecast)
async def get_a_days_weather(
    day: date,
    location_name: str | None = None,
    latitude: float | None = None,
    longitude: float | None = None,
    db: Session = Depends(database.get_db),
):
    """Get the weather forecast for a particular day."""
    try:
        if day < datetime.date(datetime.now()) or day > datetime.date(
            datetime.now() + timedelta(days=5)
        ):
            raise HTTPException(
                status_code=404, detail="Weather forecast not available for the day"
            )
        if location_name is not None and location_name != "":
            location = await get_or_create_location(location_name, db)
        elif latitude and longitude:
            location = await get_or_create_location(f"{latitude},{longitude}", db)
        else:
            location = await get_or_create_location(default_location, db)
        forecast = await query_weather_forecast(location, db, "5d")
        for forecast_day in forecast:
            if forecast_day.start_time.date() == day:
                return schemas.WeatherForecast(**forecast_day.__dict__)
        raise HTTPException(
            status_code=404, detail="Weather forecast not available for the day"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
