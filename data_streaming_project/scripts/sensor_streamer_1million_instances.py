import os
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import socket
import sqlalchemy
import ssl
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, Float, DateTime
from sqlalchemy.sql import insert
from sqlalchemy.exc import IntegrityError
from confluent_kafka import Producer
import subprocess




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
    print("\n Kafka about to start producing messages below.....🥳 \n") 
    mp3_file = "data_streaming_project/audio_message_alerts/kafka-started-alert.mp3"
    subprocess.call(["cvlc", "--play-and-exit", mp3_file])
    for i in range(2):
        os.system("paplay /usr/share/sounds/freedesktop/stereo/service-login.oga")
    
 
else:
    print("Host is not reachable! 😭")



# setup database connection
user = 'root'
password = 'root'
host = '172.17.0.3'
port = '3306'
database = 'KAFKA_DB'


# specify SSL parameters
ssl_args = {
    'ssl': {
        'cert': './../kafka-ssl/ca-cert',
        'key': './..',
        'ca': '/path/to/ca.pem',
        'check_hostname': False
    }
}



engine = create_engine("mysql+pymysql://{}:{}@{}:{}/{}".format(user, password, host, port, database))
connection = engine.connect()

metadata = MetaData() # creates a new instance of MetaData class from that is defined in the SQLAlchemy package.

'''
The 'MetaData()' function used above class acts as 
essentially an interface for storing information 
about tables, columns, constraints and other metadata 
constructs within the database without having to perform 
any physical operations on it.

'''


truck_data = Table('TRUCK_PARAMETER_MAP', metadata,
                   Column('id', Integer, primary_key=True),
                   Column('timestamp', DateTime),
                   Column('distance_covered', Float),
                   Column('engine_speed', Float),
                   Column('fuel_consumed', Float))


metadata.create_all(engine) # This line creates all the tables in the metadata object in the assigned database engine.

producer_config = {#'bootstrap.servers': '127.0.0.1:9092', # specifies the Kafka broker address and port number.
                   'bootstrap.servers':'127.0.0.1:9092',
                   #'security.protocol': 'SSL', # Security protocol to use
                   #'ssl.keystore.password': 000000 ,
                   #'ssl.ca.location': './../kafka-ssl/cert-file', # Path to CA certificate file
                   #'ssl.truststore.location': './../kafka-ssl/kafka.client.truststore.jks',
                   #'ssl.truststore.password': '000000',
                   #'ssl.keystore.location': './../kafka-ssl/kafka.server.keystore.jks', 
                   #'ssl.keystore.password': '000000',
                   #'ssl.key.password': '000000' ,
                   'acks': 'all', #  specifies different levels of acknowledgments that the leader broker must receive from a partition's replicas before considering a send request complete.
                   'queue.buffering.max.messages': 2000000, # Maximum number of messages guaranteed to be delivered to Kafka every time.
                   'queue.buffering.max.kbytes': 3000000, # Maximum total size of messages buffered in memory by the producer.
                   'partitioner': 'consistent',                   
                   'message.send.max.retries': '5',
                   'request.required.acks': '-1',
                   'compression.type': 'lz4', # The compression type for all data generated by the producer. Supported values are 'none', 'gzip', 'snappy', 'lz4', or 'zstd'.
                   'compression.level': '6' # Compression level parameter for algorithm selected by configuration property compression.type.
                   }


                   

# Create an instance of the Producer class with the provided configuration.
producer = Producer(producer_config)

# A function to generate simulated truck data and send it to a message broker.
def produce_truck_data():
    try:
        fuel_tank_capacity = 600
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

        
        # initialize a message counter variable for the simulated truck in motion
        counter = 1
        '''
        The "counter = 1" function above, initializes 
        counter to a value of 1. It is used to count 
        or index our "Message sent successfully" delivery message 
        elements used below in a program loop or 
        function, to keep track of the state of some 
        component in the larger system, or to simply 
        represent a numerical value assigned to a 
        variable for use later on in our program.
        '''
         
        # initialize a message counter variable as message delivery alerts
        message_counter = 0
        '''
        This message_counter variable is to make the 
        program beep for every 100 messages Kafka produces, 
        we can add a counter variable that increments for 
        every message produced. Once the counter variable 
        reaches 100, we then play a sound using the "os" library 
        in Python. Below we add a few modifications after 
        the line of code: "fuel_consumed": np.round(fuel_consumed, 2)} 
        ''' 
        
        
        
        
        for i in range(2400000):
            engine_speed = np.random.normal(80, 1)
            time_elapsed = np.random.exponential(scale=1/10000) * 3600  # time elapsed in seconds
            distance_travelled = (time_elapsed / 3600) * engine_speed
            distance_covered += distance_travelled 
            fuel_consumption_rate = np.interp(engine_speed, [80, 200], [0.01, 0.1])  # liters/km
            #fuel_consumed += distance_travelled * fuel_consumption_rate
            #fuel_remaining -= fuel_consumed
            fuel_consumed += time_elapsed / 3600 * engine_speed * fuel_consumption_rate
            fuel_remaining -= fuel_consumption_rate * distance_travelled

            if fuel_remaining <= 0:
                break
            timestamp = datetime.now()
            data = {"timestamp": str(timestamp),
                    "distance_covered": np.round(distance_covered, 2),
                    "engine_speed": np.round(engine_speed, 2),
                    "fuel_consumed": np.round(fuel_consumed, 2)}
            
            '''
            This second code block of the message_counter variable is where we now
            make the program to beep for every 100 messages Kafka produces, 
            we can add a counter variable that increments for 
            every message produced. Once the counter variable 
            reaches 100, we then play a sound using the "os" library 
            in Python. The beep function below ends at the comment and line:
             # reset message counter,
               message_counter = 0  

            ''' 

            # increment message counter
            message_counter += 1
            
            # check if message counter reaches 100
            if message_counter == 100:
                # play a beep sound
                os.system("paplay /usr/share/sounds/freedesktop/stereo/complete.oga")
                
                # reset message counter
                message_counter = 0


            # Send our messages to Kafka topic
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
            
            print("Message [{}] sent successfully --------------------> ".format(counter))
            
            counter += 1 # This code increments the value of our counter by 1.

        producer.flush() # flushes all outstanding messages from the kafka buffer.
   
    except Exception as e:
        print("Exception in sending message")
        print(str(e))

    finally:
        producer.flush()
    try:
        producer.close()
    except AttributeError:
        print("Error: Producer object has no close method")
                



if __name__ == '__main__':
    produce_truck_data()