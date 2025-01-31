import os
import asyncio
import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from services.nats_service import NatsService
from services.rule_engine import RuleEngine
from config.rules_config import RuleConfig

async def message_handler(msg):
    try:
        data = json.loads(msg.data.decode())
        await rule_engine.evaluate_rules(data)
    except Exception as e:
        print(f"Error processing message: {e}")

async def main():
    # Initialize database connection
    db_url = os.getenv('POSTGRES_URL')
    engine = create_engine(db_url)
    Session = sessionmaker(bind=engine)
    db_session = Session()

    # Initialize services
    nats_service = NatsService(os.getenv('NATS_URL'))
    rule_config = RuleConfig()
    
    # Load rules from database
    await rule_config.load_rules_from_db(db_session)
    
    # Initialize rule engine
    global rule_engine
    rule_engine = RuleEngine(rule_config, nats_service)
    
    # Connect to NATS
    await nats_service.connect()
    
    # Subscribe to sensor events
    await nats_service.subscribe("sensor.event", message_handler)
    
    try:
        # Keep the application running
        while True:
            await asyncio.sleep(1)
    finally:
        # Clean up
        db_session.close()

if __name__ == "__main__":
    asyncio.run(main()) 