

# Real-time Streaming Application with Visualizer

This "Data-Streaming-ETL-IUBH" repository is developed as a real-time streaming application that captures data from a file (CSV) source and ingests it into a data store for analysis and visualization. The goal is to provide a comprehensive solution that enables one to build, deploy and monitor your real-time data pipeline with ease.

## Prerequisites

 * Docker installed on local machine or cloud IDEs.
 * Basic knowledge of Apache Kafka, MySQL, Superset, containerization in-general and data visualization.
 * Understanding of real-time streaming data, message brokering, resource handling and its processing.
 * Linux OS makes life a lot easier. Avoid Windows OS when embarking on projects like this. 

## Requirements

  * Docker

  * Docker used containers below: 
  * Portainer (Resource monitor and manager for Docker containers)
  * Apache Kafka
  * Apache ZooKeeper
  * Confluent-All-In-One 7.3.1 containers:
      * Control-centre 7.3.1
      * Ksqldb-cli 7.3.1
      * Ksql-datagen 7.3.1
      * Ksqldb-server 7.3.1
      * Server-connect-datagen:0.5.3-7.1.0
      * Kafka-Rest-Proxy 7.3.1
      * Schema-Registry 7.3.1
      * Kafka Broker server 7.3.1
      * ZooKeeper 7.3.1
  * MySQL:8.0.32-debian
  * phpmyadmin
  * Apache Superset

## Features

    * Python Clients for connections: We have used PyMySQL library and confluent-kafka python libraries.
    * Data Ingestion: We have use the python script to collect and transport data from various sources to Apache Kafka.
    * Data Processing: Apache Kafka is used to process the incoming data in real-time and make it available for further analysis.
    * Data Storage: MySQL is used to store the messages as they are being ingested. Kafka ingests row-by-row.
    * Monitoring: Confluent's Control-Centre dashboard is used to monitor the topics and resources in real-time.
    * Data Visualization: Apache Superset is used to create interactive dashboards and visualizations for the ingested data.

## Setup

    1. Docker pull or build all the images above.
    2. Docker run the following containers: Apache ZooKeeper, Apache Kafka, MySQL, phpMyAdmin and the entire Confluent CP-all-in-one library (see docker_configs folder with yamls in the directory) and Apache Superset.
    3. Configure the python script to collect data from sources and transport it to Kafka.
    4. Configure Kafka to process the data


## Getting Started

1. The first step in getting started with this project is to download the latest version of Apache Superset by using the following command:

bash:
2. docker pull apache/superset

Once you have Superset installed, you can start the container using the following command:

bash:
3. docker run -d --name superset -p 8090:8088 apache/superset

This will start the container and map port 8090 on your local machine to port 8088 within the container. You can then access the Apache Superset UI by navigating to http://localhost:8090 in your web browser.

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


