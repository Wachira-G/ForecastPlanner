/**
 * Module: UserService
 * Description: Provides methods for making API requests related to user data using Axios library.
 *              Includes methods to retrieve public content and user-specific content.
 */
import axios from "axios";
import authHeader from "./auth-header";

// Base URL for the API endpoints
const API_URL = "https://forecast-planner-b6f6e7dba956.herokuapp.com/api/v1";

class UserService {
  /**
   * Method: getPublicContent
   * Description: Sends a GET request to the API endpoint to retrieve public content.
   * @returns {Promise} Promise object representing the request for public content
   */
  getPublicContent() {
    return axios.get(API_URL + "/all");
  }

  /**
   * Method: getUserBoard
   * Description: Sends a GET request to the API endpoint to retrieve user-specific content.
   *              Includes authorization header containing user's access token.
   * @returns {Promise} Promise object representing the request for user-specific content
   */
  getUserBoard() {
    return axios.get(API_URL + "/user", { headers: authHeader() });
  }
}

// Create an instance of UserService and export it
export default new UserService();
