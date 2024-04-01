import {
  REGISTER_SUCCESS,
  REGISTER_FAIL,
  LOGIN_SUCCESS,
  LOGIN_FAIL,
  LOGOUT,
  SET_MESSAGE,
} from "./types";

// Import AuthService for making API requests
import ProfileService from "../services/profile-service";

export const destination = (location_name, date, days) => (dispatch) => {
  return ProfileService.destination(location_name, date, days).then(
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
