from typing import Dict, List, Tuple, Union

#!/usr/bin/env python3



class WeatherAnalyzer:
    """
    A class that analyzes weather parameters.

    Example usage:
    ```python
    analyzer = WeatherAnalyzer()
    weather_data = {
        "temperature": 28.70,
        "humidity": 84.40,
        "precipitation_probability": 0.00
    }
    analysis = analyzer.analyze_weather(**weather_data)
    print(f"Weather Description: {analysis['description']}")
    ```
    """

    def analyze_weather(
        self,
        temperature: Union[int, float],
        humidity: Union[int, float],
        precipitation_probability: Union[int, float],
    ) -> Dict[str, str]:
        """
        Analyzes the given weather parameters and generates a description and suggestions based on the analysis.

        Args:
            temperature: The temperature in degrees Celsius.
            humidity: The humidity level in percentage.
            precipitation_probability: The probability of precipitation in percentage.

        Returns:
            A dictionary containing the description and suggestions based on the weather parameters.
            The dictionary has the following structure:
            {
                "temperature_description": str,  # Description of the temperature category
                "humidity_description": str,  # Description of the humidity category
                "precipitation_description": str,  # Description of the precipitation category
            }
        """

        # Validate input data
        if not isinstance(temperature, (int, float)):
            raise ValueError("Temperature must be a number")
        if not isinstance(humidity, (int, float)):
            raise ValueError("Humidity must be a number")
        if not isinstance(precipitation_probability, (int, float)):
            raise ValueError("Precipitation probability must be a number")

        # Define thresholds for temperature, humidity, and precipitation probability
        temperature_categories: Dict[str, Tuple[float, float]] = {
            "Cold": (-float("inf"), 10),
            "Cool": (10, 20),
            "Mild": (20, 25),
            "Warm": (25, 30),
            "Hot": (30, float("inf")),
        }

        humidity_categories: Dict[str, Tuple[float, float]] = {
            "Low": (-float("inf"), 30),
            "Moderate": (30, 60),
            "High": (60, float("inf")),
        }

        precipitation_categories: Dict[str, Tuple[float, float]] = {
            "Low": (-float("inf"), 30),
            "Moderate": (30, 60),
            "High": (60, float("inf")),
        }

        # Determine temperature category
        temperature_description = self._categorize_value(
            temperature, temperature_categories
        )

        # Determine humidity category
        humidity_description = self._categorize_value(humidity, humidity_categories)

        # Determine precipitation category
        precipitation_description = self._categorize_value(
            precipitation_probability, precipitation_categories
        )

        return {
            "temperature_description": temperature_description,
            "humidity_description": humidity_description,
            "precipitation_description": precipitation_description,
        }

    def _categorize_value(
        self, value: float, categories: Dict[str, Tuple[float, float]]
    ) -> str:
        """
        Categorizes the given value based on the provided categories.

        Args:
            value: The value to be categorized.
            categories: A dictionary containing the categories and their corresponding thresholds.

        Returns:
            The category that the value falls into.
        """
        for category, (lower_bound, upper_bound) in categories.items():
            if lower_bound < value <= upper_bound:
                return category
        return ""  # default return value in case no category is found


class WeatherRecommender:
    """
    A class that generates recommendations based on weather analysis.

    Example usage:
    ```python
    recommender = WeatherRecommender()
    weather_description = {
        "temperature_description": "Warm",
        "humidity_description": "Moderate",
        "precipitation_description": "Low",
    }
    recommendations = recommender.generate_recommendations(**weather_description)
    ```
    """

    def generate_recommendations(
        self,
        temperature_description: str,
        humidity_description: str,
        precipitation_description: str,
    ) -> Dict[str, Union[str, Dict[str, str], List[str]]]:
        """
        Generates recommendations based on the weather analysis.

        Args:
            temperature_description: The description of the temperature category.
            humidity_description: The description of the humidity category.
            precipitation_description: The description of the precipitation category.

        Returns:
            A dictionary containing the description and suggestions based on the weather parameters.
            The dictionary has the following structure:
            {
                "description": str,  # Description of the weather parameters
                "weather_descriptions": {
                    "temperature": str,  # Description of the temperature category
                    "humidity": str,  # Description of the humidity category
                    "precipitation": str,  # Description of the precipitation category
                },
                "suggestions": list,  # List of suggestions based on the weather parameters
            }
        """
        # Validate input data
        valid_categories = {"Cold", "Cool", "Mild", "Warm", "Hot"}
        if temperature_description not in valid_categories:
            raise ValueError(
                f"Invalid temperature category. Valid categories: {valid_categories}"
            )

        valid_categories = {"Low", "Moderate", "High"}
        if humidity_description not in valid_categories:
            raise ValueError(
                f"Invalid humidity category. Valid categories: {valid_categories}"
            )

        if precipitation_description not in valid_categories:
            raise ValueError(
                f"Invalid precipitation category. Valid categories: {valid_categories}"
            )

        # Generate suggestions based on the weather parameters
        suggestions = self._generate_suggestions(
            temperature_description, humidity_description, precipitation_description
        )

        return {
            "description": "Weather analysis and recommendations",
            "weather_descriptions": {
                "temperature": temperature_description,
                "humidity": humidity_description,
                "precipitation_probability": precipitation_description,
            },
            "suggestions": suggestions,
        }

    def _generate_suggestions(
        self, temperature: str, humidity: str, precipitation: str
    ) -> List[str]:
        """
        Generates suggestions based on the temperature, humidity, and precipitation.

        Args:
            temperature: The temperature category.
            humidity: The humidity category.
            precipitation: The precipitation category.

        Returns:
            A list of suggestions based on the weather parameters.
        """
        suggestions = []

        # Precipitation-based recommendations
        if precipitation == "High":
            suggestions.extend(
                ["May opt for indoor activities, if not, remember to carry an umbrella"]
            )
        else:
            suggestions.extend(["Suitable for outdoor activities. Have fun outside"])

        # Temperature-based recommendations
        if temperature == "Hot":
            suggestions.extend(
                ["Wear lightweight and breathable clothing", "Stay hydrated"]
            )
        elif temperature == "Warm":
            suggestions.append("Comfortable, casual clothing")
        elif temperature in ("Mild", "Cool"):
            suggestions.append("Light jacket or sweater")
        else:
            suggestions.append("Warm jacket, hat, and gloves")

        # Humidity-based recommendations
        if humidity == "High":
            suggestions.append("Stay hydrated")

        return suggestions
