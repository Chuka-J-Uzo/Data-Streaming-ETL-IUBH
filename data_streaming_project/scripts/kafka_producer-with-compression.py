import csv
import mysql.connector
from confluent_kafka import Producer


#p = Producer({'bootstrap.servers': '127.0.0.1:9092'})
p = Producer({'bootstrap.servers': '127.0.0.1:9092',
              'acks': 'all',
              'queue.buffering.max.messages': 1300000, # increase the maximum number of messages in the buffer
              'queue.buffering.max.kbytes': 2000000, # increase the maximum total message size in kilobytes that the producer will buffer})
              'compression.type': 'snappy'
              })




conn = mysql.connector.connect(user='root', password='root',
                              host='172.17.0.2', database='KAFKA_DB')
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

# Open the CSV file and read the data
with open("data_streaming_project/datasets/Orientation.csv", "r") as file:
    reader = csv.reader(file)
    # Skip the header row
    next(reader)
    for row in reader:
        # Convert the row to a string and encode it as utf-8
        data = ",".join(row).encode('utf-8')
        # Trigger any available delivery report callbacks from previous produce() calls
        
        # Asynchronously produce a message. The delivery report callback will
        # be triggered from the call to poll() above, or flush() below, when the
        # message has been successfully delivered or failed permanently.
        p.produce('data-inflow-1', data, callback=delivery_report)
        p.poll(0)

# Wait for any outstanding messages to be delivered and delivery report
# callbacks to be triggered.
p.flush()
conn.close()