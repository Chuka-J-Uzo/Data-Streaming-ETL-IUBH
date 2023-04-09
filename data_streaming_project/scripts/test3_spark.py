import pyspark
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, window
from pyspark.sql.types import StructType, StructField, StringType, DoubleType
from pyspark.sql.functions import col, from_json, to_timestamp, avg
from pyspark.sql.functions import avg
from pyspark.sql.functions import col


spark = SparkSession.builder \
    .appName("KafkaStream2") \
    .getOrCreate()

# Set partitionOverwriteMode to "static"
spark.conf.set("spark.sql.sources.partitionOverwriteMode", "static")

# Define Kafka consumer options
kafka_bootstrap_servers = "localhost:9092"
kafka_topic_name = "Truck-Data"
kafka_subscribe_type = "subscribe"
kafka_consumer_group = "test_group"

df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", kafka_bootstrap_servers) \
    .option(kafka_subscribe_type, kafka_topic_name) \
    .option("startingOffsets", "earliest") \
    .option("failOnDataLoss", "false") \
    .option("kafkaConsumer.pollTimeoutMs", "512") \
    .option("kafkaConsumer.request.timeout.ms", "10000") \
    .option("kafkaConsumer.session.timeout.ms", "30000") \
    .option("kafkaConsumer.max.poll.records", "1000") \
    .option("kafkaConsumer.auto.offset.reset", "latest") \
    .option("kafkaConsumer.enable.auto.commit", "false") \
    .option("kafkaConsumer.group.id", kafka_consumer_group) \
    .load()


# Define the schema for the messages received from Kafka
schema = StructType([
    StructField("timestamp", StringType()),
    StructField("distance_covered", DoubleType()),
    StructField("engine_speed", DoubleType()),
    StructField("fuel_consumed", DoubleType())    
])

# Convert Kafka messages into structured format using the defined schema
df = df.selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), schema).alias("json")) \
    .select("json.*")



df_select = df.select("timestamp", "distance_covered", "engine_speed", "fuel_consumed")


df2 = df.withColumn("speed_doubled", col("engine_speed") * 1.2)
df3 = df.withColumn("distance_engine_ratio", col("distance_covered") / col("engine_speed"))

# Union the two DataFrames
df_combined = df2.union(df3)
# Compute the ratio between distance_covered and engine_speed
df_combined = df_combined.withColumn("distance_engine_ratio", df_combined["distance_covered"] / df_combined["engine_speed"])
# Select the desired columns
df_combined_select = df_combined.select("speed_doubled", "distance_engine_ratio")



df_filtered = df.filter(col("engine_speed") > 80).alias("filtered")
df_select = df.select("timestamp", "distance_covered", "engine_speed").alias("selected")
df_combined_2 = df_filtered.join(df_select, "timestamp", "inner").select("timestamp", "filtered.distance_covered", "selected.engine_speed")





# Print the received messages to a file
query = df2.select("speed_doubled").coalesce(1).writeStream \
    .outputMode("append") \
    .option("truncate", "false") \
    .format("csv") \
    .option("path", "./../spark_job_outputs/job_output_formats_folder/df2_output.csv") \
    .option("checkpointLocation", "./../spark_job_outputs/df2_checkpoint_folder/") \
    .option("maxRecordsPerFile", 100000) \
    .trigger(processingTime="15 seconds") \
    .start() 


# Print the received messages to the console
query = df2.coalesce(1).writeStream \
    .outputMode("append") \
    .option("truncate", "false") \
    .format("csv") \
    .option("path", "./../spark_job_outputs/job_output_formats_folder/output.csv") \
    .option("checkpointLocation", "./../spark_job_outputs/checkpoint_folder/") \
    .option("maxRecordsPerFile", 100000) \
    .trigger(processingTime="15 seconds") \
    .start() 

# Print the received messages to a file
query = df3.select("distance_engine_ratio").coalesce(1).writeStream \
    .outputMode("append") \
    .option("truncate", "false") \
    .format("csv") \
    .option("path", "./../spark_job_outputs/job_output_formats_folder/df3_output.csv") \
    .option("checkpointLocation", "./../spark_job_outputs/df3_checkpoint_folder") \
    .option("maxRecordsPerFile", 100000) \
    .trigger(processingTime="15 seconds") \
    .start() 

# Print the received messages to a file
query = df_combined_select.coalesce(1).writeStream \
    .outputMode("append") \
    .option("truncate", "false") \
    .format("csv") \
    .option("path", "./../spark_job_outputs/job_output_formats_folder/df_combined_output.csv") \
    .option("checkpointLocation", "./../spark_job_outputs/df_combined_checkpoint_folder") \
    .option("maxRecordsPerFile", 100000) \
    .trigger(processingTime="15 seconds") \
    .start() 


# Print the received messages to a file
query = df_combined_2.coalesce(1).writeStream \
    .outputMode("append") \
    .option("truncate", "false") \
    .format("csv") \
    .option("path", "./../spark_job_outputs/job_output_formats_folder/df_combined_2_output.csv") \
    .option("checkpointLocation", "./../spark_job_outputs/df_combined_2_checkpoint_folder") \
    .option("maxRecordsPerFile", 100000) \
    .trigger(processingTime="15 seconds") \
    .start()



# Start the streaming query and wait for it to finish
query.awaitTermination()

while query.isActive:
    try:
        print(query.lastProgress)
    except KeyboardInterrupt:
        query.stop()
