from business_rules import run_all
from business_rules.actions import BaseActions
from business_rules.fields import FIELD_NUMERIC
from business_rules.variables import BaseVariables, numeric_rule_variable
import asyncio

class SensorVariables(BaseVariables):
    def __init__(self, sensor_data):
        self.sensor_data = sensor_data

    @numeric_rule_variable
    def value(self):
        return self.sensor_data['value']

class SensorActions(BaseActions):
    def __init__(self, nats_service):
        self.nats_service = nats_service

    def publish_alarm(self, sensor_id: str, trigger: str, action: str):
        # Create a new event loop for this synchronous context
        loop = asyncio.get_event_loop()
        alarm_message = {
            'sensor_id': sensor_id,
            'trigger': trigger,
            'action': action
        }
        # Run the async publish in the event loop
        loop.create_task(self.nats_service.publish('sensor.alarm', alarm_message))


class RuleEngine:
    def __init__(self, rule_config, nats_service):
        self.rule_config = rule_config
        self.nats_service = nats_service

    async def evaluate_rules(self, sensor_data):
        sensor_id = sensor_data['sensor_id']
        rule = self.rule_config.rules.get(sensor_id)
        
        if not rule:
            return
            
        rules = []
        if rule.max_value is not None:
            rules.append({
                'conditions': {
                    'all': [{
                        'name': 'value',
                        'operator': 'greater_than',
                        'value': rule.max_value
                    }]
                },
                'actions': [{
                    'name': 'publish_alarm',
                    'params': {
                        'sensor_id': sensor_id,
                        'trigger': rule.trigger_message,
                        'action': rule.action
                    }
                }]
            })
            
        if rule.min_value is not None:
            rules.append({
                'conditions': {
                    'all': [{
                        'name': 'value',
                        'operator': 'less_than',
                        'value': rule.min_value
                    }]
                },
                'actions': [{
                    'name': 'publish_alarm',
                    'params': {
                        'sensor_id': sensor_id,
                        'trigger': rule.trigger_message,
                        'action': rule.action
                    }
                }]
            })

        variables = SensorVariables(sensor_data)
        actions = SensorActions(self.nats_service)
        
        for rule in rules:
            run_all(rule_list=[rule],
                   defined_variables=variables,
                   defined_actions=actions) 