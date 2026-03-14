from kafka import KafkaProducer
import json


class KafkaProducerInterface:
    def send(self, topic, key, value):
        raise NotImplementedError

    def close(self):
        raise NotImplementedError
