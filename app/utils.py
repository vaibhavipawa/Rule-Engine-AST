import re
from typing import Dict, Any, Union, List

class Node:
    def __init__(self, type_: str, value: Any = None, left=None, right=None):
        self.type = type_
        self.value = value
        self.left = left
        self.right = right
    
    def to_dict(self) -> Dict:
        result = {'type': self.type}
        if self.value is not None:
            result['value'] = self.value
        if self.left:
            result['left'] = self.left.to_dict()
        if self.right:
            result['right'] = self.right.to_dict()
        return result

class RuleParser:
    def __init__(self):
        self.operators = {'AND', 'OR'}
        self.comparisons = {'>', '<', '=', '>=', '<=', '!='}
    
    def tokenize(self, rule_string: str) -> List[str]:
        # Replace parentheses with spaces around them
        rule_string = re.sub(r'([()])', r' \1 ', rule_string)
        return rule_string.split()
    
    def parse_condition(self, condition: str) -> Node:
        # Parse single conditions like "age > 30" or "department = 'Sales'"
        for op in self.comparisons:
            if op in condition:
                field, value = condition.split(op)
                return Node(
                    type_="condition",
                    value={
                        'field': field.strip(),
                        'operator': op,
                        'value': eval(value.strip())  # Safely evaluate string values
                    }
                )
        raise ValueError(f"Invalid condition: {condition}")
    
    def create_rule(self, rule_string: str) -> Node:
        tokens = self.tokenize(rule_string)
        return self._parse_expression(tokens)
    
    def _parse_expression(self, tokens: List[str], start: int = 0) -> Union[Node, tuple]:
        if not tokens:
            raise ValueError("Empty expression")
        
        stack = []
        current_expr = ""
        i = start
        
        while i < len(tokens):
            token = tokens[i]
            
            if token == '(':
                sub_expr, new_i = self._parse_expression(tokens, i + 1)
                stack.append(sub_expr)
                i = new_i
            elif token == ')':
                if current_expr:
                    stack.append(self.parse_condition(current_expr))
                return stack[-1], i + 1
            elif token in self.operators:
                if current_expr:
                    stack.append(self.parse_condition(current_expr))
                    current_expr = ""
                
                right_expr, new_i = self._parse_expression(tokens, i + 1)
                left_node = stack.pop()
                stack.append(Node(type_="operator", value=token, left=left_node, right=right_expr))
                i = new_i - 1
            else:
                current_expr += " " + token
            
            i += 1
        
        if current_expr:
            stack.append(self.parse_condition(current_expr.strip()))
        
        return stack[-1]
    
    def evaluate_rule(self, node: Dict, data: Dict) -> bool:
        if node['type'] == 'operator':
            left_result = self.evaluate_rule(node['left'], data)
            right_result = self.evaluate_rule(node['right'], data)
            
            if node['value'] == 'AND':
                return left_result and right_result
            elif node['value'] == 'OR':
                return left_result or right_result
        
        elif node['type'] == 'condition':
            field = node['value']['field']
            operator = node['value']['operator']
            value = node['value']['value']
            
            if field not in data:
                raise ValueError(f"Field {field} not found in data")
            
            data_value = data[field]
            
            if operator == '>':
                return data_value > value
            elif operator == '<':
                return data_value < value
            elif operator == '=':
                return data_value == value
            elif operator == '>=':
                return data_value >= value
            elif operator == '<=':
                return data_value <= value
            elif operator == '!=':
                return data_value != value
        
        raise ValueError(f"Invalid node type: {node['type']}")
    
    def combine_rules(self, rules: List[str], operator: str = 'AND') -> Node:
        if not rules:
            raise ValueError("Empty rules list")
        
        if len(rules) == 1:
            return self.create_rule(rules[0])
        
        combined_node = self.create_rule(rules[0])
        
        for rule in rules[1:]:
            rule_node = self.create_rule(rule)
            combined_node = Node(
                type_="operator",
                value=operator,
                left=combined_node,
                right=rule_node
            )
        
        return combined_node