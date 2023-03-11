import random
import time
import datetime
from confluent_kafka import Producer


def generate_sensor_data():
    # Generate pseudo-real-time data for all parameters
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    road_elevation = round(random.uniform(0, 100), 2) # meters
    engine_speed = round(random.uniform(500, 3000), 2) # rpm
    coolant_temp = round(random.uniform(50, 100), 2) # degrees Celsius
    oil_pressure = round(random.uniform(10, 100), 2) # kilopascals
    oil_temp = round(random.uniform(60, 100), 2) # degrees Celsius
    throttle_position = round(random.uniform(0, 100), 2) # percentage
    fuel_pressure = round(random.uniform(100, 500), 2) # kilopascals
    mass_airflow_rate = round(random.uniform(1, 5), 2) # grams per second
    intake_air_temp = round(random.uniform(30, 50), 2) # degrees Celsius
    engine_load = round(random.uniform(0, 100), 2) # percentage
    battery_voltage = round(random.uniform(12, 14), 2) # volts
    acceleration = round(random.uniform(-1, 1), 2) # meters per second squared
    fuel_level = round(random.uniform(0, 100), 2) # percentage
    exhaust_gas_temp = round(random.uniform(150, 300), 2) # degrees Celsius
    engine_hours = round(random.uniform(0, 24), 2) # hours
    tyre_pressure = [round(random.uniform(200, 300), 2) for i in range(6)] # kilopascals
    
    # Return dictionary of sensor data
    return {
        "timestamp": timestamp,
        "road_elevation": road_elevation,
        "engine_speed": engine_speed,
        "coolant_temp": coolant_temp,
        "oil_pressure": oil_pressure,
        "oil_temp": oil_temp,
        "throttle_position": throttle_position,
        "fuel_pressure": fuel_pressure,
        "mass_airflow_rate": mass_airflow_rate,
        "intake_air_temp": intake_air_temp,
        "engine_load": engine_load,
        "battery_voltage": battery_voltage,
        "acceleration": acceleration,
        "fuel_level": fuel_level,
        "exhaust_gas_temp": exhaust_gas_temp,
        "engine_hours": engine_hours,
        "tyre_pressure": tyre_pressure
    }

p = Producer({
    'bootstrap.servers': '127.0.0.1:9092',
    'acks': 'all',
    'queue.buffering.max.messages': 1300000,
    'queue.buffering.max.kbytes': 2000000,
    'compression.type': 'lz4',
    'compression.level': '6',
    'security.protocol': 'PLAINTEXT'
})

while True:
    # Generate sensor data
    sensor_data = generate_sensor_data()

    # Convert dictionary to comma-separated string for Kafka ingestion
    data_str = ""
    for k,v in sensor_data.items():
        if isinstance(v, list):
            data_str += ",".join(map(str, v)) + ","
        else:
            data_str += str(v) + ","
    data_str = data_str[:-1].encode('utf-8')

    # Publish data to Kafka topic
    p.produce('sensor-data', data_str)
    p.poll(0)

    # Wait some time before generating next set of data
    time.sleep(0.01) # Sample rate of 100 Hz
