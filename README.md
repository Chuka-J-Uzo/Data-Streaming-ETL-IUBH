

# Real-time Streaming Application with Visualizer

This "Data-Streaming-ETL-IUBH" repository is developed as a real-time streaming application that captures data from a python app that simulates streamed data from the movement of a truck as its source and ingests it into a data store for analysis and visualization. The goal is to provide a comprehensive solution that enables one to build, deploy and monitor your real-time data pipeline with ease.

![Spark Query Metrics](/home/blackjack/Pictures/Screenshots/Spark Query Metrics.png "Spark Query Metrics")


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

As you observe in the dataset, the headers in the context of "Orientation" from the moving device are the column names in the dataset. They are:

    ```time:``` The timestamp when the orientation data was recorded.

    ```seconds_elapsed:``` The number of seconds that have elapsed since the device was turned on (i.e., the uptime).

    ```qz, qy, qx, and qw:``` The components of the quaternion that represents the device's orientation. These values describe the device's rotation in 3D space.

    ```roll, pitch, and yaw:``` The Euler angles that describe the device's orientation. These values represent the rotation around the X, Y, and Z axes, respectively.

    The quaternion components ```qz, qy, qx, and qw``` are related to the ```Euler angles roll, pitch, and yaw``` through a mathematical transformation. The ```seconds_elapsed``` column is not directly related to the other columns, but it can be used to calculate the time difference between successive orientation measurements.


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


