/**
 * Reducer: authReducer
 * Description: Handles authentication-related state changes based on dispatched actions.
 *              Updates the state to reflect login status and user information.
 * @param {Object} state - Current authentication state, defaults to initialState
 * @param {Object} action - Dispatched action object containing type and payload
 * @returns {Object} Updated authentication state based on the dispatched action
 */
import {
  REGISTER_SUCCESS,
  REGISTER_FAIL,
  LOGIN_SUCCESS,
  LOGIN_FAIL,
  LOGOUT,
} from "../actions/types";

// Retrieve user data from localStorage
const user = JSON.parse(localStorage.getItem("user"));

// Initial state for authentication
const initialState = user
  ? { isLoggedIn: true, user }
  : { isLoggedIn: false, user: null };

export default function authReducer(state = initialState, action) {
  const { type, payload } = action;

  switch (type) {
    case REGISTER_SUCCESS:
      // Update state on successful registration
      return {
        ...state,
        isLoggedIn: false,
      };
    case REGISTER_FAIL:
      // Update state on registration failure
      return {
        ...state,
        isLoggedIn: false,
      };
    case LOGIN_SUCCESS:
      // Update state on successful login
      return {
        ...state,
        isLoggedIn: true,
        user: payload.user,
      };
    case LOGIN_FAIL:
      // Update state on login failure
      return {
        ...state,
        isLoggedIn: false,
        user: null,
      };
    case LOGOUT:
      // Update state on logout
      return {
        ...state,
        isLoggedIn: false,
        user: null,
      };
    default:
      // Return current state for unknown actions
      return state;
  }
}
