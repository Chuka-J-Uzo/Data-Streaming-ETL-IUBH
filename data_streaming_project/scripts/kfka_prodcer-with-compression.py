import csv
#import mysql.connector
import pymysql
from confluent_kafka import Producer


p = Producer({'bootstrap.servers': '127.0.0.1:9092',
              'acks': 'all',
              'queue.buffering.max.messages': 1300000,
              'queue.buffering.max.kbytes': 2000000,
              'compression.type': 'lz4',
              'compression.level': '6',
              'security.protocol': 'PLAINTEXT',
              'ssl.ca.location': 'data_streaming_project/ssl_certificates/ca.pem',
              'ssl.certificate.location': 'data_streaming_project/ssl_certificates/cert.pem',
              'ssl.key.location': 'data_streaming_project/ssl_certificates/key.pm'
              })

#conn = mysql.connector.connect(user='root', password='root', host='172.17.0.3', database='KAFKA_DB')
conn = pymysql.connect(
    host='172.17.0.3',
    user='root',
    password='root',
    db='KAFKA_DB'
    )

cursor = conn.cursor()

# Set innodb_buffer_pool_size to 128MB
cursor.execute("SET GLOBAL innodb_buffer_pool_size=134217728")

# Set innodb_flush_log_at_trx_commit to 0
cursor.execute("SET GLOBAL innodb_flush_log_at_trx_commit=0")

def delivery_report(err, msg):
    if err is not None:
        print('Message delivery failed: {}'.format(err))
    else:
        print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))
        data = msg.value().decode('utf-8')
        values = data.split(',')
        cursor.execute("INSERT INTO INGESTED_TABLE_1 (time, seconds_elapsed, qz,  qy,  qx,  qw,  roll, pitch, yaw) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", values)
        conn.commit()

with open("data_streaming_project/datasets/Orientation.csv", "r") as file:
    reader = csv.reader(file)
    next(reader)
    data_list = []
    for i, row in enumerate(reader):
        data = ",".join(row).encode('utf-8')
        data_list.append(data)
        if (i + 1) % 1000000 == 0:
            for data in data_list:
                p.produce('data-inflow-1', data, callback=delivery_report)
                p.poll(0)
            data_list = []

if data_list:
    for data in data_list:
        p.produce('data-inflow-1', data, callback=delivery_report)
        p.poll(0)

p.flush()
conn.commit()
conn.close()