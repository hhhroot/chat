import uuid
from typing import List

from starlette.websockets import WebSocket


class ChatMessage:
    def __init__(self, **kwargs):
        self.msg_type = kwargs['msg_type']
        self.room_id: str = kwargs['room_id']
        self.sender: str = kwargs['sender']
        self.msg: str = kwargs['msg']


class ChatRoom:
    def __init__(self, r_id, r_name):
        self.id: str = r_id
        self.name: str = r_name
        self.wss: List[WebSocket] = []

    async def broadcast(self, message):
        for ws in self.wss:
            await ws.send_text(message)

    def append_ws(self, ws):
        self.wss.append(ws)

    def remove_ws(self, ws):
        self.wss.remove(ws)


class Chat:
    def __init__(self):
        self.rooms = {}

    def create_room(self, r_name) -> str:
        r_id = str(uuid.uuid4())
        room = ChatRoom(r_id, r_name)
        self.rooms[r_id] = room
        return str(r_id)

    def get_all_rooms(self) -> List[ChatRoom]:
        return list(self.rooms.values())

    def get_room(self, r_id) -> ChatRoom:
        return self.rooms.get(r_id)

    async def msg_handler(self, chat_msg: ChatMessage, ws: WebSocket):
        room = self.get_room(chat_msg.room_id)

        if chat_msg.msg_type == "ENTER":
            room.append_ws(ws)
            await room.broadcast(f'{chat_msg.sender}님이 입장하셨습니다.')
        elif chat_msg.msg_type == "TALK":
            await room.broadcast(f'{chat_msg.sender}: {chat_msg.msg}')
        elif chat_msg.msg_type == "QUIT":
            room.remove_ws(ws)
