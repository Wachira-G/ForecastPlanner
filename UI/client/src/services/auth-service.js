/**
 * Module: AuthService
 * Description: Handles authentication-related API requests using Axios library.
 *              Provides methods for user authentication (login and register) and logout functionality.
 */
import axios from "axios";

// Base URL for the API endpoints
const API_URL = "https://forecast-planner-b6f6e7dba956.herokuapp.com/api/v1";

class AuthService {
  /**
   * Method: login
   * Description: Sends a POST request to the API endpoint for user login with provided phone number and password.
   *              If login is successful, stores user data in the browser's localStorage.
   * @param {string} phone - User's phone number
   * @param {string} password - User's password
   * @returns {Promise} Promise object representing the login request
   */
  login(phone, password) {
    return axios
      .post(API_URL + "/signin", { phone, password })
      .then((response) => {
        if (response.data.accessToken) {
          // If login successful, store user data in localStorage
          localStorage.setItem("user", JSON.stringify(response.data));
        }
        return response.data;
      });
  }

  /**
   * Method: logout
   * Description: Removes user data from the browser's localStorage, effectively logging the user out.
   */
  logout() {
    // Remove user data from localStorage
    localStorage.removeItem("user");
  }

  /**
   * Method: register
   * Description: Sends a POST request to the API endpoint for user registration with provided phone number, email, and password.
   * @param {string} phone - User's phone number
   * @param {string} email - User's email address
   * @param {string} password - User's password
   * @returns {Promise} Promise object representing the registration request
   */
  register(phone, email, password) {
    return axios.post(API_URL + "/signup", {
      phone,
      email,
      password,
    });
  }
}

// Create an instance of AuthService and export it
export default new AuthService();
