import React, { Component } from "react";
import ProfileService from "../services/profile-service";

class Recommendation extends Component {
  constructor(props) {
    super(props);
    this.state = {
      recommendations: [],
      locationName: "",
    };
  }

  componentDidMount() {
    ProfileService.getUserProfile()
      .then(response => {
        const { user_id } = response.data;
        this.getCurrentDestination(user_id);
      })
      .catch(error => {
        console.error("Error fetching User:", error);
      });
  }

  getCurrentDestination(userId) {
    ProfileService.getCurrentDestination(userId)
      .then(response => {
        const { location_name, date, days } = response.data;
        this.setState({ locationName: location_name });
        this.getRecommendation(location_name, date, days);
      })
      .catch(error => {
        console.error("Error fetching current destination:", error);
      });
  }

  getRecommendation(locationName, date, days) {
    ProfileService.getRecommendation(locationName, date, days)
      .then(response => {
        this.setState({ recommendations: response.data });
      })
      .catch(error => {
        console.error("Error fetching recommendation:", error);
      });
  }

  render() {
    const { locationName, recommendations } = this.state;

    return (
      <div>
        <p className="text-warning bg-dark">CURRENT DESTINATION</p>
        <p>{locationName}</p>
        <p className="text-warning bg-info">WALLDROP SUGGESTION</p>
        {recommendations.map((recommendation, index) => (
          <div key={index}>
            <p>Weather: {recommendation.forecast.weather_descriptions.temperature}</p>
            <p>Walldrop: {recommendation.recommendations.suggestions.join(', ')}</p>
          </div>
        ))}
      </div>
    );
  }
}

export default Recommendation;
