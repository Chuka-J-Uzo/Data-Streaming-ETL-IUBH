

# Real-time Streaming Application with Visualizer

This "Data-Streaming-ETL-IUBH" repository is developed as a real-time streaming application that captures data from a python app that simulates streamed data from the movement of a truck as its source and ingests it into a data store for analysis and visualization. The goal is to provide a comprehensive solution that enables one to build, deploy and monitor your real-time data pipeline with ease.

![Spark Query Metrics](./data_streaming_project/image_assets/Spark%20Query%20Metrics.png "Spark Query Metrics") <br>
*Image above: Spark Query Metrics generated while spark was running*

![DAG - Visualization](./data_streaming_project/image_assets/DAG%20(Directed%20Acyclic%20Graph)%20visualization.png "DAG - Visualization") <br>
*Image above: DAG (Directed Acyclic Graph) Visualization of our Spark Logic.*

!["Query Stage ID and Task ID"](./data_streaming_project/image_assets/Query%20Stage%20ID%20and%20Task%20ID.png "Query Stage ID and Task ID") <br>
*Image above: Query Stage ID and Task ID*


## The Dataset

The dataset was collected from a moving device, across a 70 km drive. An application in a mobile device was used to extract the phone's "Orientation" values during this trip that lasted 2 - 3 hrs. 

A snippet of the data looks like this:

```
INSERT INTO `TRUCK_PARAMETER_MAP` 
(`id`, `timestamp`, `distance_covered`, `engine_speed`, `fuel_consumed`) VALUES

(1922346, '2023-04-10 01:02:27', 0, 80.22, 0),
(1922347, '2023-04-10 01:02:28', 0.01, 79.2, 0),
(1922348, '2023-04-10 01:02:28', 0.02, 79.45, 0),
(1922349, '2023-04-10 01:02:29', 0.03, 79.54, 0),
(1922350, '2023-04-10 01:02:29', 0.03, 78.58, 0),
(1922351, '2023-04-10 01:02:29', 0.03, 80.83, 0),
(1922352, '2023-04-10 01:02:29', 0.05, 78.34, 0),
(1922353, '2023-04-10 01:02:30', 0.06, 80.13, 0),
(1922354, '2023-04-10 01:02:30', 0.07, 80.24, 0),
(1922355, '2023-04-10 01:02:30', 0.13, 80.62, 0),  

```

## How the code works

The python code consists of two separate applications, one serving as a Kafka producer script and the other as a Spark data processing script.

The Kafka producer script simulates the movement of a truck by generating random values for engine speed and time elapsed. The script connects to a MySQL database and creates a table named 'TRUCK_PARAMETER_MAP'. The script then generates data for distance covered, fuel consumption rate, and fuel remaining. It checks if the fuel remaining is above 0 and sends the generated data as a JSON object to a Kafka broker using the 'confluent_kafka' package. The package specifies the Kafka broker address and port number, maximum number of messages and maximum size of messages buffered in memory, compression type, and compression level. The 'produce_truck_data' function includes a loop to generate data points for a truck at a rate of approximately 1 point every 4 milliseconds. The script also includes a function to test network and server connection. If the host is reachable, the script will start producing messages to Kafka.


Then the Spark data processing script uses the PySpark library to create a streaming pipeline that reads data from a Kafka topic and processes it. This code reads streaming data from Kafka, transforms it using PySpark DataFrame operations, and writes the output to files or console periodically. The code can be modified to read from different sources or write to different sinks based on the specific use case.
Below is a brief summary of what the code does:

* Imports necessary PySpark modules and logging module.
* Sets up a SparkSession with specific configurations.
* Defines the Kafka consumer options, including the topic to read from, group ID, and consumer settings.
* Reads streaming data from Kafka and casts the value column to string type.
* Parses the JSON-formatted messages from Kafka using a pre-defined schema.
* Performs several transformations on the data, including filtering, selection, union, and computing new columns.
* Writes the resulting data streams to a file or console in CSV format with the specified output mode, location, and trigger settings.
* Starts the streaming query using the defined options and outputs.



## Prerequisites

 1. Docker installed on local machine or cloud IDEs.
 2. Basic knowledge of Apache Kafka, MySQL, Superset, containerization in-general and data visualization.
 3. Understanding of real-time streaming data, message brokering, resource handling and its processing.
 4. Linux OS makes life a lot easier. Avoid Windows OS when embarking on projects like this. 

## Requirements

  * Docker

  * Docker used containers below: 
  * Docker for Visual Studio Code - by Microsoft (Create, manage, and debug containerized applications on Docker)
  * Docker Explorer for Visual Studio Code - by Jun Han (Manage Docker Containers, Docker Images, Docker Hub and Azure Container Registry)
  * Apache Kafka (image source: ubuntu/kafka:latest)
  * Apache ZooKeeper  (image source: ubuntu/zookeeper:latest)
  * Apache Spark (image source: ruslanmv/pyspark-elyra:latest)
  * MySQL Server and Database:```version: 8.0.32-debian``` (image source: mysql:8.0.32-debian)
  * PhpMyAdmin:  (image source: phpmyadmin:latest) 
  * Prometheus for metrics logging (image source: prom/prometheus:latest)
  * Node-exporter-prometheus (image source: quay.io/prometheus/node-exporter:latest)
  * Grafana (image source: grafana/grafana:latest)
  * Docker-Autocompose (image source: ghcr.io/red5d/docker-autocompose:latest)

## Features

    1. Python Clients for connections:  We have used SqlAlchemy library and Confluent-Kafka python libraries to write our kafka producer code.

    1.1 Then we also use another python client code to write our Pyspark code that instantly receives produced Kafka messages and processes them super fast.
    
    2. Data Ingestion: We have use the python script to collect and transport data from various sources to Apache Kafka.
    
    3. Data Processing: Apache Spark is used to process the incoming data in real-time and make it available for further analysis.
    
    4. Data Storage: MySQL Server and database is used to store the messages as they are being produced. Kafka produces and writes the messages row-by-row to our db, with an acknowledge and append function.
    
    5. Monitoring: Prometheus and Node exporter are to collect, log metrics and resources in real-time.
    
    6. Data Visualization: Grafana dashboard is used to create interactive dashboards and visualizations for the ingested data.

## Setup

    1. Docker pull or build all the images above.
    2. Docker run the following containers: Apache ZooKeeper, Apache Kafka, MySQL, phpMyAdmin (see docker_configs folder with yamls in the directory) and Grafana.
    3. Configure the python script to collect data from sources and transport it to Kafka.
    4. Configure Kafka to process the data


## Getting Started

Install Docker for Visual Studio Code and Docker Explorer for Visual Studio Code on your Ubuntu machine.

1. Install Docker for Visual Studio Code and Docker Explorer for Visual Studio Code on your Ubuntu machine. If you run into issues, check the official Docker installation guide for Ubuntu: https://docs.docker.com/engine/install/ubuntu/


Pull Docker images: Pull the Docker images for the containers you want to use by running the following commands:

        docker pull ubuntu/kafka:latest
        docker pull ubuntu/zookeeper:latest
        docker pull ruslanmv/pyspark-elyra:latest
        docker pull mysql:8.0.32-debian
        docker pull phpmyadmin:latest
        docker pull prom/prometheus:latest
        docker pull quay.io/prometheus/node-exporter:latest
        docker pull grafana/grafana:latest




1. The first step in getting started with this project is to download the latest version of Apache Superset by using the following command:

bash:
```
2. $ docker pull apache/superset
```

Once you have Superset installed, you can start the container using the following command:

bash:
```
3. docker run -d --name superset -p 8090:8088 apache/superset
```

This will start the container and map port ```8090``` on your local machine to port ```8088``` within the container. You can then access the Apache Superset UI by navigating to ```http://localhost:8090 ``` in your web browser.

4. Configuring Apache Superset:

The next step is to configure Apache Superset to work with your real-time streaming data. This includes setting up the database connection, creating a data source, and building a dashboard to visualize the data. The exact steps to do this will vary based on the type of data you are working with, but here are some general guidelines:

    Connect to your database and create a data source
    Create a new dashboard
    Add a chart or graph to the dashboard
    Configure the chart or graph to display the real-time data

Visualizing the Streaming Data

Once you have configured Apache Superset, you can start visualizing your real-time streaming data. This could include creating charts, graphs, and other visualizations that provide insights into the data as it streams in.
Conclusion

In conclusion, this repository provides a guide on how to build a real-time streaming application using the containers above. By following the steps outlined here, you can get up and running quickly and start visualizing your streaming data in real-time. 


