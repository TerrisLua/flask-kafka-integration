# Real-Time Event Tracking with Kafka and Flask

This project demonstrates a real-time event tracking system using Kafka, Flask, and PostgreSQL. The application tracks two types of events: button clicks and page views. The data is processed in real-time and displayed in a web interface.

## Features
- **Real-Time Data Processing**: Events are processed in real-time using Kafka.
- **Data Storage**: Event data is stored in a PostgreSQL database.
- **Web Interface**: A simple web interface to display event data.

## Prerequisites
- Python 3.x
- Kafka
- PostgreSQL

## Set Up Python Virtual Environment
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

## Install Dependencies
pip install -r requirements.txt

## Start Zookeeper
bin/zookeeper-server-start.sh config/zookeeper.properties
## Start Kafka
bin/kafka-server-start.sh config/server.properties

## Create Kafka Topics
bin/kafka-topics.sh --create --topic button_clicks --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
bin/kafka-topics.sh --create --topic page_views --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1

## Set Up PostgreSQL Database
Create a database named kafka_events.
Create tables button_clicks and page_views using the schema provided in the application.

## Project Structure
- **app.py: The Flask application.
- **consumer.py: The Kafka consumer that processes events and stores them in PostgreSQL.
- **templates/: Contains the HTML templates for the web interface.
- **static/: Contains static files such as CSS and JavaScript.
- **requirements.txt: List of Python dependencies.



