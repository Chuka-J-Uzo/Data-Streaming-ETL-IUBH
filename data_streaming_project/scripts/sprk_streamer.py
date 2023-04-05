import findspark
import pyspark
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
from pyspark import SparkConf, SparkContext
import os
import sys
import py4j
import json

findspark.init()
os.environ['JAVA_HOME'] = '/usr/local/java/jdk-11.0.18+10'
os.environ['SPARK_HOME'] = '/usr/local/spark'
sys.path.append('/usr/local/spark/python')
sys.path.append('/usr/local/spark/python/lib/pyspark.zip')
sys.path.append('/usr/local/spark/python/lib/py4j-0.10.9.5-src.zip')
sys.path.append('/usr/local/spark/bin')
sys.path.append('/usr/local/spark/yarn/spark-3.3.2-yarn-shuffle.jar')
sys.path.append('/usr/local/spark/jars')

# Create a Spark session
spark = SparkSession.builder \
    .config("spark.driver.host", "localhost") \
    .config("spark.driver.logLevel", "DEBUG") \
    .appName('Realtime_Streamprocessing_app') \
    .getOrCreate()

# Define the schema for the data
schema = StructType([
    StructField("id", IntegerType(), True),
    StructField("timestamp", LongType(), True),
    StructField("distance_covered", DoubleType(), True),
    StructField("engine_speed", DoubleType(), True),
    StructField("fuel_consumed", DoubleType(), True),
])

# Consume data from the Kafka topic
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

# Define the schema for the data
schema = StructType([
    StructField('id', IntegerType(), True),
    StructField('timestamp', StringType(), True),
    StructField('distance_covered', DoubleType(), True),
    StructField('engine_speed', DoubleType(), True),
    StructField('fuel_consumed', DoubleType(), True),
])

# Convert the value column from binary to string, and parse the fields
parsed_df = df.selectExpr('CAST(value AS STRING)').select(from_json('value', schema).alias('data'), 'timestamp')

# Flatten the struct column and rename the fields
transformed_df = parsed_df.selectExpr(
    'data.id AS id',
    'timestamp',
    'data.distance_covered AS distance_covered',
    'data.engine_speed AS engine_speed',
    'data.fuel_consumed AS fuel_consumed'
)

# Now, we write our transformed data to a MySQL table
transformed_df.writeStream \
    .format("jdbc") \
    .option("url", "jdbc:mysql://MySQL_Container:3306/KAFKA_DB") \
    .option("dbtable", "SPARK_TABLE_TRANSFORMED") \
    .option("user", "root") \
    .option("password", "root") \
    .option("checkpointLocation", "/tmp/checkpoints") \
    .option("driver", "com.mysql.cj.jdbc.Driver") \
    .start()

# Submit my file to spark-submit

# spark.sparkContext.addPyFile('./spark_streamer.py')
# spark.sparkContext.submit(MainClass='spark_streamer.py')
