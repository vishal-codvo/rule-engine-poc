# Sensor Rule Engine - Architecture Documentation

## 1. System Overview

### 1.1 Purpose
The Sensor Rule Engine is a scalable, real-time system designed to process streaming sensor data and trigger alerts based on predefined rules. It implements a microservices architecture using Docker containers.

### 1.2 Key Features
- Real-time sensor data processing
- Configurable rule-based alerting
- Scalable microservices architecture
- Persistent rule storage
- Asynchronous message processing
- Docker containerization

## 2. System Architecture

### 2.1 High-Level Architecture
The system consists of three main components:
1. NATS Message Broker
2. PostgreSQL Database
3. Python Rule Engine Service

### 2.2 Component Details

#### 2.2.1 NATS Message Broker
- Purpose: Handles real-time message streaming
- Features:
  - Publish-Subscribe messaging pattern
  - High-performance message delivery
  - Built-in load balancing
- Message Subjects:
  - sensor.event: Incoming sensor data
  - sensor.alarm: Outgoing alarm notifications

#### 2.2.2 PostgreSQL Database
- Purpose: Stores rule configurations
- Schema:
  ```sql
  sensor_rules (
      id SERIAL PRIMARY KEY,
      sensor_id VARCHAR(50),
      rule_type VARCHAR(20),
      min_value FLOAT,
      max_value FLOAT,
      action TEXT,
      trigger_message TEXT
  )
  ```
- Features:
  - Persistent rule storage
  - ACID compliance
  - Efficient query performance

#### 2.2.3 Python Rule Engine Service
- Purpose: Processes messages and applies business rules
- Components:
  1. NATS Service (nats_service.py)
     - Handles message subscription
     - Manages message publishing
  2. Rule Config (rules_config.py)
     - Loads rules from database
     - Maintains rule cache
  3. Rule Engine (rule_engine.py)
     - Evaluates sensor data
     - Applies business rules
     - Triggers actions

### 2.3 Data Flow

1. Input Flow:
   ```
   Sensor → NATS (sensor.event) → Rule Engine
   ```

2. Processing Flow:
   ```
   Rule Engine → Rule Evaluation → Action Trigger
   ```

3. Output Flow:
   ```
   Rule Engine → NATS (sensor.alarm) → Alert Subscribers
   ```

## 3. Implementation Details

### 3.1 Docker Configuration
- Services:
  1. NATS Container
     - Port: 4222 (client), 8222 (monitoring)
  2. PostgreSQL Container
     - Port: 5433
     - Persistent volume for data
  3. Rule Engine Container
     - Python 3.9 based
     - Dependencies managed via requirements.txt

### 3.2 Rule Engine Implementation

#### 3.2.1 Rule Definition
```python
class SensorRule:
    sensor_id: str
    rule_type: str
    min_value: Optional[float]
    max_value: Optional[float]
    action: str
    trigger_message: str
```

#### 3.2.2 Message Format
1. Input Message (sensor.event):
```json
{
    "sensor_id": "Temperature-101",
    "value": 140
}
```

2. Output Message (sensor.alarm):
```json
{
    "sensor_id": "Temperature-101",
    "trigger": "temperature beyond threshold",
    "action": "lower fuel"
}
```

### 3.3 Scalability Features
1. Horizontal Scaling
   - Multiple rule engine instances possible
   - NATS handles load balancing
   - Stateless service design

2. Performance Optimization
   - Asynchronous message processing
   - Rule caching
   - Efficient database queries

## 4. Deployment and Operation

### 4.1 Prerequisites
- Docker and Docker Compose
- Network access for ports:
  - 4222 (NATS)
  - 5433 (PostgreSQL)

### 4.2 Deployment Steps
1. Environment Setup
2. Container Build
3. Service Startup
4. Rule Configuration
5. System Verification

### 4.3 Monitoring and Maintenance
- Log monitoring
- Performance metrics
- Database maintenance
- Rule updates

## 5. Security Considerations

### 5.1 Network Security
- Isolated container network
- Port exposure control
- Service-to-service communication

### 5.2 Data Security
- Database authentication
- Message validation
- Error handling

## 6. Future Enhancements

### 6.1 Potential Improvements
1. Authentication and Authorization
2. Message persistence
3. Rule versioning
4. Web interface for rule management
5. Metrics and monitoring dashboard
6. High availability setup

### 6.2 Scaling Considerations
1. Database clustering
2. NATS clustering
3. Load balancing
4. Cache implementation
5. Message queue optimization 