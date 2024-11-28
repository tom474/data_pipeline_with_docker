# Data Pipeline with Docker


## Overview
This project implements a Dockerized data pipeline that integrates multiple big data technologies to process, store, and analyze diverse datasets. The pipeline includes:

- **Apache Kafka**: A distributed streaming platform for real-time data ingestion.
- **Apache Cassandra**: A NoSQL database for scalable and high-performance data storage.
- **Jupyter Notebook**: A robust environment for data analysis and visualization.

The pipeline processes datasets from three APIs:
1. **OpenWeatherMap API**: Streams real-time weather data for selected cities.
2. **Faker API**: Generates synthetic data with customizable fields for testing and analysis.
3. **The Movie Database (TMDB) API**: Collects movie-related metadata for comprehensive insights.

By integrating real-time and synthetic data sources, this project demonstrates the practical application of modern data engineering tools to handle, store, and visualize large datasets for actionable insights.


## Instructions
You need to apply for some APIs to use with this. The APIs might take days for application to be granted access. Sample API keys are given, but it can be blocked if too many users are running this.

- OpenWeatherMap API: https://openweathermap.org/api
- Faker API: https://faker.readthedocs.io/en/master/providers.html
- The Movie Database (TMDB): https://www.themoviedb.org/

After obtaining the API keys, please update the files "owm-producer/openweathermap_service.cfg" accordingly.

### 1. Create Docker Networks
```bash
$ docker network create kafka-network          # Create network for Kafka services.
$ docker network create cassandra-network      # Create network for Cassandra services.
$ docker network ls                            # Verify network creation.
```

### 2. Starting Cassandra and Kafka
```bash
$ docker-compose -f cassandra/docker-compose.yml up -d  # Start Cassandra.
$ docker-compose -f kafka/docker-compose.yml up -d      # Start Kafka.
$ docker ps -a                                          # Check running containers.
```

### 3. Access Kafka UI Frontend
- **Open the Kafka UI:**
    - Navigate to http://localhost:9000 in your web browser.
    - Use the following credentials to log in:
        - **Username:** `admin`
        - **Password:** `bigbang`

- **Add a Data Pipeline Cluster:**
    - After logging in, click on the option to add a new cluster.
    - Enter the following details:
        - **Cluster Name:** `MyCluster`
        - **Cluster Zookeeper:** `zookeeper:2181`
    - Save the configuration to connect the cluster to the UI.

### 4. Starting Cassandra Sinks
You have to manually go to CLI of the "kafka-connect" container and run the below comment to start the Cassandra sinks.
```bash
./start-and-wait.sh
```

### 5. Starting Producers
```bash
$ docker-compose -f owm-producer/docker-compose.yml up -d   # Start OpenWeatherMap producer.
$ docker-compose -f faker-producer/docker-compose.yml up -d # Start Faker producer.
$ docker-compose -f tmdb-producer/docker-compose.yml up -d  # Start TMDB producer.
```

### 6. Starting Consumers
```bash
$ docker-compose -f consumers/docker-compose.yml up -d     # Start Kafka consumers.
```

### 6. Querying Data in Cassandra
First login into Cassandra's container with the following command or open a new CLI from Docker Desktop if you use that.
```bash
$ docker exec -it cassandra bash                        # Access Cassandra container.
```
Once loged in, bring up cqlsh with this command and query weatherreport, fakerdata and movies tables like this:
```bash
$ cqlsh --cqlversion=3.4.4 127.0.0.1                   # Make sure you use the correct cqlversion
cqlsh> desc keyspaces;                                 # View databases.
cqlsh> use kafkapipeline;                              # Switch to kafkapipeline keyspace.
cqlsh> desc tables;                                    # View tables.
cqlsh:kafkapipeline> select * from weatherreport;      # Query data from weatherreport table.
cqlsh:kafkapipeline> select * from fakerdata;          # Query data from fakerdata table.
cqlsh:kafkapipeline> select * from movies;             # Query data from movies table.
```

### 6. Visualization
Run the following command the go to http://localhost:8888 and run the visualization notebook accordingly
```bash
$ docker-compose -f data-vis/docker-compose.yml up -d  # Start Jupyter Notebook.
```

### 7. Teardown
To stop all running kakfa cluster services:
```bash
$ docker-compose -f data-vis/docker-compose.yml down           # Stop visualization
$ docker-compose -f consumers/docker-compose.yml down          # Stop consumers
$ docker-compose -f owm-producer/docker-compose.yml down       # Stop owm producer
$ docker-compose -f faker-producer/docker-compose.yml down     # Stop faker producer
$ docker-compose -f tmdb-producer/docker-compose.yml down      # Stop tmdb producer
$ docker-compose -f kafka/docker-compose.yml down              # Stop kafka
$ docker-compose -f cassandra/docker-compose.yml down          # Stop cassandra
```
To remove the kafka and cassandra network:
```bash
$ docker network rm kafka-network            # Remove kafka network
$ docker network rm cassandra-network        # Remove cassandra network
```
To remove resources in Docker:
```bash
$ docker container prune    # Remove stopped containers
$ docker volume prune       # Remove all volumes
$ docker image prune -a     # Remove all images
$ docker builder prune      # Remove all build cache
$ docker system prune -a    # Remove everything
```

## The Movie Database (TMDB) API


## Data Visualization & Analysis


## Practical Implication of the Project