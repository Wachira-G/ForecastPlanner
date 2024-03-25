const signupForm = document.getElementById('signupForm');
const responseMessage = document.getElementById('response-message');

signupForm.addEventListener('submit', function (event) {
  event.preventDefault;

  const apiUrl = 'https://forecast-planner-b6f6e7dba956.herokuapp.com/api/v1/users';
  const formData = new FormData(signupForm);
  
  const requestOptions = {
    method: 'POST',
    body: formData.JSON.parse(),
  }

  console.log(requestOptions.body);

  fetch(apiUrl, requestOptions)
    .then((response) => {
      if(!response.ok){
        throw new Error(`HTTP error! status: ${response.status}`);
      } else{
        responseMessage('success', "Account created successfully!");
        setTimeout(()=> window.location.replace("/login"), 2000);
      }
    })
    .catch((error) => {
      console.log('There was a problem', error);
    });
});
