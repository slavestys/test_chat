import uuid
import json

from websockets.exceptions import ConnectionClosedError

from core.token import get_token_payload


class SocketHandler:
    user_id = None

    def __init__(self, websocket, callback):
        self.websocket = websocket
        self.callback = callback
        self.id = uuid.uuid4()

    async def handle_messages(self):
        try:
            async for message in self.websocket:
                await self.handle_message(message)
        except ConnectionClosedError:
            pass
        self.eval_callback("socket_close")

    def handle_message(self, message):
        try:
            message = json.loads(message)
        except:
            pass
        match message:
            case {"command": "authenticate", "token": str(token)}:
                return self.handle_authentication(token)
            case {"command": "subscribe", "channel_ids": list(channel_ids)}:
                return self.handle_subscribe(channel_ids)
            case _:
                return self.handle_unknown_command()

    def handle_authentication(self, token):
        payload = get_token_payload(token)
        if not payload:
            return self.send_to_socket({"status": "error", "message": "wrong-token"})
        user_id = payload.get("sub")
        if not user_id:
            return self.send_to_socket({"status": "error", "message": "wrong-token"})
        self.eval_callback("user_authenticated", user_id=user_id)
        self.user_id = user_id
        return self.send_to_socket({"status": "ok", "message": "authenticated"})

    def handle_subscribe(self, channel_ids):
        if not self.user_id:
            return self.send_to_socket({"status": "error", "message": "not-authenticated"})
        self.eval_callback("user_subscribed", channel_ids=channel_ids)
        return self.send_to_socket({"status": "ok", "message": "subscribed"})

    def handle_unknown_command(self):
        return self.send_to_socket({"status": "error", "message": "unknown-command"})

    def eval_callback(self, method, **params):
        params["handler"] = self
        self.callback(method, params)

    def send_to_socket(self, data):
        return self.websocket.send(json.dumps(data))
