document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('#evaluate-rule-form');
    const result = document.querySelector('#evaluation-result');

    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const formData = new FormData(form);
        
        fetch(form.action, {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            result.textContent = data.eligible ? 'Eligible' : 'Not Eligible';
            result.className = data.eligible ? 'evaluation-result success' : 'evaluation-result error';
        })
        .catch(error => {
            console.error('Error:', error);
            result.textContent = 'An error occurred while evaluating the rule.';
            result.className = 'evaluation-result error';
        });
    });
});