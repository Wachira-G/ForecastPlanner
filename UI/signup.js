const apiUrl = 'https://forecast-planner-b6f6e7dba956.herokuapp.com/api/v1/users';
        
        const signupForm = document.getElementById('signupForm');
        const responseMessage = document.getElementById('response-message');

        signupForm.addEventListener('submit', function (event) {
          event.preventDefault();

          const formData = new FormData(signupForm);

          const requestOptions = {
            method: 'POST',
            body: formData,
          };

          fetch(apiUrl, requestOptions)
            .then(response => {
              if (!response.ok) {
                throw new Error('Network response was not ok');
              }
              return response.text("Succesfullu Signed Up!");
            })
            .then(data => {
              responseMessage.textContent = data;
            })
            .catch(error => {
              console.error('Error:', error);
            });
        });