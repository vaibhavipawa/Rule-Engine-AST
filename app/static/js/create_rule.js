document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('#create-rule-form');
    const ruleString = document.querySelector('#rule_string');
    const errorMessage = document.querySelector('#error-message');

    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Simple client-side validation
        if (!validateRule(ruleString.value)) {
            errorMessage.textContent = 'Invalid rule syntax. Please check your rule.';
            return;
        }

        // If validation passes, submit the form
        form.submit();
    });

    function validateRule(rule) {
        // This is a simple validation. You might want to implement a more robust one.
        const operators = ['AND', 'OR'];
        const comparators = ['>', '<', '>=', '<=', '='];
        
        let tokens = rule.match(/\(|\)|\w+|'[^']+'|[<>=]+/g);
        
        if (!tokens) return false;

        let openParenCount = 0;
        let expectOperand = true;

        for (let token of tokens) {
            if (token === '(') {
                openParenCount++;
            } else if (token === ')') {
                if (openParenCount === 0) return false;
                openParenCount--;
            } else if (operators.includes(token)) {
                if (expectOperand) return false;
                expectOperand = true;
            } else if (comparators.includes(token)) {
                if (!expectOperand) return false;
                expectOperand = true;
            } else {
                if (!expectOperand) return false;
                expectOperand = false;
            }
        }

        return openParenCount === 0 && !expectOperand;
    }
});
