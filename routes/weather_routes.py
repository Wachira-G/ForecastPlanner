#!/usr/bin/env python3

"""Weather related endpoints."""
from datetime import datetime, timedelta, date
from typing import Dict, List, Optional, Union
from fastapi import APIRouter, Depends, HTTPException, Path
import logging
from sqlalchemy.orm import Session

import database
import schemas
from config import settings
from models.location import get_or_create_location
from services.recommendation_service import WeatherAnalyzer, WeatherRecommender
from services.weather_service import query_weather_forecast


logger = logging.getLogger(__name__)
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
    """Get the current weather forecast for a location.

    Args:
        location_name (str, optional): The name of the location. Defaults to None.
        latitude (float, optional): The latitude of the location. Defaults to None.
        longitude (float, optional): The longitude of the location. Defaults to None.
        db (Session, optional): The database session. Defaults to Depends(database.get_db).

    Returns:
        schemas.WeatherForecast: The current weather forecast for the specified location or default_location(Nairobi).

    Raises:
        HTTPException: If there is an error retrieving the weather forecast.

    Examples:
        Example usage to get the current weather forecast using location name as input:
        ```python
        {
            "location_name": "New York",
        }
        ```
        Example usage to get the current weather forecast using latitude and longitude:
        ```python
        {
            "latitude": 40.7128,
            "longitude": -74.0060
        }
        ```
        Example usage to get the current weather forecast using default location:
        ```python
        {
            "location_name": ""
        }
        ```
    """
    try:
        if location_name is not None and location_name != "":
            location = await get_or_create_location(location_name, db)
        elif latitude and longitude:
            location = await get_or_create_location(f"{latitude},{longitude}", db)
        else:
            location = await get_or_create_location(default_location, db)
        forecast = await query_weather_forecast(location, db, "realtime")
        forecast_dict = forecast.__dict__
        forecast_dict["location_name"] = location.city_name
        forecast_object = schemas.WeatherForecast(**forecast_dict)
        return forecast_object
    except Exception as e:
        logger.error(f"get_current_weather function encountered an error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Could not retrieve the current weather forecast.")


@router.get("/five-day_weather", response_model=list[schemas.WeatherForecast])
async def get_five_day_forecast(
    location_name: str | None = None,
    latitude: float | None = None,
    longitude: float | None = None,
    db: Session = Depends(database.get_db),
):
    """Get a five day weather forecast for a location.

    Args:
        location_name (str, optional): The name of the location. Defaults to None.
        latitude (float, optional): The latitude of the location. Defaults to None.
        longitude (float, optional): The longitude of the location. Defaults to None.
        db (Session, optional): The database session. Defaults to Depends(database.get_db).

    Returns:
        list[schemas.WeatherForecast]: The five day weather forecast for the location.

    Raises:
        HTTPException: If there is an error retrieving the weather forecast.

    Examples:
        Example usage to get the five day weather forecast using location name as input:
        ```python
        {
            "location_name": "New York",
        }
        ```
        Example usage to get the five day weather forecast using latitude and longitude:
        ```python
        {
            "latitude": 40.7128,
            "longitude": -74.0060
        }
        ```
        Example usage to get the five day weather forecast using default location:
        ```python
        {
            "location_name": ""
        }
        ```
    """
    try:
        if location_name is not None and location_name != "":
            location = await get_or_create_location(location_name, db)
        elif latitude is not None and longitude is not None:
            location = await get_or_create_location(f"{latitude},{longitude}", db)
        else:
            location = await get_or_create_location(default_location, db)
        forecast = await query_weather_forecast(location, db, "5d")
        #forecast_dict = forecast.__dict__
        #forecast_dict["location_name"] = location.city_name
        #forecast_object = schemas.WeatherForecast(**forecast_dict)
        # create a location_name key in every forecast item in forecast
        forecast_dicts: List[dict] = []
        for day in forecast:
            day_dict = day.__dict__
            day_dict["location_name"] = location.city_name
            forecast_dicts.append(day_dict)
        forecast_objects = [schemas.WeatherForecast(**day) for day in forecast_dicts]
        return forecast_objects
    except Exception as e:
        logger.error(f"get_five_day_forecast function encountered an error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Could not retrieve the five day weather forecast.")


@router.get("/a_days_weather", response_model=schemas.WeatherForecast)
async def get_a_days_weather(
    day: date,
    location_name: str | None = None,
    latitude: float | None = None,
    longitude: float | None = None,
    db: Session = Depends(database.get_db),
):
    """Get the weather forecast for a particular day.

    Args:
        day (date): The date for which to retrieve the weather forecast.
        location_name (str, optional): The name of the location. Defaults to None.
        latitude (float, optional): The latitude of the location. Defaults to None.
        longitude (float, optional): The longitude of the location. Defaults to None.
        db (Session, optional): The database session. Defaults to Depends(database.get_db).

    Returns:
        schemas.WeatherForecast: The weather forecast for the particular day.

    Raises:
        HTTPException: If the weather forecast is not available for the day or if there is an error retrieving the forecast.

    Examples:
        Example usage to get the weather forecast for a particular day using location name as input:
        ```python
        {
            "day": "2022-12-31",
            "location_name": "New York",
        }
        ```
        Example usage to get the weather forecast for a particular day using latitude and longitude:
        ```python
        {
            "day": "2022-12-31",
            "latitude": 40.7128,
            "longitude": -74.0060
        }
        ```
        Example usage to get the weather forecast for a particular day using default location:
        ```python
        {
            "day": "2022-12-31",
            "location_name": ""
        }
        ```
    """
    try:
        if day < datetime.date(datetime.now()) or day > datetime.date(
            datetime.now() + timedelta(days=5)
        ):
            raise HTTPException(
                status_code=404,
                detail="Weather forecast not available for the day: date need to be today(+5 days)."
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
                forecast_day_dict  = forecast_day.__dict__
                forecast_day_dict["location_name"] = location.city_name
                return schemas.WeatherForecast(**forecast_day_dict)
        raise HTTPException(
            status_code=404, detail="Weather forecast not available for the day."
        )
    except Exception as e:
        logger.error(f"get_a_days_weather function encountered an error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Could not retrieve the weather forecast for the day.")


@router.post("/recommendations", response_model=schemas.Recommendation)
async def get_recommendations(weather_data: schemas.WeatherRecommenderData):
    """Get recommendations based on the weather data.

    Args:
        weather_data (schemas.WeatherRecommenderData): The weather data for generating recommendations.

    Returns:
        schemas.Recommendation: The generated recommendations based on the weather data.

    Raises:
        HTTPException: If there is an error generating the recommendations.

    Examples:
        Example usage to get recommendations based on the weather data:
        ```python
        {
            "temperature": 25,
            "humidity": 80,
            "precipitation_probability": 0.5
        }
        ```
    """
    try:
        analyzer = WeatherAnalyzer()
        recommender = WeatherRecommender()

        weather_description = analyzer.analyze_weather(
            weather_data.temperature,
            weather_data.humidity,
            weather_data.precipitation_probability,
        )

        recommendations = recommender.generate_recommendations(**weather_description)

        return schemas.Recommendation(**recommendations)
    except Exception as e:
        logger.error(f"get_recommendations functions encountered an error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Could not generate a recommendation."
        )


@router.get("/{forecast_type}", response_model=list[schemas.WeatherForecast])
async def get_weather_forecast(
    forecast_type: str = Path(
        ...,
        description="The type of forecast to return. Possible values are 'current_weather', 'five-day_weather', 'a_days_weather'"
    ),
    location_name: str | None = None,
    latitude: float | None = None,
    longitude: float | None = None,
    day: date | None = None,
    db: Session = Depends(database.get_db),
):
    """Get the weather forecast based on the forecast type.

    This function retrieves the weather forecast based on the specified forecast type.
    The forecast type can be one of the following:
    - 'current_weather': Returns the current weather forecast.
    - 'five-day_weather': Returns the weather forecast for the next five days.
    - 'a_days_weather': Returns the weather forecast for a specific day.

    The weather forecast can be retrieved using either the location name or the latitude and longitude coordinates.
    If the location name is provided, it will be used to retrieve the location from the database.
    If the latitude and longitude coordinates are provided, they will be used to create a new location in the database.

    Args:
        forecast_type (str): The type of forecast to return.
        location_name (str, optional): The name of the location. Defaults to None.
        latitude (float, optional): The latitude of the location. Defaults to None.
        longitude (float, optional): The longitude of the location. Defaults to None.
        day (date, optional): The date for which to retrieve the weather forecast. Defaults to None.
        db (Session, optional): The database session. Defaults to Depends(database.get_db).

    Returns:
        list[schemas.WeatherForecast]: The weather forecast based on the forecast type.

    Raises:
        HTTPException: If the forecast type is invalid, or if the weather forecast is not available for the specified day, or if there is an error retrieving the forecast.

    Examples:
        Example usage to get the current weather forecast:
        ```python
        {
            "forecast_type": "current_weather",
            "location_name": "New York"
        }
        ```
        Example usage to get the five day weather forecast:
        ```python
        {
            "forecast_type": "five-day_weather",
            "latitude": 40.7128,
            "longitude": -74.0060
        }
        ```
        Example usage to get the weather forecast for a particular day:
        ```python
        {
            "forecast_type": "a_days_weather",
            "day": "2022-12-31",
            "location_name": "New York"
        }
        ```
    """
    try:
        if forecast_type == "current_weather":
            return await get_current_weather(location_name, latitude, longitude, db)
        elif forecast_type == "five-day_weather":
            return await get_five_day_forecast(location_name, latitude, longitude, db)
        elif forecast_type == "a_days_weather":
            if day is None:
                raise HTTPException(
                    status_code=400,
                    detail="Day parameter is required for a_days_weather forecast type."
                )
            if day < datetime.date(datetime.now()) or day > datetime.date(
                datetime.now() + timedelta(days=5)
            ):
                raise HTTPException(
                    status_code=404,
                    detail="Weather forecast not available for the day: date need to be today(+5 days)."
                )
            return await get_a_days_weather(day, location_name, latitude, longitude, db)
        else:
            raise HTTPException(
                status_code=400,
                detail="Invalid forecast type provided. Valid values are 'current_weather', 'five-day_weather', 'a_days_weather'."
            )
    except Exception as e:
        logger.error(f"get_weather_forecast function encountered an error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Could not retrieve the weather forecast.")


@router.get("/weather_and_recommendations/{forecast_type}", response_model=List[Dict[str, Union[dict, schemas.WeatherForecast, schemas.Recommendation]]])
async def get_weather_and_recommendations(
    forecast_type: str = Path(
        ...,
        description="The type of forecast to return. Possible values are 'current_weather', 'five-day_weather', 'a_days_weather'"
    ),
    location_name: Optional[str] = None,
    latitude: Optional[float] = None,
    longitude: Optional[float] = None,
    day: Optional[date] = None,
    db: Session = Depends(database.get_db),
) -> List[Dict[str, Union[dict, schemas.WeatherForecast, schemas.Recommendation]]]:
    """
    Retrieves the weather forecast and recommendations based on the provided parameters.

    Args:
        forecast_type (str): The type of forecast to return.
            Possible values are 'current_weather', 'five-day_weather', 'a_days_weather'.
        location_name (str, optional): The name of the location. Defaults to None.
        latitude (float, optional): The latitude of the location. Defaults to None.
        longitude (float, optional): The longitude of the location. Defaults to None.
        day (date, optional): The specific day for the forecast. Defaults to None.
        db (Session, optional): The database session. Defaults to Depends(database.get_db).

    Returns:
        List[Dict[str, Union[dict, schemas.WeatherForecast, schemas.Recommendation]]]: 
        A list of dictionaries containing the forecast and recommendations.

    Raises:
        HTTPException: If an error occurs while retrieving the weather and recommendations.
    """
    try:
        weather_forecast = await get_weather_forecast(forecast_type, location_name, latitude, longitude, day, db)
        if isinstance(weather_forecast, List):
            forecasts_and_recommendations = []
            for forecast in weather_forecast:
                recommendations = await get_recommendations(schemas.WeatherRecommenderData(**forecast.__dict__))
                days_forecast_and_recommendation = {"forecast": forecast.__dict__, "recommendations": recommendations}
                forecasts_and_recommendations.append(days_forecast_and_recommendation)
            return forecasts_and_recommendations
        else:
            recommendations = await get_recommendations(schemas.WeatherRecommenderData(**weather_forecast.__dict__))
        return [{"forecast": weather_forecast.__dict__, "recommendations": recommendations}]
    except ValueError as e:
        logger.error(f"get_weather_and_recommendations function encountered an error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException as e:
        if e.status_code != 500:
            raise
        logger.error(f"get_weather_and_recommendations function encountered an HTTP error: {str(e.detail)}")
        raise HTTPException(status_code=500, detail="Could not get the weather and recommendations")
    except Exception as e:
        logger.error(f"get_weather_and_recommendations function encountered an unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="Could not get the weather and recommendations")