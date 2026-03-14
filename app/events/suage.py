for i in range(1000):
    producer.send("events", key=f"user{i}", value={"event_id": i})

producer.flush()


class EventService:
    def __init__(self, producer):
        self.producer = producer

    def publish_user_event(self, user_id, action):
        event = {"user_id": user_id, "action": action}

        self.producer.send("user-events", key=user_id, value=event)
