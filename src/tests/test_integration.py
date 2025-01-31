import pytest
import asyncio
import json
from src.services.nats_service import NatsService
from src.services.rule_engine import RuleEngine
from src.config.rules_config import RuleConfig

@pytest.fixture
async def setup_services():
    # Initialize services
    nats_service = NatsService("nats://localhost:4222")
    rule_config = RuleConfig()
    rule_engine = RuleEngine(rule_config, nats_service)
    
    # Connect to NATS
    await nats_service.connect()
    
    yield nats_service, rule_config, rule_engine
    
    # Cleanup
    await nats_service.nc.close()

@pytest.mark.asyncio
async def test_end_to_end_flow(setup_services):
    """Test complete flow from message receipt to alarm generation"""
    nats_service, rule_config, rule_engine = setup_services
    
    # Store received alarms
    received_alarms = []
    
    async def alarm_handler(msg):
        received_alarms.append(json.loads(msg.data.decode()))
    
    # Subscribe to alarms
    await nats_service.subscribe("sensor.alarm", alarm_handler)
    
    # Publish test event
    test_event = {
        "sensor_id": "Temperature-101",
        "value": 140.0
    }
    await nats_service.publish("sensor.event", test_event)
    
    # Wait for processing
    await asyncio.sleep(1)
    
    # Verify alarm was generated
    assert len(received_alarms) == 1
    assert received_alarms[0]["sensor_id"] == "Temperature-101"
    assert received_alarms[0]["action"] == "lower fuel"

@pytest.mark.asyncio
async def test_multiple_events(setup_services):
    """Test handling of multiple events"""
    nats_service, rule_config, rule_engine = setup_services
    
    received_alarms = []
    async def alarm_handler(msg):
        received_alarms.append(json.loads(msg.data.decode()))
    
    await nats_service.subscribe("sensor.alarm", alarm_handler)
    
    # Publish multiple events
    test_events = [
        {"sensor_id": "Temperature-101", "value": 140.0},
        {"sensor_id": "Temperature-102", "value": 70.0},
        {"sensor_id": "Pressure-A201", "value": 90.0}
    ]
    
    for event in test_events:
        await nats_service.publish("sensor.event", event)
    
    # Wait for processing
    await asyncio.sleep(2)
    
    # Verify correct number of alarms
    assert len(received_alarms) == 3 