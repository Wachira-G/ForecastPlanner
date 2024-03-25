// Define the API URL
const apiUrl = 'https://forecast-planner-b6f6e7dba956.herokuapp.com//api/v1/auth/login';

// Make a GET request
fetch(apiUrl)
  .then(response => {
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    return response.json();
  })
  .then(data => {
    console.log(data);
  })
  .catch(error => {
    console.error('Error:', error);
  });