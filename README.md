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
https://github.com/vaibhavipawa/Rule-Engine-AST.git
cd Rule-Engine-AST
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
