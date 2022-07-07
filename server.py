from socket import socket
from fastapi import FastAPI
import socketio
from typing import Optional
from fastapi import FastAPI, Header
from pydantic import BaseModel
import uvicorn
import control as controller
from fastapi.middleware.cors import CORSMiddleware
#import jwt

app = FastAPI()
sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins='*', logger=True, engineio_logger=True)
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


@app.get("/")
def firstPage():
    return "hello!"

@app.get("/home")
def home():
    return "hello!"

@sio.event
def connect(sid, environ):
    print('connect ', sid)

@sio.event
def disconnect(sid):
    print('disconnect ', sid)

@sio.on('light')
async def pressLightBtn(sid, data):
    print('pressLightBtn', sid, data)
    username = data['username']
    lightOn = data['lightOn']
    lightOnLabel = ''
    if lightOn == True:
        lightOnLabel = 'on'
        controller.turnOnLight()
    else:
        lightOnLabel = 'off'
        controller.turnOffLight()
    await sio.emit('record', {'message' : f'{username} has turned {lightOnLabel} the light.', 'lightOn': controller.lightOn})

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=80)