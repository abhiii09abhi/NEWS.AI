// API URL - change this if your backend runs on a different address
const API_URL = 'http://127.0.0.1:5000';

async function getStability() {
  const countryCode = document.getElementById('country').value || 'in';
  const resultsDiv = document.getElementById('results');
  const loadingDiv = document.getElementById('loading');
  const errorDiv = document.getElementById('error');

  // Clear previous results and errors
  resultsDiv.innerHTML = "";
  errorDiv.innerHTML = "";

  // Show loading message
  loadingDiv.style.display = 'block';

  try {
    const response = await fetch(`${API_URL}/predict_live?country=${countryCode}`);

    if (!response.ok) {
      throw new Error(`${response.status} ${response.statusText}`);
    }

    const data = await response.json();

    // Hide loading message
    loadingDiv.style.display = 'none';

    if (data.length === 0) {
      resultsDiv.innerHTML = `<p>No news found for country code: ${countryCode}</p>`;
      return;
    }

    // Display results
    data.forEach((item, index) => {
      const statusClass = item.prediction === "At Risk" ? "risk" : "safe";

      // Format explanation list items
      let explanationHtml = "";
      if (item.explanation && item.explanation.length > 0) {
        explanationHtml = item.explanation
          .map(ex => `<li>${ex[0]} (${typeof ex[1] === 'number' ? ex[1].toFixed(3) : ex[1]})</li>`)
          .join("");
      } else {
        explanationHtml = "<li>No explanation available</li>";
      }

      // Create result card
      resultsDiv.innerHTML += `
        <div class="card">
          <h3>News ${index + 1}</h3>
          <p><strong>Text:</strong> ${item.text}</p>
          <p><strong>Status:</strong> <span class="${statusClass}">${item.prediction}</span></p>
          <p><strong>Confidence:</strong> ${item.confidence.toFixed(2)}</p>
          <p><strong>Key Factors:</strong></p>
          <ul>${explanationHtml}</ul>
          <p><a href="${item.url}" target="_blank">Read Full Article</a></p>
        </div>
      `;
    });

  } catch (error) {
    // Hide loading message
    loadingDiv.style.display = 'none';

    // Show error message
    errorDiv.innerHTML = `
      <div class="error">
        <p>Error fetching results: ${error.message}</p>
        <p>Make sure the backend server is running at ${API_URL}</p>
      </div>
    `;
    console.error('Error:', error);
  }
}

// Optional: Add event listener for Enter key on the input field
document.getElementById('country').addEventListener('keypress', function(event) {
  if (event.key === 'Enter') {
    getStability();
  }
});