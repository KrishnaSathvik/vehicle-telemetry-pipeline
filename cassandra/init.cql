CREATE KEYSPACE IF NOT EXISTS telemetry WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '1'};

USE telemetry;

CREATE TABLE IF NOT EXISTS vehicle_data (
    vehicle_id int,
    timestamp text,
    lat double,
    lon double,
    speed double,
    fuel_level double,
    engine_temp double,
    PRIMARY KEY (vehicle_id, timestamp)
);
