from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import socket
import sqlalchemy
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, Float, DateTime
from sqlalchemy.sql import insert
from sqlalchemy.exc import IntegrityError
from confluent_kafka import Producer

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
    print("\n Hurray! Host is now reachable on " , host , "and port number:" , port)
    print("\n Kafka is now producing messages.....🥳 \n")     
else:
    print("Host is not reachable! 😭")


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
        fuel_tank_capacity = 250
        fuel_remaining = fuel_tank_capacity
        distance_travelled = 0
        counter = 0
        
        # get the last recorded distance and fuel consumption from the database
        last_record = connection.execute(truck_data.select().order_by(truck_data.c.id.desc()).limit(1)).fetchone()
        if last_record is None:
            # if no records exist in the database, start from the beginning
            distance_covered = 0
            fuel_consumed = 0
        else:
            # if records exist, continue from the last recorded values
            distance_covered = last_record.distance_covered
            fuel_consumed = last_record.fuel_consumed

        counter = 1

        '''
        The "counter = 1" line of code above, initializes 
        counter to a value of 1. It is used to count 
        or index our "Message sent successfully" delivery message 
        elements used below in a program loop or 
        function, to keep track of the state of some 
        component in the larger system, or to simply 
        represent a numerical value assigned to a 
        variable for use later on in our program.
        '''

        while fuel_remaining > 0:
            engine_speed = np.random.normal(80, 0.1)
            time_elapsed = np.random.exponential(scale=1/3000) * 3600  # time elapsed in seconds
            distance_travelled = (time_elapsed / 3600) * engine_speed
            distance_covered += distance_travelled
            fuel_consumption_rate = np.interp(engine_speed, [80, 95], [0.01, 0.1])  # liters/km
            fuel_consumed += distance_travelled * fuel_consumption_rate
            fuel_remaining -= fuel_consumed
            if fuel_remaining <= 0:
                break
            timestamp = datetime.now()
            data = {"timestamp": str(timestamp),
                    "distance_covered": np.round(distance_covered, 2),
                    "engine_speed": np.round(engine_speed, 2),
                    "fuel_consumed": np.round(fuel_consumed, 2)}
            producer.produce("Truck-Data", value=str(data).encode())
            producer.flush() # We add a flush here to ensure messages are delivered before moving to next iteration
            
            
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
            
            
            print("Message sent successfully [{}]".format(counter))

            counter += 1 # This code increments the value of our counter by 1.

        producer.flush() # flushes all outstanding messages from the buffer.
   
    except Exception as e:
        print("Exception in sending message")
        print(str(e))

    finally:
        connection.close()


if __name__ == '__main__':
    produce_truck_data()
