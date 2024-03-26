/**
 * Component: AuthVerify
 * Description: Monitors changes in the browser history and verifies the authentication status of the user.
 *              If the user's access token has expired, it triggers a logout action.
 */
import React, { Component } from "react";
import { history } from '../helpers/history';

/**
 * Function: parseJwt
 * Description: Parses and decodes a JWT token to extract its payload.
 * @param {string} token - The JWT token to be parsed
 * @returns {object|null} The decoded JWT payload object, or null if parsing fails
 */
const parseJwt = (token) => {
  try {
    return JSON.parse(atob(token.split('.')[1]));
  } catch (e) {
    return null;
  }
};

class AuthVerify extends Component {
  constructor(props) {
    super(props);

    // Listen for changes in the browser history
    history.listen(() => {
      // Retrieve user data from localStorage
      const user = JSON.parse(localStorage.getItem("user"));

      if (user) {
        // Parse and decode the JWT token
        const decodedJwt = parseJwt(user.accessToken);

        // Check if the token has expired
        if (decodedJwt.exp * 1000 < Date.now()) {
          // If token has expired, trigger logout action
          props.logOut();
        }
      }
    });
  }

  render() {
    // This component does not render anything visible
    return <div></div>;
  }
}

// Export the AuthVerify component
export default AuthVerify;
