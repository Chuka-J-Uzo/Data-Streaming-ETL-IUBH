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
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, Float, DateTime



p = Producer({
    'bootstrap.servers': '127.0.0.1:9092',
    'acks': 'all',
    'queue.buffering.max.messages': 1300000,
    'queue.buffering.max.kbytes': 2000000,
    'compression.type': 'lz4',
    'compression.level': '6',
       
})

# Test for network availablility first!

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


# Set up our connection to the database and create a new table.

''' Here we will set up our connection
to our mysql database that currently is being served 
at 172.17.0.3:3306 by a MySQL container that we have already 
started before running this python script.'''

#user = 'root'
#password = 'root'
#host =  '172.17.0.4'
#port = 3306
#database = 'KAFKA_DB'

metadata = MetaData()

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





def delivery_report(err, msg):
    if err is not None:
        print('Message delivery failed: {}'.format(err))
    else:
        print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))
        try:
            # database connection settings
            user = 'root'
            password = 'root'
            host =  '172.17.0.3'
            port = 3306
            database = 'KAFKA_DB'

            # set up the SQLalchemy engine object
            engine = create_engine(f'mysql+pymysql://{user}:{password}@{host}:{port}/{database}')


            conn = engine.connect()
            data = msg.value().decode('utf-8')
            # cast each item from string to appropriate type before insertion
            values = [float(x) if x != '' else 0 for x in data.split(',')[1:]]
            metadata.create_all(engine)
            statement = ingest_table.insert().values(
                road_elevation=values[0], Engine_Speed=values[1], Coolant_Temp=values[2], 
                Oil_Pressure=values[3], Oil_Temp=values[4], Throttle_Position=values[5], 
                Fuel_Pressure=values[6], Mass_Airflow_Rate=values[7], Intake_Air_Temp=values[8], 
                Engine_Load=values[9], Battery_Voltage=values[10], Acceleration=values[11],
                Fuel_Level=values[12], Exhaust_Gas_Temp=values[13], Engine_Hours=values[14], 
                Tyre_Pressure=values[15])
            conn.execute(statement)
            conn.close()
        except Exception as e:
            print(f"Error - {str(e)}")
            conn.close()
        
      

while True:
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

    p.produce('sensor-data', message.encode('utf-8'), callback=delivery_report)
    p.poll(0)
    time.sleep(0.01)

conn.commit()
conn.close()






