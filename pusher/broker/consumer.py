import asyncio
from aiokafka import AIOKafkaConsumer
import json

from observer import event_observer


class BrokerConsumer:
    _consumer: AIOKafkaConsumer | None = None

    def __init__(self, *topics, broker_url):
        self.topics = topics
        self.broker_url = broker_url
        self.callbacks = []

    async def __aenter__(self):
        self._consumer = AIOKafkaConsumer(*self.topics, bootstrap_servers=self.broker_url)
        await self._consumer.start()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._consumer.stop()
        self._producer = None

    async def receive_messages(self):
        if self._consumer is None:
            raise Exception("Consumer not started")
        try:
            async for msg in self._consumer:
                print("consumed: ", msg.topic, msg.partition, msg.offset,
                      msg.key, msg.value, msg.timestamp)
                message = self.parse_message(msg.value)
                self.emit_event(**message)
        except asyncio.CancelledError:
            pass

    @staticmethod
    def parse_message(message):
        try:
            return json.loads(message)
        except:
            print("Wrong message")
            return None

    @staticmethod
    def emit_event(message_type=None, message=None):
        if not message_type or not message:
            return
        event_observer.emit(message_type, **message)