import React, { Component } from "react";
import ProfileService from "../services/profile-service";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faSun, faCloudRain, faSnowflake, faWind } from "@fortawesome/free-solid-svg-icons";

export default class Weather extends Component {

  constructor(props) {
    super(props);
    this.state = {
      weatherData: [],
      cityInput: "",
    };
  }

  componentDidMount() {
     // Fetch weather data for default city (Nairobi)
     this.fetchWeatherData("Nairobi");
   }

   fetchWeatherData(city) {
  ProfileService.getWeatherContent(city)
    .then((response) => {
      this.setState({
        weatherData: response.data,
      });
    })
    .catch((error) => {
      console.error("Error fetching weather data:", error);
    });
}

handleCityInputChange = (event) => {
  this.setState({
    cityInput: event.target.value,
  });
};

handleSearch = () => {
  const { cityInput } = this.state;
  if (cityInput.trim() !== "") {
    this.fetchWeatherData(cityInput);
  }
};

getWeatherIcon = (weatherCode) => {
   switch (weatherCode) {
     case 0:
       return <FontAwesomeIcon icon={faSun} />;
     case weatherCode === 2 && weatherCode < 4 : //light
       return <FontAwesomeIcon icon={faCloudRain} />; //moderate
     case weatherCode === 4 && weatherCode < 6:
       return <FontAwesomeIcon icon={faCloudRain} />;
     default:
       return <FontAwesomeIcon icon={faCloudRain} />;
   }
 };

formatDate = (dateString) => {
  const date = new Date(dateString);
  const day = date.getDate();
  const month = date.getMonth() + 1;
  const year = date.getFullYear() % 10000; // Get last two digits of year
  return `${day < 10 ? "0" + day : day}-${month < 10 ? "0" + month : month}-${year}`;
};

  render() {
     const { weatherData, cityInput } = this.state;
  return (
    <div>
    <section className="p-5" id="weather">
      <div className="container weather-container-two">
        <div className="weather-input">
          <h4>Enter Name Of A City</h4>
          <input
            className="city-input"
            type="text"
            placeholder="E.g., Nairobi, Kisumu"
            value={cityInput}
            onChange={this.handleCityInputChange}
          />
          <button className="search-btn bg-warning" onClick={this.handleSearch}>
            Search
          </button>
          <div className="separator"></div>
          <button className="location-btn">Use Current Location</button>
        </div>
        <div className="weather-data" style={{ marginTop: '30px' }}>
          <div className="current-weather">
            <div className="details">
              {weatherData.length > 0 ? (
                <div>
                  <h2>{this.formatDate(weatherData[0].date_time)}</h2>
                  <h3>{weatherData[0].location_id}</h3>
                  <h6>Temperature: {weatherData[0].temperature}°C</h6>
                  <h6>Wind: {weatherData[0].wind_speed} M/S</h6>
                  <h6>Humidity: {weatherData[0].humidity}%</h6>
                  <h6>Precipitation: {weatherData[0].precipitation_probability} mm</h6>
                  {/* Add weather icon */}
                  <div>{this.getWeatherIcon(weatherData[0].precipitation_probabilit)}</div>
                </div>
              ) : (
                <p>Loading...</p>
              )}
            </div>
          </div>
        </div>
      </div>
    </section>

        </div>
      );
    };
}
