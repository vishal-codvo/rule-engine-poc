CREATE TABLE sensor_rules (
    id SERIAL PRIMARY KEY,
    sensor_id VARCHAR(50) NOT NULL UNIQUE,
    rule_type VARCHAR(20) NOT NULL,
    min_value FLOAT,
    max_value FLOAT,
    action TEXT NOT NULL,
    trigger_message TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert sample rules
INSERT INTO sensor_rules (sensor_id, rule_type, min_value, max_value, action, trigger_message) VALUES
('Temperature-101', 'temperature', NULL, 120, 'lower fuel', 'temperature beyond threshold'),
('Temperature-102', 'temperature', 80, 120, 'lower fuel', 'temperature beyond threshold'),
('Pressure-A201', 'pressure', NULL, 80, 'open valve xyz', 'Pressure beyond threshold'),
('Pressure-A202', 'pressure', 60, NULL, 'close valve xyz', 'Pressure below threshold'); 