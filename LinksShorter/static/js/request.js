document.getElementById('sendRequestBtn').addEventListener('click', function() {
  const apiUrl = 'http://192.168.1.4:5000/addurl';
  fetch(apiUrl)
      .then(response => {
          if (!response.ok) {
              throw new Error('Network response was not ok');
          }
          return response.json();
      })
      .then(data => {
          document.getElementById('responseOutput').innerHTML = `
              <h3>Response Data:</h3>
              <pre>${JSON.stringify(data, null, 2)}</pre>
          `;
      })
      .catch(error => {
          document.getElementById('responseOutput').innerHTML = `
              <h3>Error:</h3>
              <p>${error.message}</p>
          `;
      });
});
