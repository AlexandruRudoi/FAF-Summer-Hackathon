document.getElementById('compare').addEventListener('click', () => {
  const url1 = document.getElementById('url1').value;
  const url2 = document.getElementById('url2').value;
  fetch(`http://127.0.0.1:8080/api/comparative`, {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json'
      },
      body: JSON.stringify({ url1: url1, url2: url2 })
  })
  .then(response => response.json())
  .then(data => {
      document.getElementById('inputArea').style.display = 'none'; // Hide input area
      const resultArea = document.getElementById('result');
      resultArea.classList.remove('hidden');
      resultArea.innerHTML = ''; // Clear previous results
      // Check if data contains expected response1 and response2
      if (data.response1 && data.response2) {
          resultArea.innerHTML += `<div class="data-item">${JSON.stringify(data.response1, null, 4)}</div>`;
          resultArea.innerHTML += `<div class="data-item">${JSON.stringify(data.response2, null, 4)}</div>`;
      } else {
          resultArea.textContent = 'No data available';
      }
  })
  .catch(error => {
      console.error('Error:', error);
      document.getElementById('result').innerText = 'Failed to fetch data';
  });
});
