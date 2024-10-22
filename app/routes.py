from flask import jsonify, request, render_template
from app import app, db
from app.models import Rule
from app.utils import RuleParser
import json

rule_parser = RuleParser()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/rules', methods=['GET'])
def get_rules():
    rules = Rule.query.all()
    return jsonify([rule.to_dict() for rule in rules])

@app.route('/api/rules', methods=['POST'])
def create_rule():
    data = request.get_json()
    
    try:
        # Parse and validate the rule
        ast = rule_parser.create_rule(data['rule_string'])
        
        # Create new rule
        rule = Rule(
            name=data['name'],
            description=data.get('description', ''),
            rule_string=data['rule_string'],
            ast_json=json.dumps(ast.to_dict())
        )
        
        db.session.add(rule)
        db.session.commit()
        
        return jsonify(rule.to_dict()), 201
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/rules/evaluate', methods=['POST'])
def evaluate_rule():
    data = request.get_json()
    
    try:
        rule_id = data['rule_id']
        user_data = data['data']
        
        rule = Rule.query.get_or_404(rule_id)
        ast = json.loads(rule.ast_json)
        
        result = rule_parser.evaluate_rule(ast, user_data)
        
        return jsonify({
            'result': result,
            'rule_id': rule_id,
            'rule_name': rule.name
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/rules/combine', methods=['POST'])
def combine_rules():
    data = request.get_json()
    
    try:
        rule_ids = data['rule_ids']
        operator = data.get('operator', 'AND')
        
        rules = Rule.query.filter(Rule.id.in_(rule_ids)).all()
        rule_strings = [rule.rule_string for rule in rules]
        
        combined_ast = rule_parser.combine_rules(rule_strings, operator)
        
        return jsonify({
            'combined_ast': combined_ast.to_dict(),
            'rule_ids': rule_ids
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400