import json

from aiokafka import AIOKafkaProducer

import settings


class BrokerProducer:
    _producer: AIOKafkaProducer | None = None

    async def __aenter__(self):
        self._producer = AIOKafkaProducer(bootstrap_servers=settings.BROKER_URL)
        await self._producer.start()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._producer.stop()
        self._producer = None

    def send_message(self, topic: str, message_type: str, message: dict):
        if self._producer is None:
            raise Exception("Producer not started")
        data = {
            "message_type": message_type,
            "message": message,
        }
        return self._producer.send(topic, json.dumps(data).encode("utf-8"))


producer = BrokerProducer()
