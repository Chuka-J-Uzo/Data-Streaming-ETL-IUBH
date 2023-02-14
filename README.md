

# Real-time Streaming Application with Visualizer

This "Data-Streaming-ETL-IUBH" repository is developed as a real-time streaming application that captures data from a file (CSV) source and ingests it into a data store for analysis and visualization. The goal is to provide a comprehensive solution that enables one to build, deploy and monitor your real-time data pipeline with ease.

![image](https://user-images.githubusercontent.com/95084188/218446337-c83e8779-ce42-4f0c-8db0-f55f88d4df17.png)

## The Dataset

The dataset was collected from a moving device, across a 70 km drive. An application in a mobile device was used to extract the phone's "Orientation" values during this trip that lasted 2 - 3 hrs. 

A snippet of the data looks like this:

```
| time                | seconds_elapsed   | qz                | qy                | qx                 | qw                | roll              | pitch              | yaw               |
+---------------------+-------------------+-------------------+-------------------+--------------------+-------------------+-------------------+--------------------+-------------------+
| 28-10-2022 04:55:56 |   0.1645263671875 | 0.495980978012085 | 0.188404202461243 | 0.0901745185256004 | 0.842837631702423 | 0.244929581880569 | -0.345741897821426 | -1.02081370353699 |
| 28-10-2022 04:55:56 |   0.1695009765625 | 0.495985835790634 | 0.188402488827705 | 0.0901651754975319 | 0.842836260795593 | 0.244933515787125 | -0.345724999904633 | -1.02082526683807 |
| 28-10-2022 04:55:56 |  0.17450537109375 | 0.495990812778473 | 0.188399642705917 | 0.0901557356119156 | 0.842834949493408 | 0.244935348629951 | -0.345706850290298 | -1.02083742618561  

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
  * MySQL:```8.0.32-debian```
  * phpmyadmin
  * Apache Superset

## Features

    1. Python Clients for connections:  We have used PyMySQL library and confluent-kafka python libraries.
    
    2. Data Ingestion: We have use the python script to collect and transport data from various sources to Apache Kafka.
    
    3. Data Processing: Apache Kafka is used to process the incoming data in real-time and make it available for further analysis.
    
    4. Data Storage: MySQL is used to store the messages as they are being ingested. Kafka ingests row-by-row.
    
    5. Monitoring: Confluent's Control-Centre dashboard is used to monitor the topics and resources in real-time.
    
    6. Data Visualization: Apache Superset is used to create interactive dashboards and visualizations for the ingested data.

## Setup

    1. Docker pull or build all the images above.
    2. Docker run the following containers: Apache ZooKeeper, Apache Kafka, MySQL, phpMyAdmin and the entire Confluent CP-all-in-one library (see docker_configs folder with yamls in the directory) and Apache Superset.
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


