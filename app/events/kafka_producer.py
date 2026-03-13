from kafka import KafkaProducer
import json

producer = KafkaProducer(
    bootstrap_servers=["kafka:9092"],
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    retries=5,
)

future = producer.send("test-topic", {"message": "hello kafka"})

try:
    record_metadata = future.get(timeout=10)
    print("Sent to:")
    print("Topic:", record_metadata.topic)
    print("Partition:", record_metadata.partition)
    print("Offset:", record_metadata.offset)

except Exception as e:
    print("Kafka send failed:", e)

finally:
    producer.flush()
    producer.close()
