#!/usr/bin/env python3

import unittest
from services.recommendation_service import WeatherAnalyzer, WeatherRecommender


class TestWeatherAnalyzer(unittest.TestCase):
    def test_analyze_weather(self):
        analyzer = WeatherAnalyzer()
        weather_data = {
            "temperature": 28.70,
            "humidity": 84.40,
            "precipitation_probability": 0.00,
        }
        analysis = analyzer.analyze_weather(**weather_data)
        self.assertIsInstance(analysis, dict)
        self.assertIn("temperature_description", analysis)
        self.assertIn("humidity_description", analysis)
        self.assertIn("precipitation_description", analysis)

        recommendations = WeatherRecommender().generate_recommendations(**analysis)
        self.assertIsInstance(recommendations, dict)
        self.assertIn("description", recommendations)
        self.assertIn("suggestions", recommendations)
        self.assertIn("weather_descriptions", recommendations)


if __name__ == "__main__":
    unittest.main()
