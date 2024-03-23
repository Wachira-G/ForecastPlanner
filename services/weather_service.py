#!/usr/bin/env python3

from datetime import datetime, timedelta
import logging
import httpx
from sqlalchemy.orm import Session

import models.location
import models.weather
from config import settings

units = settings.DEFAULT_UNITS
default_location = settings.DEFAULT_LOCATION
api_key = settings.TOMORROW_IO_API_KEY
fields = []

logger = logging.getLogger(__name__)


async def query_weather_forecast(
    location: models.location.Location, db: Session, forecast_type: str
) -> models.weather.Weather_Forecast | list[models.weather.Weather_Forecast]:
    """Query the weather forecast for a location.

    Args:
        location (models.location.Location): The location for which to query the weather forecast.
        db (Session): The database session.
        forecast_type (str): The type of forecast to query.

    Returns:
        models.weather.Weather_Forecast | list[models.weather.Weather_Forecast]: The weather forecast data.

    """
    try:
        # Find if forecast already queried and in db and return that
        if forecast_type == "realtime":
            existing_forecast = (
                db.query(models.weather.Weather_Forecast)
                .join(models.location.Location)
                .filter(
                    models.location.Location.name == location.name,
                    models.weather.Weather_Forecast.start_time >= datetime.now(),
                    models.weather.Weather_Forecast.end_time
                    <= datetime.now() + timedelta(days=1),
                )
                .first()
            )
            if existing_forecast:
                del existing_forecast.__dict__["_sa_instance_state"]
                return models.weather.Weather_Forecast(**existing_forecast.__dict__)

        if forecast_type == "5d":
            existing_forecast = (
                db.query(models.weather.Weather_Forecast)
                .join(models.location.Location)
                .filter(
                    models.location.Location.name == location.name,
                    models.weather.Weather_Forecast.start_time
                    >= datetime.date(datetime.now()),
                    models.weather.Weather_Forecast.start_time
                    <= datetime.now() + timedelta(days=5),
                )
                .order_by(models.weather.Weather_Forecast.date_time.desc())
                .distinct(models.weather.Weather_Forecast.start_time)
                .all()
            )
            if existing_forecast:
                unique_forecasts = []
                forecast_dates = set()
                for forecast in existing_forecast:
                    if forecast.start_time.date() not in forecast_dates:
                        unique_forecasts.append(
                            models.weather.Weather_Forecast(
                                **{
                                    k: v
                                    for k, v in forecast.__dict__.items()
                                    if k != "_sa_instance_state"
                                }
                            )
                        )
                        forecast_dates.add(forecast.start_time.date())
                return unique_forecasts

        # else try query various apis
        forecast = await query_tomorrow_io(location, db, forecast_type)
        forecast_object = await parse_weather_data(
            forecast, location, forecast_type, db
        )
        return forecast_object
    except Exception as e:
        # Handle the exception here, you can log the error or return a default value
        logger.error(f"An error occurred: {e}")
        return []


async def query_tomorrow_io(
    location: models.location.Location, db: Session, forecast_type: str
) -> dict:
    """Query the weather forecast from Tomorrow.io API.

    Args:
        location (models.location.Location): The location for which to query the weather forecast.
        db (Session): The database session.
        forecast_type (str): The type of forecast to query.

    Returns:
        dict: The weather forecast data.

    """
    try:
        parameters = {
            "apikey": api_key,
            "location": ",".join(map(str, [location.latitude, location.longitude])),
            "fields": ",".join(fields),
            "units": units,
            "timezone": "GMT+3",
        }
        if forecast_type == "realtime":
            pass
        elif forecast_type == "1d":
            parameters["timesteps"] = "1d"
            parameters["startTime"] = "tomorrow"
            parameters["endTime"] = "tomorrow + 1d"
        elif forecast_type == "5d":
            parameters["timesteps"] = "1d"
            parameters["startTime"] = "tomorrow"
            parameters["endTime"] = "tomorrow + 5d"

        if forecast_type == "realtime":
            url = "https://api.tomorrow.io/v4/weather/realtime"
        else:
            url = "https://api.tomorrow.io/v4/weather/forecast"
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=parameters)
        response.raise_for_status()
        forecast_data = response.json()
        return forecast_data
    except httpx.HTTPError as e:
        logger.error(f"HTTP error occurred: {e}")
    except Exception as e:
        logger.error(f"An error occurred: {e}")
    return {}


async def parse_weather_data(
    weather_data: dict,
    location: models.location.Location,
    forecast_type: str,
    db: Session,
) -> models.weather.Weather_Forecast | list[models.weather.Weather_Forecast]:
    """Parse the weather data from the Tomorrow.io API.

    Args:
        weather_data (dict): The weather data received from the API.
        location (models.location.Location): The location for which the weather data is parsed.
        forecast_type (str): The type of forecast being parsed.
        db (Session): The database session.

    Returns:
        models.weather.Weather_Forecast | list[models.weather.Weather_Forecast]: The parsed weather forecast data.

    """
    try:
        if forecast_type == "realtime":
            received_forecast_data = models.weather.Weather_Forecast(
                location=location,
                start_time=datetime.fromisoformat(weather_data["data"]["time"]),
                end_time=datetime.fromisoformat(weather_data["data"]["time"])
                + timedelta(days=1),
                date_time=datetime.now(),
                humidity=weather_data["data"]["values"]["humidity"],
                temperature=weather_data["data"]["values"]["temperature"],
                wind_speed=weather_data["data"]["values"]["windSpeed"],
                precipitation_probability=weather_data["data"]["values"][
                    "precipitationProbability"
                ],
            )
            db.add(received_forecast_data)
            db.commit()
            db.refresh(received_forecast_data)
            return received_forecast_data
        else:
            six_day_forecast = []
            for day in weather_data["timelines"]["daily"]:
                received_forecast_data = models.weather.Weather_Forecast(
                    location=location,
                    start_time=datetime.fromisoformat(day["time"]),
                    end_time=datetime.fromisoformat(day["time"]) + timedelta(days=1),
                    date_time=datetime.now(),
                    humidity=day["values"]["humidityAvg"],
                    temperature=day["values"]["temperatureAvg"],
                    wind_speed=day["values"]["windSpeedAvg"],
                    precipitation_probability=day["values"][
                        "precipitationProbabilityAvg"
                    ],
                )
                six_day_forecast.append(received_forecast_data)
            db.add_all(six_day_forecast)
            db.commit()
            for forecast in six_day_forecast:
                db.refresh(forecast)

            return six_day_forecast
    except Exception as e:
        logger.error(f"An error occurred while parsing weather data: {e}")
        return []


async def query_accuweather(location: models.location.Location):
    """Query the weather forecast from AccuWeather API.

    Args:
        location (models.location.Location): The location for which to query the weather forecast.

    """
    # Add the code to query the AccuWeather API and return the forecast
    pass
