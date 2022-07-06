from socket import socket
from fastapi import FastAPI
import socketio
from typing import Optional
from fastapi import FastAPI, Header
from pydantic import BaseModel
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
#import jwt

app = FastAPI()
sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins=['*'])
socket_app = socketio.ASGIApp(sio)
app.mount("/", socket_app)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# @app.get("/")
# def firstPage():
#     return "hello!"

@app.get("/home")
def home():
    return "hello!"

@sio.event
def connect(sid, environ, auth):
    print('connect ', sid)

@sio.on('join')
async def join(sid, data):
    print('join', sid)
    await sio.emit('lobby', 'User join')

@sio.on('light')
async def changeLightStatus(sid, data):
    print('light', sid, data)
    username = data['username']
    lightOn = data['lightOn']
    lightOnLabel = ''
    if lightOn == True:
        lightOnLabel = 'on'
    else:
        lightOnLabel = 'off'
    await sio.emit('record', {'message' : f'{username} has turned {lightOnLabel} the light.'})

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=80)