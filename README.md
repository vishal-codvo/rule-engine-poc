# Sensor Rule Engine

## Overview
This is a scalable rule engine for processing sensor data streams using NATS messaging system and PostgreSQL for rule storage.

## Architecture
- NATS: Message broker for handling sensor events
- PostgreSQL: Stores sensor rules and configurations
- Python Service: Processes messages and applies business rules

## Execution Flow
1. System startup:
   - PostgreSQL initializes with predefined rules
   - NATS server starts and listens for messages
   - Python service connects to both NATS and PostgreSQL

2. Message Processing:
   - Sensors publish data to `sensor.event` subject
   - Python service receives messages asynchronously
   - Rule engine evaluates each message against stored rules
   - If rule conditions are met, alerts are published to `sensor.alarm`

3. Rule Processing:
   - Rules are loaded from PostgreSQL at startup
   - Each sensor message is evaluated against its specific rules
   - Multiple rules can be defined for each sensor
   - Rules can check for both minimum and maximum thresholds

## Running the System
1. Build and start services:
   ```bash
   docker-compose up --build
   ```

2. Monitor logs:
   ```bash
   docker-compose logs -f
   ```

3. Stop services:
   ```bash
   docker-compose down
   ```

## Testing
To test the system, publish messages to the NATS subject `sensor.event`:

Example message: