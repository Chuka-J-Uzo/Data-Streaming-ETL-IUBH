from datetime import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import socket
import sqlalchemy
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, Float, DateTime
from sqlalchemy.sql import insert
from sqlalchemy.exc import IntegrityError
from confluent_kafka import Producer

# setup database connection
user = 'root'
password = 'root'
host = '172.17.0.3'
port = '3306'
database = 'KAFKA_DB'

engine = create_engine("mysql+pymysql://{}:{}@{}:{}/{}".format(user, password, host, port, database))
connection = engine.connect()

metadata = MetaData()

truck_data = Table('TRUCK_PARAMETER_MAP', metadata,
                   Column('id', Integer, primary_key=True),
                   Column('timestamp', DateTime),
                   Column('distance_covered', Float),
                   Column('engine_speed', Float),
                   Column('fuel_consumed', Float))


metadata.create_all(engine)

producer_config = {'bootstrap.servers': '127.0.0.1:9092',
                   'acks': 'all',
                   'queue.buffering.max.messages': 1300000,
                   'queue.buffering.max.kbytes': 2000000,
                   'compression.type': 'lz4',
                   'compression.level': '6',
                   'security.protocol': 'PLAINTEXT'}

producer = Producer(producer_config)


def produce_truck_data():
    try:
        distance_covered = 100
        fuel_tank_capacity = 50
        fuel_remaining = fuel_tank_capacity
        engine_speed = 80
        counter = 0
        
        # Get the latest timestamp in the database
        latest_timestamp_query = truck_data.select().order_by(truck_data.c.timestamp.desc()).limit(1)
        latest_timestamp = connection.execute(latest_timestamp_query).scalar()
        
        # If no records in the database yet, set the timestamp to the current time
        if latest_timestamp is None:
            latest_timestamp = datetime.now()
        else:
            latest_timestamp = pd.to_datetime(latest_timestamp)
        
        for i in range(100):
            distance_travelled = i + 1
            fuel_consumed = (distance_travelled / distance_covered) * fuel_tank_capacity
            fuel_remaining -= fuel_consumed
            if fuel_remaining <= 0:
                break
            timestamp = latest_timestamp + pd.Timedelta(seconds=counter)
            data = {"timestamp": str(timestamp),
                    "distance_covered": np.round(distance_travelled, 2),
                    "engine_speed": np.round(engine_speed, 2),
                    "fuel_consumed": np.round(fuel_consumed, 2)}
            producer.produce("Truck-Data", value=str(data).encode())
            
            # Insert generated data into mysql database
            stmt = insert(truck_data).values(
                timestamp=timestamp, 
                distance_covered=data['distance_covered'],
                engine_speed=data['engine_speed'], 
                fuel_consumed=data['fuel_consumed']
            )
            
            try:
                connection.execute(stmt)
            except IntegrityError:
                # If the insert fails due to a duplicate key error, update the existing record instead
                stmt = truck_data.update().values(
                    distance_covered=data['distance_covered'],
                    engine_speed=data['engine_speed'], 
                    fuel_consumed=data['fuel_consumed']
                ).where(truck_data.c.timestamp == timestamp)
                connection.execute(stmt)
            
            connection.commit()
            
            counter += 1
            print("Message sent successfully")

        producer.flush() # flushes all outstanding messages from the buffer.
   
    except Exception as e:
        print("Exception in sending message")
        print(str(e))

    finally:
        connection.close()

if __name__ == '__main__':
    produce_truck_data()
