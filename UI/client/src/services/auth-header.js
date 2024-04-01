/**
 * Function: authHeader
 * Description: Generates an authorization header for API requests based on the user's access token stored in the browser's localStorage.
 * @returns {Object} Authorization header object containing the access token in the format "Bearer {accessToken}" if user object and accessToken are present, otherwise returns an empty object.
 */
export default function authHeader() {
  // Retrieve user object from localStorage and parse it as JSON
  const user = JSON.parse(localStorage.getItem("user"));

  // Check if user object and accessToken property are present
  if (user && user.access_token) {
    // If present, construct and return authorization header with the access token
    return { "Authorization": "Bearer " + user.access_token };
  } else {
    // If user object or accessToken is missing, return an empty object
    return {};
  }
}
