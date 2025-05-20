# 📁 File: data_simulator/simulator.py
import json
import time
import random
from kafka import KafkaProducer
from datetime import datetime

# Define static vehicle profiles
vehicle_profiles = {
    1001: {"city": "Chicago", "lat": 41.8781, "lon": -87.6298},
    1002: {"city": "New York", "lat": 40.7128, "lon": -74.0060},
    1003: {"city": "San Francisco", "lat": 37.7749, "lon": -122.4194},
    1004: {"city": "Houston", "lat": 29.7604, "lon": -95.3698},
    1005: {"city": "Seattle", "lat": 47.6062, "lon": -122.3321}
}

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Function to update GPS coordinates slightly
def update_position(lat, lon):
    lat += random.uniform(-0.0005, 0.0005)
    lon += random.uniform(-0.0005, 0.0005)
    return round(lat, 6), round(lon, 6)

# Function to simulate telemetry
def generate_telemetry(vehicle_id, lat, lon):
    speed = round(random.uniform(0, 120), 2)
    fuel_level = round(random.uniform(5, 100), 2)
    engine_temp = round(60 + (speed / 120) * 70 + random.uniform(-5, 5), 2)

    return {
        "vehicle_id": vehicle_id,
        "timestamp": datetime.utcnow().isoformat(),
        "lat": lat,
        "lon": lon,
        "speed": speed,
        "fuel_level": fuel_level,
        "engine_temp": engine_temp
    }

# Main loop
while True:
    for vid, profile in vehicle_profiles.items():
        profile["lat"], profile["lon"] = update_position(profile["lat"], profile["lon"])
        telemetry = generate_telemetry(vid, profile["lat"], profile["lon"])
        producer.send("vehicle-telemetry", telemetry)
        print(f"Sent: {telemetry}")
    time.sleep(1)
