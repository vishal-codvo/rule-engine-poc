from dataclasses import dataclass
from typing import Optional
from sqlalchemy import text
from sqlalchemy.sql import text as sql_text

@dataclass
class SensorRule:
    sensor_id: str
    rule_type: str
    min_value: Optional[float]
    max_value: Optional[float]
    action: str
    trigger_message: str

class RuleConfig:
    def __init__(self):
        self.rules = {}

    async def load_rules_from_db(self, db_session):
        """Load rules from database"""
        query = sql_text("""
            SELECT sensor_id, rule_type, min_value, max_value, action, trigger_message 
            FROM sensor_rules;
        """)
        result = db_session.execute(query)
        
        # Get column names from result
        columns = result.keys()
        
        for row in result:
            # Convert row tuple to dictionary using column names
            rule_dict = dict(zip(columns, row))
            
            self.rules[rule_dict['sensor_id']] = SensorRule(
                sensor_id=rule_dict['sensor_id'],
                rule_type=rule_dict['rule_type'],
                min_value=rule_dict['min_value'],
                max_value=rule_dict['max_value'],
                action=rule_dict['action'],
                trigger_message=rule_dict['trigger_message']
            ) 