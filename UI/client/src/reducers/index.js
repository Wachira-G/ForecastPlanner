/**
 * Module: rootReducer
 * Description: Combines multiple reducers into a single reducer using combineReducers method from Redux.
 *              The combined reducer manages the state of the entire application.
 */

import { combineReducers } from "redux";
import auth from "./auth";
import message from "./message";

// Combine individual reducers into a single reducer
export default combineReducers({
  auth, // Authentication reducer
  message, // Message reducer
});
