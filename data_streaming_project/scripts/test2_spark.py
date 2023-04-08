from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, window
from pyspark.sql.types import StructType, StructField, StringType, DoubleType


spark = SparkSession.builder \
    .appName("KafkaStream2") \
    .getOrCreate()

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

# Deserialize the Kafka message value as JSON and apply the schema
df = df.selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), schema).alias("json")) \
    .select("json.*")

# Create a window of 5 minutes and calculate the average distance covered, engine speed and fuel consumed for each truck
df2 = df \
    .groupBy(window("timestamp", "5 minutes")) \
    .agg({"distance_covered": "avg", "engine_speed": "avg", "fuel_consumed": "avg"}) \
    .withColumnRenamed("avg(distance_covered)", "avg_distance_covered") \
    .withColumnRenamed("avg(engine_speed)", "avg_engine_speed") \
    .withColumnRenamed("avg(fuel_consumed)", "avg_fuel_consumed")

# Write the processed data to MySQL tables "truck_distance_correlation" and "truck_engine_speed_correlation" and "truck_fuel_consumption"
df2.writeStream \
    .outputMode("update") \
    .option("checkpointLocation", "/tmp/checkpoints") \
    .option("url", "jdbc:mysql://MySQL_Container:3306/KAFKA_DB") \
    .option("dbtable", "TRUCK_DISTANCE_CORRELATION") \
    .option("user", "root") \
    .option("password", "root") \
    .start() \
    .writeStream \
    .format("console") \
    .outputMode("complete") \
    .start()

df2.writeStream \
    .outputMode("update") \
    .option("checkpointLocation", "/tmp/checkpoints") \
    .option("url", "jdbc:mysql://MySQL_Container:3306/KAFKA_DB") \
    .option("dbtable", "TRUCK_ENGINE_SPEED_CORRELATION") \
    .option("user", "root") \
    .option("password", "root") \
    .start() \
    .writeStream \
    .format("console") \
    .outputMode("complete") \
    .start()



# Start the streaming query and wait for it to finish
query.awaitTermination()
