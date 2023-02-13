import csv
import pymysql
from confluent_kafka import Producer


#p = Producer({'bootstrap.servers': '127.0.0.1:9092'})
producers = [Producer({'bootstrap.servers': '127.0.0.1:9092',
              'acks': 'all',
              'queue.buffering.max.messages': 1300000, # increase the maximum number of messages in the buffer
              'queue.buffering.max.kbytes': 2000000, # increase the maximum total message size in kilobytes that the producer will buffer})
              'security.protocol': 'PLAINTEXT', 
              }) for _ in range(4)]




conn = pymysql.connect(
    host='172.17.0.3',
    user='root',
    password='root',
    db='KAFKA_DB'
    )

cursor = conn.cursor()

def delivery_report(err, msg):
    """ Called once for each message produced to indicate delivery result.
        Triggered by poll() or flush(). """
    if err is not None:
        print('Message delivery failed: {}'.format(err))
    else:
        print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))
        # Convert the data to a string and decode it from utf-8
        data = msg.value().decode('utf-8')
        # Split the data into separate values
        values = data.split(',')
        # Insert the values into the database. 'INGESTED_TABLE_1' is the name of our MySQL table.
        cursor.execute("INSERT INTO INGESTED_TABLE_1 (time, seconds_elapsed, qz,  qy,  qx,  qw,  roll, pitch, yaw) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", values)
        conn.commit()


def produce_message(producer, data):
    producer.produce('data-inflow-1', data, callback=delivery_report)
    producer.poll(0)


# Open the CSV file and read the data
with open("data_streaming_project/datasets/Orientation.csv", "r") as file:
    reader = csv.reader(file)
    # Skip the header row
    next(reader)
    for i, row in enumerate(reader):
        # Convert the row to a string and encode it as utf-8
        data = ",".join(row).encode('utf-8')
        # Trigger any available delivery report callbacks from previous produce() calls
        
        # Asynchronously produce a message. The delivery report callback will
        # be triggered from the call to poll() above, or flush() below, when the
        # message has been successfully delivered or failed permanently.
        producer_index = i % len(producers) # pick a producer to use
        produce_message(producers[producer_index], data)

for producer in producers:
    producer.flush()
conn.close()