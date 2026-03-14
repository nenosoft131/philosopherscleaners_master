class JsonKafkaProducer(KafkaProducerInterface):
    def __init__(self, servers):
        self.producer = KafkaProducer(
            bootstrap_servers=servers,
            key_serializer=lambda k: k.encode("utf-8") if k else None,
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
            retries=5,
            linger_ms=5,
        )

    def send(self, topic, key=None, value=None):
        future = self.producer.send(topic, key=key, value=value)
        future.add_callback(self.on_success)
        future.add_errback(self.on_error)

    def on_success(self, record_metadata):
        print(
            f"Sent to {record_metadata.topic} "
            f"partition={record_metadata.partition} "
            f"offset={record_metadata.offset}"
        )

    def on_error(self, exc):
        print("Kafka error:", exc)

    def flush(self):
        self.producer.flush()

    def close(self):
        self.producer.close()
