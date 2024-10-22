from app import db
from datetime import datetime
import json

class Rule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500))
    rule_string = db.Column(db.Text, nullable=False)
    ast_json = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'rule_string': self.rule_string,
            'ast_json': json.loads(self.ast_json),
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }