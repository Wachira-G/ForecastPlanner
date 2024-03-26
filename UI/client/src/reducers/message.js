/**
 * Reducer: messageReducer
 * Description: Handles state changes related to message display based on dispatched actions.
 * @param {Object} state - Current message state, defaults to an empty object
 * @param {Object} action - Dispatched action object containing type and payload
 * @returns {Object} Updated message state based on the dispatched action
 */
import { SET_MESSAGE, CLEAR_MESSAGE } from "../actions/types";

// Initial state for message display
const initialState = {};

export default function messageReducer(state = initialState, action) {
  const { type, payload } = action;

  switch (type) {
    case SET_MESSAGE:
      // Update state to set the message
      return { message: payload };

    case CLEAR_MESSAGE:
      // Update state to clear the message
      return { message: "" };

    default:
      // Return current state for unknown actions
      return state;
  }
}
