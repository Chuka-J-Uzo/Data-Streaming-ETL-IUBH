from confluent_kafka import Producer
import subprocess
import json

producer_config = {
    'bootstrap.servers': '127.0.0.1:9092',  # Kafka broker address and port number
    'acks': 'all',  # Wait for all replicas to acknowledge the message
    'queue.buffering.max.messages': 2000000,  # Maximum number of messages guaranteed to be delivered to Kafka every time
    'queue.buffering.max.kbytes': 3000000,  # Maximum total size of messages buffered in memory by the producer
    'partitioner': 'consistent',
    'message.send.max.retries': '5',
    'request.required.acks': '-1',
    'compression.type': 'lz4',
    'compression.level': '6'
}

# Create an instance of the Producer class with the provided configuration.
producer = Producer(producer_config)
print("Created Kafka producer instance:", producer)

while True:
    try:
        p = subprocess.Popen(['adb', 'shell', 'dumpsys', 'sensorservice'], stdout=subprocess.PIPE)
        output, err = p.communicate()
        if err:
            print(f"Error occurred: {err}")
            continue

        sensor_data = {}
        for line in output.splitlines():
            line = line.strip()
            if b'Accelerometer Sensor:' in line:
                for i in range(5):
                    line = output.splitlines()[output.splitlines().index(line) + i]
                    if b'x:' in line:
                        sensor_data['x'] = float(line.split(b' ')[-1])
                    elif b'y:' in line:
                        sensor_data['y'] = float(line.split(b' ')[-1])
                    elif b'z:' in line:
                        sensor_data['z'] = float(line.split(b' ')[-1])
            elif b'Gyroscope Sensor:' in line:
                for i in range(5):
                    line = output.splitlines()[output.splitlines().index(line) + i]
                    if b'x:' in line:
                        sensor_data['gyro_x'] = float(line.split(b' ')[-1])
                    elif b'y:' in line:
                        sensor_data['gyro_y'] = float(line.split(b' ')[-1])
                    elif b'z:' in line:
                        sensor_data['gyro_z'] = float(line.split(b' ')[-1])
            elif b'Orientation Sensor:' in line:
                for i in range(5):
                    line = output.splitlines()[output.splitlines().index(line) + i]
                    if b'azimuth:' in line:
                        sensor_data['azimuth'] = float(line.split(b' ')[-1])
                    elif b'pitch:' in line:
                        sensor_data['pitch'] = float(line.split(b' ')[-1])
                    elif b'roll:' in line:
                        sensor_data['roll'] = float(line.split(b' ')[-1])
        
        if sensor_data:
            encoded_data = json.dumps(sensor_data).encode('utf-8')
            print("Produced sensor data:", encoded_data)                                   
            producer.produce('Mobile-Device-Data', encoded_data)

            print("Message produced successfully") #


        producer.poll(0.5)
    except Exception as e:
        print(f"Error occurred: {e}")
