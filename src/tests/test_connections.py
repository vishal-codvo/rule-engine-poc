import pytest
import asyncio
from sqlalchemy import create_engine, text
from nats.aio.client import Client as NATS
from src.config.rules_config import RuleConfig
from src.services.nats_service import NatsService

@pytest.fixture
async def nats_client():
    nats = NATS()
    await nats.connect("nats://localhost:4222")
    yield nats
    await nats.close()

@pytest.fixture
def db_session():
    engine = create_engine('postgresql+psycopg2://ruleengine:ruleengine123@localhost:5433/sensor_rules')
    connection = engine.connect()
    yield connection
    connection.close()

@pytest.mark.asyncio
async def test_nats_connection(nats_client):
    """Test NATS connection"""
    assert nats_client.is_connected

@pytest.mark.asyncio
async def test_nats_pub_sub(nats_client):
    """Test NATS publish-subscribe"""
    received_messages = []
    
    async def message_handler(msg):
        received_messages.append(msg.data.decode())
    
    await nats_client.subscribe("test.subject", cb=message_handler)
    await nats_client.publish("test.subject", b"test message")
    
    # Wait for message processing
    await asyncio.sleep(1)
    assert len(received_messages) == 1
    assert received_messages[0] == "test message"

def test_db_connection(db_session):
    """Test database connection"""
    result = db_session.execute(text("SELECT 1")).scalar()
    assert result == 1

def test_db_rules_exist(db_session):
    """Test if rules exist in database"""
    result = db_session.execute(text("SELECT COUNT(*) FROM sensor_rules")).scalar()
    assert result > 0 