import asyncio

from broker import BrokerConsumer
from observer import event_observer
from ws.connections_handler import ConnectionsHandler
import settings


async def main():
    connections_handler = ConnectionsHandler(port=settings.WEBSOCKET_PORT)
    websocket_task = asyncio.create_task(connections_handler.loop())
    event_observer.register("message", connections_handler.send_message_to_channel)
    event_observer.register("chat_join", connections_handler.user_join_to_channel)
    broker_consumer = BrokerConsumer("messages", broker_url=settings.BROKER_URL)
    async with broker_consumer:
        broker_task = asyncio.create_task(broker_consumer.receive_messages())
        try:
            await asyncio.gather(broker_task, websocket_task)
        except asyncio.CancelledError:
            pass

asyncio.run(main())