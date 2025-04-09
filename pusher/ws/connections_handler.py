from collections import defaultdict
import asyncio
import json

from websockets.asyncio.server import serve, broadcast

from .socket_handler import SocketHandler


class ConnectionsHandler:
    def __init__(
            self,
            host: str = "",
            port: int = 8001
    ):
        self.host = host
        self.port = port
        self.channel_user_ids = defaultdict(set)
        self.user_id_sockets = defaultdict(dict)
        self.user_id_channels = defaultdict(set)

    async def loop(self):
        try:
            async with serve(self.handle_connection, self.host, self.port) as server:
                await server.serve_forever()
        except asyncio.CancelledError:
            pass

    def send_message_to_channel(self, chat_id=None, **message):
        if not chat_id:
            return
        chat_id = int(chat_id)
        sockets = [socket.websocket for user_id in self.channel_user_ids[chat_id] for socket in self.user_id_sockets[user_id].values()]
        if not sockets:
            return
        broadcast(sockets, json.dumps(message))

    def user_join_to_channel(self, user_id=None, chat_id=None):
        if not user_id or not chat_id:
            return
        self.subscribe_user_to_channels(user_id, channel_ids=[chat_id])

    def handle_connection(self, websocket):
        handler = SocketHandler(websocket, self.socket_handler_callback)
        return handler.handle_messages()

    def socket_handler_callback(self, method, params):
        method = getattr(self, method)
        method(**params)

    def user_authenticated(self, *, user_id, handler: SocketHandler):
        self.user_id_sockets[user_id][handler.id] = handler

    def user_subscribed(self, channel_ids: list[int], handler: SocketHandler):
        user_id = handler.user_id
        self.subscribe_user_to_channels(user_id, channel_ids)

    def subscribe_user_to_channels(self, user_id, channel_ids):
        for channel_id in channel_ids:
            self.channel_user_ids[channel_id].add(user_id)
        self.user_id_channels[user_id].update(channel_ids)

    def socket_close(self, handler: SocketHandler):
        user_id = handler.user_id
        if not user_id:
            return
        if handler.id in self.user_id_sockets[user_id]:
            del self.user_id_sockets[user_id][handler.id]
        if not self.user_id_sockets[user_id]:
            channel_ids = self.user_id_channels[user_id]
            del self.user_id_channels[user_id]
            for channel_id in channel_ids:
                self.channel_user_ids[channel_id].remove(user_id)






