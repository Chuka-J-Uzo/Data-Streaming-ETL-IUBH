from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, StringType



spark = SparkSession.builder \
    .appName("KafkaStream") \
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
schema = StructType([StructField("message", StringType())])

# Deserialize the Kafka message value as JSON and apply the schema
df = df.selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), schema).alias("json")) \
    .select("json.message")

# Print the received messages to the console
query = df.writeStream \
    .outputMode("append") \
    .format("console") \
    .start()

# Start the streaming query and wait for it to finish
query.awaitTermination()
