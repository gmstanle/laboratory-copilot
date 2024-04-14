document.getElementById('submitBtn').addEventListener('click', function() {
    var userQuestion = document.getElementById('userQuestion').value; // Get the user's question
    fetch('/ask', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ question: userQuestion })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('answer').innerText = data.answer; // Display the answer
    })
    .catch(error => console.error('Error:', error));
});
