import json

from fastapi import FastAPI, Body
from starlette.websockets import WebSocket, WebSocketDisconnect

from server.classes import Chat, ChatMessage

app = FastAPI()
chat = Chat()


# REST API 로 채팅방 생성
@app.get('/chat')
def find_all_room():
    return chat.get_all_rooms()


@app.post('/chat')
def create_room(name: str = Body(..., embed=True)):
    return chat.create_room(name)


@app.websocket('/ws')
async def ws_endpoint(ws: WebSocket):
    await ws.accept()
    while True:
        try:
            data = await ws.receive_text()
            msg = ChatMessage(**json.loads(data))
            await chat.msg_handler(msg, ws)
        except WebSocketDisconnect:
            # 연결 끊겼을 때 처리하기
            print("ws 끊김")
