
schema = StructType([
        StructField("id", IntegerType(), True),
        StructField("timestamp", LongType(), True),
        StructField("distance_covered", DoubleType(), True),
        StructField("engine_speed", DoubleType(), True),
        StructField("fuel_consumed", DoubleType(), True),
    ])

schema = StructType([
...     StructField("time", LongType(), True),
...     StructField("seconds", IntegerType(), True),
...     StructField("qz", DoubleType(), True),
...     StructField("qy", DoubleType(), True),
...     StructField("qx", DoubleType(), True),
...     StructField("qw", DoubleType(), True),
...     StructField("roll", DoubleType(), True),
...     StructField("pitch", DoubleType(), True),
...     StructField("yaw", DoubleType(), True)
... ])

df = spark \
    .readStream \
    .format('kafka') \
    .option('kafka.bootstrap.servers', 'localhost:9092') \
    .option('subscribe', 'Truck-Data') \
    .option('startingOffsets', 'earliest') \
    .option('failOnDataLoss', 'false') \
    .option('includeTimestamp', 'true') \
    .option('schema', schema) \
    .load()

os.environ['SPARK_HOME'] = '/opt/spark-3.3.2-bin-hadoop3'
sys.path.append('/opt/spark-3.3.2-bin-hadoop3/python')
sys.path.append('/opt/spark-3.3.2-bin-hadoop3/python/lib')

i have a java home already set for my computer but i want to set a different version jdk11 as a home so that python can find it when i run pyspark. However i don't want it to replace my actual java home.  what command should i use if my downloaded java path is this: ./home/blackjack/Data-Streaming-ETL-IUBH-main/Data-Streaming-ETL-IUBH/jav_a_folder/jdk-11.0.18+10