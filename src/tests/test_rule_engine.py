import pytest
from src.services.rule_engine import RuleEngine, SensorVariables, SensorActions
from src.config.rules_config import RuleConfig, SensorRule
from src.services.nats_service import NatsService

@pytest.fixture
def rule_config():
    config = RuleConfig()
    # Add test rules
    config.rules["Temperature-101"] = SensorRule(
        sensor_id="Temperature-101",
        rule_type="temperature",
        min_value=None,
        max_value=120.0,
        action="lower fuel",
        trigger_message="temperature beyond threshold"
    )
    return config

@pytest.fixture
def nats_service():
    return NatsService("nats://localhost:4222")

@pytest.fixture
def rule_engine(rule_config, nats_service):
    return RuleEngine(rule_config, nats_service)

@pytest.mark.asyncio
async def test_rule_evaluation_above_threshold(rule_engine):
    """Test rule evaluation when value is above threshold"""
    test_data = {
        "sensor_id": "Temperature-101",
        "value": 130.0
    }
    
    # Capture published alarms
    published_alarms = []
    async def mock_publish(subject, message):
        published_alarms.append((subject, message))
    rule_engine.nats_service.publish = mock_publish
    
    await rule_engine.evaluate_rules(test_data)
    assert len(published_alarms) == 1
    subject, message = published_alarms[0]
    assert subject == "sensor.alarm"
    assert message["sensor_id"] == "Temperature-101"
    assert message["action"] == "lower fuel"

@pytest.mark.asyncio
async def test_rule_evaluation_below_threshold(rule_engine):
    """Test rule evaluation when value is below threshold"""
    test_data = {
        "sensor_id": "Temperature-101",
        "value": 110.0
    }
    
    published_alarms = []
    rule_engine.nats_service.publish = lambda subject, message: published_alarms.append(message)
    
    await rule_engine.evaluate_rules(test_data)
    assert len(published_alarms) == 0

@pytest.mark.asyncio
async def test_unknown_sensor(rule_engine):
    """Test rule evaluation for unknown sensor"""
    test_data = {
        "sensor_id": "Unknown-Sensor",
        "value": 100.0
    }
    
    published_alarms = []
    rule_engine.nats_service.publish = lambda subject, message: published_alarms.append(message)
    
    await rule_engine.evaluate_rules(test_data)
    assert len(published_alarms) == 0 