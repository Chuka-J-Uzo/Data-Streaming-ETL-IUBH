import findspark
findspark.init()
import pyspark 
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
import os
import sys

os.environ['SPARK_HOME'] = '/opt/spark'
sys.path.append('/opt/spark/python')
sys.path.append('/opt/spark/python/lib/py4j-0.10.9-src.zip')


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


# Now, let's perform transformations on the inbound data as needed
# 1. Calculate the average pitch for each second
#df_transformed = df.groupBy(df['seconds']).agg(avg(df['pitch']).alias("avg_pitch"))

# 2. Filter data with only specific columns and rename the columns
df_transformed = df.select("time", "qz", "qy", "qx", "qw") \
                   .withColumnRenamed("time", "timestamp") \
                   .withColumnRenamed("qz", "z_axis") \
                   .withColumnRenamed("qy", "y_axis") \
                   .withColumnRenamed("qx", "x_axis") \
                   .withColumnRenamed("qw", "w_axis")

# 3. Group the data by "timestamp" and compute the average of each axis
df_grouped = df_transformed.groupBy(df_transformed.timestamp) \
                           .agg(avg(df_transformed.z_axis),
                                avg(df_transformed.y_axis),
                                avg(df_transformed.x_axis),
                                avg(df_transformed.w_axis))



# Define the schema for the transformed data
schema_transformed = StructType([
    StructField("timestamp", TimestampType(), True),
    StructField("seconds", IntegerType(), True),
    StructField("avg_qz", DoubleType(), True),
    StructField("avg_qy", DoubleType(), True),
    StructField("avg_qx", DoubleType(), True),
    StructField("avg_qw", DoubleType(), True),
    StructField("avg_roll", DoubleType(), True),
    StructField("avg_pitch", DoubleType(), True),
    StructField("avg_yaw", DoubleType(), True)
])


# Perform transformations on the data
df_transformed = df.withColumn("timestamp", from_unixtime(col("time")/1000, "yyyy-MM-dd HH:mm:ss")) \
                   .groupBy(window("timestamp", "1 minute")) \
                   .agg(avg("qz").alias("avg_qz"),
                        avg("qy").alias("avg_qy"),
                        avg("qx").alias("avg_qx"),
                        avg("qw").alias("avg_qw"),
                        avg("roll").alias("avg_roll"),
                        avg("pitch").alias("avg_pitch"),
                        avg("yaw").alias("avg_yaw"))


# Now, we write our transformed data to a MySQL table
df_transformed.writeStream \
    .format("jdbc") \
    .option("url", "jdbc:mysql://MySQL_Container:3306/KAFKA_DB") \
    .option("dbtable", "SPARK_TABLE_TRANSFORMED") \
    .option("user", "root") \
    .option("password", "root") \
    .option("checkpointLocation", "/tmp/checkpoints") \
    .option("driver", "com.mysql.cj.jdbc.Driver") \
    .start()

# Submit my file to spark-submit

#spark.sparkContext.addPyFile('./sparkstreamer.py')
#spark.sparkContext.submit(MainClass='sparkstreamer.py')
