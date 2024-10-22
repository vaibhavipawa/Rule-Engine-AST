# Rule Engine with AST

A flexible and powerful rule engine application that uses Abstract Syntax Trees (AST) to represent and evaluate conditional rules. This system allows for dynamic creation, combination, and modification of business rules based on various attributes like age, department, income, etc.

## Features

- Create complex conditional rules using a simple string syntax
- Convert rule strings into Abstract Syntax Trees (AST) for efficient evaluation
- Combine multiple rules with AND/OR operators
- Evaluate rules against user data
- Store rules in a SQLite database
- RESTful API for rule management
- Web interface for rule creation and evaluation
- Support for various comparison operators (>, <, =, >=, <=, !=)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/rule-engine.git
cd rule-engine
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

4. Set up the database:
```bash
flask db init
flask db migrate
flask db upgrade
```

## Project Structure
```
rule_engine/
│
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── routes.py
│   ├── utils.py
│   ├── static/
│   │   ├── css/
│   │   │   └── custom.css
│   │   └── js/
│   │       ├── create_rule.js
│   │       └── evaluate_rule.js
│   └── templates/
│       ├── base.html
│       ├── index.html
│       ├── create_rule.html
│       └── evaluate_rule.html
├── config.py
├── run.py
└── requirements.txt
```

## Usage

1. Start the application:
```bash
python run.py
```

2. Access the web interface at `http://localhost:5000`

### Creating Rules

Rules can be created using a simple string syntax. Here are some examples:

```
# Simple rule
age > 30 AND department = 'Sales'

# Complex rule
((age > 30 AND department = 'Sales') OR (age < 25 AND department = 'Marketing')) AND (salary > 50000 OR experience > 5)
```

### API Endpoints

#### Create Rule
```http
POST /api/rules
Content-Type: application/json

{
    "name": "Sales Rule",
    "description": "Rule for sales department",
    "rule_string": "age > 30 AND department = 'Sales'"
}
```

#### Evaluate Rule
```http
POST /api/rules/evaluate
Content-Type: application/json

{
    "rule_id": 1,
    "data": {
        "age": 35,
        "department": "Sales",
        "salary": 60000,
        "experience": 3
    }
}
```

#### Combine Rules
```http
POST /api/rules/combine
Content-Type: application/json

{
    "rule_ids": [1, 2],
    "operator": "AND"
}
```

## Data Structure

### Node Class
The AST is built using a Node class with the following structure:
```python
class Node:
    def __init__(self, type_, value=None, left=None, right=None):
        self.type = type_      # "operator" or "condition"
        self.value = value     # operator value or condition details
        self.left = left       # left child node
        self.right = right     # right child node
```

### Database Schema
```sql
CREATE TABLE rule (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    description VARCHAR(500),
    rule_string TEXT NOT NULL,
    ast_json TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

## Testing

Run the test suite:
```bash
python -m pytest tests/
```

Example test cases are provided for:
- Rule creation
- Rule combination
- Rule evaluation
- Error handling
- Edge cases

## Error Handling

The system includes comprehensive error handling for:
- Invalid rule syntax
- Missing attributes in evaluation data
- Invalid operators
- Database errors
- Invalid API requests

## Limitations

- Nested functions are not supported in the current version
- All attribute values must be strings or numbers
- Complex date operations are not supported natively

## Future Enhancements

- Support for custom functions in rules
- Additional operators (CONTAINS, IN, etc.)
- Rule versioning
- Rule templates
- Performance optimizations for large rule sets
- Support for date/time operations
- Rule dependency tracking
- Rule validation against attribute catalog

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Flask documentation
- SQLAlchemy documentation
- Python AST module documentation

## Support

For support, please open an issue in the GitHub repository or contact the maintainers.
