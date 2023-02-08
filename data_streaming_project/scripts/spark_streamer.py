import sys
import pyspark                
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
#import findspark
#findspark.init()



# Create a Spark session
#spark = SparkSession.builder.appName('Realtime_Streamprocessing_app').getOrCreate()
spark = SparkSession \
            .builder \
            .config("spark.driver.host", "localhost") \
            .appName('Realtime_Streamprocessing_app') \
            .getOrCreate()



# Define the schema for the data
schema = StructType([
    StructField("time", LongType(), True),
    StructField("seconds", IntegerType(), True),
    StructField("qz", DoubleType(), True),
    StructField("qy", DoubleType(), True),
    StructField("qx", DoubleType(), True),
    StructField("qw", DoubleType(), True),
    StructField("roll", DoubleType(), True),
    StructField("pitch", DoubleType(), True),
    StructField("yaw", DoubleType(), True)
])

# Consume data from the Kafka topic
df = spark \
    .readStream \
    .format('kafka') \
    .option('kafka.bootstrap.servers', 'localhost:9092') \
    .option('subscribe', 'data-inflow-1') \
    .option('startingOffsets', 'earliest') \
    .option('failOnDataLoss', 'false') \
    .option('includeTimestamp', 'true') \
    .option('schema', schema) \
    .load()

# Write the data to a Postgres table
df.writeStream \
    .format('jdbc') \
    .option('url', 'jdbc:postgresql://localhost:5432/test_db1') \
    .option('dbtable', 'table_1') \
    .option('user', 'root') \
    .option('password', 'root') \
    .option('checkpointLocation', '/tmp/checkpoints') \
    .start()

# Perform any transformations or aggregations on the data as needed
df_transformed = df.select(...)

# Write the transformed data to another Postgres table
df_transformed.writeStream \
    .format('jdbc') \
    .option('url', 'jdbc:postgresql://localhost:5432/test_db1') \
    .option('dbtable', 'table_1_transformed') \
    .option('user', 'root') \
    .option('password', 'root') \
    .option('checkpointLocation', '/tmp/checkpoints') \
    .start()


# Submit my file to spark-submit

#spark.sparkContext.addPyFile('./sparkstreamer.py')
#spark.sparkContext.submit(MainClass='sparkstreamer.py')
