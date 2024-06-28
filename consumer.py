from kafka import KafkaConsumer
import json
import psycopg2
from psycopg2.extras import execute_values
import os
from dotenv import load_dotenv

load_dotenv()

# PostgreSQL connection setup
conn = psycopg2.connect(
    dbname="kafka_events",
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    host="localhost",
    port="5432"
)
cur = conn.cursor()

# Initialize Kafka consumer
consumer = KafkaConsumer(
    'button_clicks', 'page_views',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

print("Starting Kafka Consumer...")

for message in consumer:
    event_data = message.value
    print('Consumed event:', event_data)
    
    try:
        if message.topic == 'button_clicks':
            query = "INSERT INTO button_clicks (action, timestamp) VALUES %s"
        elif message.topic == 'page_views':
            query = "INSERT INTO page_views (action, timestamp) VALUES %s"
        values = [(event_data['action'], event_data['timestamp'])]
        execute_values(cur, query, values)
        conn.commit()
        print('Inserted event into PostgreSQL')
    except Exception as e:
        print(f'Error inserting event into PostgreSQL: {e}')
        conn.rollback()
