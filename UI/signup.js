const apiUrl = 'https://forecast-planner-b6f6e7dba956.herokuapp.com//api/v1/users';

const contactForm = document.getElementById('signupForm');
const responseMessage = document.getElementById('response-message');

contactForm.addEventListener('submit', function (event) {
  event.preventDefault();

  const formData = new FormData(SignupForm);

  const requestOptions = {
    method: 'POST',
    body: formData,
  };

  fetch(apiUrl, requestOptions)
    .then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.text();
    })
    .then(data => {
      responseMessage.textContent = data;
    })
    .catch(error => {
      console.error('Error:', error);
    });
});