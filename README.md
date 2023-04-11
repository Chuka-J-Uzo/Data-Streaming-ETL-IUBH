

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

-----------------------
### Docker Running MySQL server & Database:
I installed MySQL docker image according to the linux debian on Ubuntu 22.04, but you can find other flavours on ```https://hub.docker.com/_/mysql) ```

    docker pull mysql:8.0.32-debian

Starting our MySQL instance (find this command and details from ```https://hub.docker.com/_/mysql) ```:

    docker run --name MySQL_Container -e MYSQL_ROOT_PASSWORD=root -p 3306:3306 -d mysql:8.0.32-debian

For me, as seen above, I called the docker container "MySQL_Container".

Next, activate your MySQL shell by right-clicking against the MySQL_Container (In vscode) which is our MySQL server.

Then you'll see this prompt waiting for us to login to MySQL ---> ```root@a20370fbdbfc:/# ``` 

Now type this into the shell to login. We use ```'root'``` as ```username -u``` and ```'root' as -p password```. 

The command will look like this ---->    ```mysql -u root  -p```  
If that doesn't work, do this ------>     ```mysql --user=root --password=root``` 

After running MySQL on docker, and you are trying to enter mysql prompt, but you get this error, ```ERROR 2002 (HY000): Can't connect to local MySQL server through socket '/var/run/mysqld/mysqld.sock' (2)```, Just use the command below....replace with your container name and user name, so that it looks like ```sudo docker exec -it <container_name> mysql -u <user_name> -p```
 
    sudo docker exec -it MySQL_Container mysql -u root -p

OTHERWISE USE THIS BELOW:

    mysql --user=root --password=root

Once your login is successful, then we create a database to collect Kafka's producer messages. we will call the database "KAFKA_DB"

      mysql> CREATE DATABASE KAFKA_DB;

Then, we create a table inside this databse. To do this, we use the ```"use"``` command on the created DB as follows:

      mysql> use KAFKA_DB;

Then we create a Table using the schema or column names in the data we are trying to ingest. Our tables are called "INGESTED_TABLE_1", "TRUCK_PARAMETER_MAP", "TRUCK_DISTANCE_CORRELATION", "TRUCK_ENGINE_SPEED_CORRELATION". See below how we use SQL queries to create the respective tables.

    CREATE TABLE INGESTED_TABLE_1 (time float, seconds_elapsed float,  qz float, qy float, qx float, qw float, roll float, pitch float, yaw float);

  
    CREATE TABLE TRUCK_PARAMETER_MAP (
            `id` INT AUTO_INCREMENT PRIMARY KEY,
            `timestamp` DATETIME,
            `distance_covered` FLOAT,
            `engine_speed` FLOAT,
            `fuel_consumed` FLOAT
        );


    CREATE TABLE TRUCK_DISTANCE_CORRELATION (
        `id` INT AUTO_INCREMENT PRIMARY KEY,
        `distance_covered` DOUBLE,
        `time_elapsed` DOUBLE,
        `correlation` DOUBLE
    );

    CREATE TABLE TRUCK_ENGINE_SPEED_CORRELATION (
        `id` INT AUTO_INCREMENT PRIMARY KEY,
        `engine_speed` DOUBLE,
        `time_elapsed` DOUBLE,
        `correlation` DOUBLE
    );

After creating our tables in SQL, we must ensure that our Python code for producing Kafka messages has a function that instructs Python to create a database schema for the messages produced. See what the corresponding code snippets in python will look like below: 


!["Python > MySQL Schema"](./data_streaming_project/image_assets/python%20code%20with%20mysql%20table%20schema.png "Python > MySQL Schema") <br>
*Image above: Python code with MySQL table schema*



!["Python > MySQL Output"](./data_streaming_project/image_assets/Python%20code%20to%20output%20to%20MySQL%20Database.png "Python > MySQL Output") <br>
*Image above: Python code to output to MySQL Database*


### Docker Running Prometheus and Grafana Containers:

After installing Prometheus, you will need a Node-exporter that helps to scrape metrics to be exported.

Step1: Follow this video to download Node-exporter first >> https://www.youtube.com/watch?v=uCYfDtR9S9k&t=26s


    docker run -d \
    --net="host" \
    --pid="host" \
    -v "/:/host:ro,rslave" \
    quay.io/prometheus/node-exporter \
    --path.rootfs=/host


Step 2: Create ```Prometheus.yml``` (see files in the repository)

    global:
    scrape_interval: 5s
    external_labels:
        monitor: 'node'
    scrape_configs:
    - job_name: 'prometheus'
        static_configs:
        - targets: ['192.168.88.97:9090'] ## IP Address of the localhost
    - job_name: 'node-exporter'
        static_configs:
        - targets: ['192.168.88.97:9100'] ## IP Address of the localhost
      

```
For example, 192.168.88.97 was the ip address of our host machine and we get it
by using "ifconfig" command in our linux terminal.

In my case, i got the following when i use it and scrolled to the base wlx.... to 
see the value of the inet address:

 vethcarh8fb: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet6 fe80::687c:9cff:fe4f:bdd2  prefixlen 64  scopeid 0x20<link>
        ether 1a:7c:6c:4f:ad:d2  txqueuelen 0  (Ethernet)
        RX packets 0  bytes 0 (0.0 B)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 494  bytes 88296 (88.2 KB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

wlx28ee520868b9: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 192.164.22.37  netmask 255.255.255.0  broadcast 192.168.88.255
        inet6 ge605:f18f:1098:a20e:587r  prefixlen 64  scopeid 0x20<link>
        ether 16:gg:56:08:68:k9  yxlutullen 1000  (Ethernet)
        RX packets 822150  bytes 955915554 (955.9 MB)
        RX errors 0  dropped 214097  overruns 0  frame 0
        TX packets 470142  bytes 79273897 (79.2 MB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
```

After you've docker pulled (Installing) Prometheus from docker >> https://hub.docker.com/r/prom/prometheus

Bind-mount your prometheus.yml from the host by running the code below
Ensure you cd into the container containing the prometheus.yml before running this code:

    docker run -d --name prometheus -p 9090:9090 -v $PWD/prometheus.yml:/etc/prometheus/prometheus.yml prom/prometheus


Step 4: Install Grafana from docker website >> https://hub.docker.com/r/grafana/grafana

    docker run -d --name=grafana -p 3000:3000 grafana/grafana


When you try to connect prometheus to in Grafana and you get this error: ```Err reading Prometheus: Post "http://localhost:9090/api/v1/query": dial tcp 127.0.0.1:9090: connect: connection refused```, you can just use the docker inspect command to find the IP address of the Prometheus container and then replace the localhost word with it.