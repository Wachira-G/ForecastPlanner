/**
 * Action Creators: setMessage, clearMessage
 * Description: Define action creators for setting and clearing messages in the application.
 */

// Import action types
import { SET_MESSAGE, CLEAR_MESSAGE } from "./types";

/**
 * Action Creator: setMessage
 * Description: Dispatches an action to set a message in the application state.
 * @param {string} message - The message to be set
 * @returns {Object} Action object containing the type and payload (message)
 */
export const setMessage = (message) => ({
  type: SET_MESSAGE,
  payload: message,
});

/**
 * Action Creator: clearMessage
 * Description: Dispatches an action to clear the message in the application state.
 * @returns {Object} Action object with type CLEAR_MESSAGE
 */
export const clearMessage = () => ({
  type: CLEAR_MESSAGE,
});
