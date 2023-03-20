import json
import csv
from kafka import KafkaProducer
from MyConfig import kafka_topic,kafka_bootstrap_servers,dataset_path

def producer():
    producer = KafkaProducer(
    bootstrap_servers=kafka_bootstrap_servers,
    value_serializer=lambda v: json.dumps(v).encode('utf-8'))

    import codecs
    f = codecs.open(dataset_path + 'Bitcoin_tweets.csv', 'r', 'UTF-8')
    reader = csv.DictReader(f, delimiter=",")
    
    for row in reader:
        producer.send(topic=kafka_topic, value=row)
        producer.flush()
        

if __name__ == '__main__':
    producer()