from flask import Flask, render_template, jsonify, request
from kafka import KafkaProducer
import json
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from collections import defaultdict
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os 

load_dotenv()

app = Flask(__name__)
print("Starting application")

# Database setup
DB_USER=os.getenv('DB_USER')
DB_PASSWORD=os.getenv('DB_PASSWORD')
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@localhost:5432/kafka_events"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class ButtonClick(Base):
    __tablename__ = "button_clicks"
    id = Column(Integer, primary_key=True, index=True)
    action = Column(String, index=True)
    timestamp = Column(DateTime, index=True)

class PageView(Base):
    __tablename__ = "page_views"
    id = Column(Integer, primary_key=True, index=True)
    action = Column(String, index=True)
    timestamp = Column(DateTime, index=True)

# Create the tables
Base.metadata.create_all(bind=engine)

print("Starting Kafka Producer...")
# Initialize Kafka producer
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_event', methods=['POST'])
def send_event():
    event_data = request.json
    print('Received event:', event_data)
    event_data['timestamp'] = datetime.utcnow().isoformat()
    event_type = event_data.get('event_type')

    # Send event to the appropriate Kafka topic based on event type
    if event_type == 'click':
        producer.send('button_clicks', value=event_data)
    elif event_type == 'page_view':
        producer.send('page_views', value=event_data)
    else:
        return jsonify({'status': 'error', 'message': 'Unknown event type'}), 400

    producer.flush()
    print('Sent event to Kafka:', event_data)
    return jsonify({'status': 'success', 'data': event_data})

@app.route('/display')
def display():
    return render_template('display.html')

@app.route('/get_event_data')
def get_event_data():
    event_type = request.args.get('event_type')
    session = SessionLocal()
    one_week_ago = datetime.utcnow() - timedelta(days=7)
    
    if event_type == 'click':
        events = session.query(ButtonClick).filter(ButtonClick.timestamp >= one_week_ago).all()
    elif event_type == 'page_view':
        events = session.query(PageView).filter(PageView.timestamp >= one_week_ago).all()
    else:
        return jsonify({'status': 'error', 'message': 'Unknown event type'}), 400

    count_by_day = defaultdict(int)
    for event in events:
        day = event.timestamp.strftime('%Y-%m-%d')
        count_by_day[day] += 1

    response_data = [{'timestamp': day, 'count': count} for day, count in sorted(count_by_day.items())]
    print(f'Sending {event_type} data:', response_data)
    return jsonify(response_data)

if __name__ == '__main__':
    app.run(debug=True)
