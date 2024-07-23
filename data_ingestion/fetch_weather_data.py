import requests
import json
from kafka import KafkaProducer
import time

def fetch_weather_data(api_url, api_key, location):
    response = requests.get(f"{api_url}?q={location}&appid={api_key}")
    data = response.json()
    return data

def produce_messages(producer, topic, data):
    producer.send(topic, json.dumps(data).encode('utf-8'))

if __name__ == "__main__":
    api_url = "http://api.openweathermap.org/data/2.5/weather"
    api_key = "your_api_key"
    location = "New York"
    kafka_topic = "weather"
    kafka_producer = KafkaProducer(bootstrap_servers='localhost:9092')

    while True:
        data = fetch_weather_data(api_url, api_key, location)
        produce_messages(kafka_producer, kafka_topic, data)
        time.sleep(600)  # Fetch new data every 10 minutes
