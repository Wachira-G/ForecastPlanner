import axios from "axios";
import authHeader from "./auth-header";

// Base URL for the API endpoints
const API_URL = "https://forecast-planner-b6f6e7dba956.herokuapp.com/api/v1";

/**
 * Class: ProfileService
 * Description: Provides methods for making API requests related to user profile data using Axios library.
 *              Includes methods to retrieve weather content, user profile, and post destination data.
 */
class ProfileService {
  /**
   * Method: getWeatherContent
   * Description: Sends a GET request to the API endpoint to retrieve weather content for a specific location.
   * @param {string} location_name - The name of the location to retrieve weather content for
   * @returns {Promise} Promise object representing the request for weather content
   */
  static getWeatherContent(location_name) {
    return axios.get(API_URL + "/five-day_weather", {
      params: {
        location_name: location_name
      }
    });
  }

  /**
   * Method: getUserProfile
   * Description: Sends a GET request to the API endpoint to retrieve user profile information.
   *              Includes authorization header containing user's access token.
   * @returns {Promise} Promise object representing the request for user profile information
   */
  static getUserProfile() {
    return axios.get(API_URL + "/auth/me", { headers: authHeader() });
  }

  /**
   * Method: destination
   * Description: Sends a POST request to the API endpoint to post destination data.
   * @param {string} location_name - The name of the destination location
   * @param {string} date - The date of the destination
   * @param {number} days - The number of days for the destination
   * @returns {Promise} Promise object representing the request to post destination data
   */
  static destination(location_name, date, days) {
    return axios.post(API_URL + "/post-destination", {
      location_name,
      date,
      days,
    });
  }

  /**
   * Method: getCurrentDestination
   * Description: Sends a GET request to the API endpoint to retrieve the current destination for a user.
   * @param {string} userId - The ID of the user
   * @returns {Promise} Promise object representing the request for the current destination
   */
  static getCurrentDestination(userId) {
    return axios.get(API_URL + "/current-destination", {
      params: {
        user_id: userId
      }
    });
  }

  /**
   * Method: getPastDestinations
   * Description: Sends a GET request to the API endpoint to retrieve the destination for a user.
   * @param {string} userId - The ID of the user
   * @returns {Promise} Promise object representing the request for the destination
   */
  static getPastDestinations(userId) {
    return axios.get(API_URL + "/destination", {
      params: {
        user_id: userId
      }
    });
  }


  /**
   * Method: getRecommendation
   * Description: Sends a GET request to the API endpoint to retrieve recommendations for a specific location, date, and duration.
   * @param {string} location_name - The name of the location
   * @param {string} date - The date
   * @param {number} days - The duration
   * @returns {Promise} Promise object representing the request for recommendations
   */
  static getRecommendation(location_name, date, days) {
    return axios.get(API_URL + "/weather_and_recommendation", {
      params: {
        location_name: location_name,
        date: date,
        days: days
      }
    });
  }
}

export default ProfileService;
