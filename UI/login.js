document.getElementById('loginButton').addEventListener('click', function() {
  const apiUrl = 'https://forecast-planner-b6f6e7dba956.herokuapp.com//api/v1/auth/login';

  const userData = {
    username: 'gabriel',
    password: 'password'
  };
  
  // Make a GET request
  fetch(apiUrl,  {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(userData)
  })
  
    .then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.json();
    })
    .then(data => {
      console.log(data);
      window.location.href = "landing.html";
    })
    .catch(error => {
      console.error('Error:', error);
    });
    });