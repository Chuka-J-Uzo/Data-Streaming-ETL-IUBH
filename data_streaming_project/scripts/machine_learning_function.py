from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, to_timestamp
from pyspark.sql.types import StructType, StructField, StringType, DoubleType
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.classification import RandomForestClassifier
from pyspark.ml import Pipeline
from pyspark.ml.classification import LogisticRegression
from pyspark.sql import SQLContext
from pyspark import SparkContext
from pyspark import SparkFiles


sc = SparkContext()
sqlContext = SQLContext (sc)


# Create a Spark session
spark = SparkSession.builder \
    .appName("Truck_Data_Stream (Machine Learning)") \
    .config("spark.jars", "./../mysql_conn-JAR-FILE/mysql-connector-java-8.0.32.jar") \
    .master("local[*]") \
    .getOrCreate()

    

# Define Kafka consumer options
kafka_bootstrap_servers = "localhost:9092"
kafka_topic_name = "Truck-Data"
kafka_subscribe_type = "subscribe"
kafka_consumer_group = "test_group"

schema = StructType([
    StructField("timestamp", StringType()),
    StructField("distance_covered", DoubleType()),
    StructField("engine_speed", DoubleType()),
    StructField("fuel_consumed", DoubleType())
])

# Read data from Kafka
df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", kafka_bootstrap_servers) \
    .option(kafka_subscribe_type, kafka_topic_name) \
    .option("startingOffsets", "earliest") \
    .load() \
    .selectExpr("CAST(value AS STRING)")

# Parse the JSON data and select the required columns
parsed_df = df.select(from_json("value", schema).alias("data")) \
    .select("data.*")



# Every record of this DataFrame contains the label and
# features represented by a vector.
df = sqlContext(parsed_df, ["label", "features"])

# Set parameters for the algorithm.
# Here, we limit the number of iterations to 10.
lr = LogisticRegression(maxIter=10)

# Fit the model to the data.
model = lr.fit(df)

# Given a dataset, predict each point's label, and show the results.
model.transform(df).show()



# Write the output to a console sink
query = model.transform(df).writeStream \
    .format("console") \
    .option("truncate", "false") \
    .start()

# Wait for the query to finish
query.awaitTermination()
