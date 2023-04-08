from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, window
from pyspark.sql.types import StructType, StructField, StringType, DoubleType


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

# Create a window of 5 minutes and calculate the average distance covered, engine speed and fuel consumed for each truck


# Write the processed data to MySQL tables "truck_distance_correlation" and "truck_engine_speed_correlation" and "truck_fuel_consumption"

    
# Print the received messages to the console
    
query = df.coalesce(1).writeStream \
    .outputMode("append") \
    .option("truncate", "false") \
    .format("csv") \
    .option("path", "./../spark_job_outputs/job_output_formats_folder/output.csv") \
    .option("checkpointLocation", "./../spark_job_outputs/checkpoint_folder/") \
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
