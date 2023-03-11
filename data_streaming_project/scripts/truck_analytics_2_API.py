import csv
import time
import random
import pymysql
from datetime import datetime
from confluent_kafka import Producer
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import socket
import sqlalchemy
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, Float, DateTime
from sqlalchemy.sql import insert 

''' This first function will test for network, 
server and port connection before anything else'''
def is_reachable(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    try:
        s.connect((host, port))
        s.close()
        return True
    except:
        return False

host = "172.17.0.3"
port = 3306

if is_reachable(host, port):
    print("Hurray! Host is reachable!")
else:
    print("Host is not reachable!")


p = Producer({
    'bootstrap.servers': '127.0.0.1:9092',
    'acks': 'all',
    'queue.buffering.max.messages': 1300000,
    'queue.buffering.max.kbytes': 2000000,
    'compression.type': 'lz4',
    'compression.level': '6',
       
})



user = 'root'
password = 'root'
host =  '172.17.0.3'
port = 3306
database = 'KAFKA_DB'

# create a SQLAlchemy engine pointing to your database
engine = sqlalchemy.create_engine("mysql+pymysql://{}:{}@{}:{}/{}".format(user, password, host, port, database))

# create a connection to the database
conn = engine.connect()

# create metadata object bound to the engine, using the default schema
metadata = MetaData(engine)


ingest_table = Table(
    'TRUCK_PARAMETER_MAP', metadata,
    Column('current_time', DateTime),
    Column('road_elevation', Float),
    Column('engine_speed', Float),
    Column('Coolant_Temp', Float),
    Column('Oil_Pressure', Float),
    Column('Oil_Temp', Float),
    Column('Throttle_Position', Float),
    Column('Fuel_Pressure', Float),
    Column('Mass_Airflow_Rate', Float),
    Column('Intake_Air_Temp', Float),
    Column('Engine_Load', Float),
    Column('Battery_Voltage', Float),
    Column('Acceleration', Float),
    Column('Fuel_Level', Float),
    Column('Exhaust_Gas_Temp', Float),
    Column('Engine_Hours', Float),
    Column('Tyre_Pressure', Float)
)

conn = engine.connect()

metadata.create_all(engine)



current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3] 
road_elevation = round(random.uniform(0, 100), 2)
engine_speed = round(random.uniform(500, 3000), 2)
coolant_temp = round(random.uniform(80, 110), 2)
oil_pressure = round(random.uniform(10, 60), 2)
oil_temp = round(random.uniform(60, 85), 2)
throttle_position = round(random.uniform(0, 100), 2)
fuel_pressure = round(random.uniform(20, 70), 2)
mass_airflow_rate = round(random.uniform(50, 300), 2)
intake_air_temp = round(random.uniform(30, 70), 2)
engine_load = round(random.uniform(0, 100), 2)
battery_voltage = round(random.uniform(11, 15), 2)
acceleration = round(random.uniform(0, 100), 2)
fuel_level = round(random.uniform(0, 100), 2)
exhaust_gas_temp = round(random.uniform(300, 700), 2)
engine_hours = round(random.uniform(1, 24), 2)
tyre_pressure = round(random.uniform(25, 35), 2)





# map the database table to a Table object using SQLAlchemy's automap functionality
metadata = MetaData(engine)
Base = automap_base(metadata=metadata)
Base.prepare()

# get a reference to the table
table = Base.classes.TRUCK_PARAMETER_MAP.__table__


def delivery_report(err, msg):
    if err is not None:
        print('Message delivery failed: {}'.format(err))
    else:
        print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))

        # parse the payload from the Kafka message and convert it into a list of values
        payload = msg.value().decode("utf-8")
        payload_values = payload.split(',')

        # create a dictionary that maps column name strings to their corresponding values
        payload_dict = {
            'current_time': datetime.strptime(payload_values[0], '%Y-%m-%d %H:%M:%S.%f'),
            'road_elevation': float(payload_values[1]),
            'engine_speed': float(payload_values[2]),
            'Coolant_Temp': float(payload_values[3]),
            'Oil_Pressure': float(payload_values[4]),
            'Oil_Temp': float(payload_values[5]),
            'Throttle_Position': float(payload_values[6]),
            'Fuel_Pressure': float(payload_values[7]),
            'Mass_Airflow_Rate': float(payload_values[8]),
            'Intake_Air_Temp': float(payload_values[9]),
            'Engine_Load': float(payload_values[10]),
            'Battery_Voltage': float(payload_values[11]),
            'Acceleration': float(payload_values[12]),
            'Fuel_Level': float(payload_values[13]),
            'Exhaust_Gas_Temp': float(payload_values[14]),
            'Engine_Hours': float(payload_values[15]),
            'Tyre_Pressure': float(payload_values[16])
        }

        try:
            # create an INSERT statement with columns names and relevant values
            stmt = table.insert().values(**payload_dict)

            # execute the statement and commit the changes to the database
            conn.execute(stmt)
            conn.commit()
    
        except Exception as e:
            print(f"Error - {str(e)}")

conn = engine.connect()

while True:
    # generate a random payload as before
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3] 
    road_elevation = round(random.uniform(0, 100), 2)
    engine_speed = round(random.uniform(500, 3000), 2)
    coolant_temp = round(random.uniform(80, 110), 2)
    oil_pressure = round(random.uniform(10, 60), 2)
    oil_temp = round(random.uniform(60, 85), 2)
    throttle_position = round(random.uniform(0, 100), 2)
    fuel_pressure = round(random.uniform(20, 70), 2)
    mass_airflow_rate = round(random.uniform(50, 300), 2)
    intake_air_temp = round(random.uniform(30, 70), 2)
    engine_load = round(random.uniform(0, 100), 2)
    battery_voltage = round(random.uniform(11, 15), 2)
    acceleration = round(random.uniform(0, 100), 2)
    fuel_level = round(random.uniform(0, 100), 2)
    exhaust_gas_temp = round(random.uniform(300, 700), 2)
    engine_hours = round(random.uniform(1, 24), 2)
    tyre_pressure = round(random.uniform(25, 35), 2)
    message = f"{current_time},{road_elevation},{engine_speed},{coolant_temp},{oil_pressure},{oil_temp},{throttle_position},{fuel_pressure},{mass_airflow_rate},{intake_air_temp},{engine_load},{battery_voltage},{acceleration},{fuel_level},{exhaust_gas_temp},{engine_hours},{tyre_pressure}"

    # send message to Kafka and handle delivery reports to ensure messages are persisted correctly
    p.produce('sensor-data', message.encode('utf-8'), callback=delivery_report)
    p.poll(0)
    time.sleep(0.01)

conn.commit()
conn.close()






