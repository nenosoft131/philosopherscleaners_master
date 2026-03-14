producer = JsonKafkaProducer(["kafka:9092"])

producer.send(
    topic="test-topic", key="user1", value={"event": "login", "status": "success"}
)

producer.send(topic="test-topic", value={"event": "purchase", "amount": 120})

producer.flush()
producer.close()
