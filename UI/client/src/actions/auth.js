/**
 * Action Creators: register, login, logout
 * Description: Define action creators for user registration, login, and logout.
 *              These actions interact with the AuthService to make API requests and dispatch corresponding actions.
 */

// Import action types
import {
  REGISTER_SUCCESS,
  REGISTER_FAIL,
  LOGIN_SUCCESS,
  LOGIN_FAIL,
  LOGOUT,
  SET_MESSAGE,
} from "./types";

// Import AuthService for making API requests
import AuthService from "../services/auth-service";

/**
 * Action Creator: register
 * Description: Dispatches actions for user registration.
 * @param {string} phone - User's phone number
 * @param {string} email - User's email address
 * @param {string} password - User's password
 * @returns {Promise} Promise object representing the registration request
 */
export const register = (phone, email, password) => (dispatch) => {
  return AuthService.register(phone, email, password).then(
    (response) => {
      // Dispatch REGISTER_SUCCESS action
      dispatch({
        type: REGISTER_SUCCESS,
      });

      // Dispatch SET_MESSAGE action with success message
      dispatch({
        type: SET_MESSAGE,
        payload: response.data.message,
      });

      return Promise.resolve();
    },
    (error) => {
      // Extract error message from error response
      const message =
        (error.response &&
          error.response.data &&
          error.response.data.message) ||
        error.message ||
        error.toString();

      // Dispatch REGISTER_FAIL action
      dispatch({
        type: REGISTER_FAIL,
      });

      // Dispatch SET_MESSAGE action with error message
      dispatch({
        type: SET_MESSAGE,
        payload: message,
      });

      return Promise.reject();
    }
  );
};

/**
 * Action Creator: login
 * Description: Dispatches actions for user login.
 * @param {string} phone - User's phone number
 * @param {string} password - User's password
 * @returns {Promise} Promise object representing the login request
 */
export const login = (phone, password) => (dispatch) => {
  return AuthService.login(phone, password).then(
    (data) => {
      // Dispatch LOGIN_SUCCESS action with user data
      dispatch({
        type: LOGIN_SUCCESS,
        payload: { user: data },
      });

      return Promise.resolve();
    },
    (error) => {
      // Extract error message from error response
      const message =
        (error.response &&
          error.response.data &&
          error.response.data.message) ||
        error.message ||
        error.toString();

      // Dispatch LOGIN_FAIL action
      dispatch({
        type: LOGIN_FAIL,
      });

      // Dispatch SET_MESSAGE action with error message
      dispatch({
        type: SET_MESSAGE,
        payload: message,
      });

      return Promise.reject();
    }
  );
};

/**
 * Action Creator: logout
 * Description: Dispatches action for user logout.
 * @returns {void}
 */
export const logout = () => (dispatch) => {
  // Call logout method from AuthService
  AuthService.logout();

  // Dispatch LOGOUT action
  dispatch({
    type: LOGOUT,
  });
};
