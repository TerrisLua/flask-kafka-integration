# Real-Time Event Tracking with Kafka and Flask

This project demonstrates a real-time event tracking system using Kafka, Flask, and PostgreSQL. The application tracks two types of events: button clicks and page views. The data is processed in real-time and displayed in a web interface.

## Features
- **Real-Time Data Processing**: Events are processed in real-time using Kafka.
- **Data Storage**: Event data is stored in a PostgreSQL database.
- **Web Interface**: A simple web interface to display event data.

## Prerequisites
- Python 
- Kafka
- PostgreSQL
- Zookeeper

### Set Up Python Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Start Zookeeper & Kafka
```bash
bin/zookeeper-server-start.sh config/zookeeper.properties
bin/kafka-server-start.sh config/server.properties
```

### Create Kafka Topics
```bash
bin/kafka-topics.sh --create --topic button_clicks --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
bin/kafka-topics.sh --create --topic page_views --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
```

### Set Up PostgreSQL Database
Create a database named kafka_events.
Create tables button_clicks and page_views using the schema provided in the application.

## Project Structure
- **app.py**: The Flask application.
- **consumer.py**: The Kafka consumer that processes events and stores them in PostgreSQL.
- **templates/**: Contains the HTML templates for the web interface.
- **static/**: Contains static files such as CSS and JavaScript.
- **requirements.txt: List of Python dependencies.

## Running the Application

1. Start the Flask application:
   ```bash
   python app.py
   ```
2. In a separate terminal, start the Kafka consumer:
   ```bash
   python consumer.py
    ```
## Explanation of Files and Functions

#### app.py
- **Flask Application Setup:** Initializes the Flask app, Kafka producer, and PostgreSQL connection.
- **Endpoints:**
  - `/`: Renders the main page with the button click event.
  - `/send_event`: Handles incoming events and sends them to the appropriate Kafka topic.
  - `/display`: Renders the display page for real-time data.
  - `/get_event_data`: Fetches event data from PostgreSQL to display in the web interface.

#### consumer.py
- **Kafka Consumer Setup:** Initializes the Kafka consumer and PostgreSQL connection.
- **Event Processing:** Listens to Kafka topics (button_clicks and page_views), processes incoming events, and inserts them into PostgreSQL.

#### templates/index.html
- HTML template for the main page with the button click event.

#### templates/display.html
- HTML template for displaying real-time event data.

#### static/display.js
- JavaScript for fetching event data from the server and updating the display in real-time.




