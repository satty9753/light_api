from socket import socket
from time import timezone
from fastapi import FastAPI
import socketio
from typing import Optional
from fastapi import FastAPI, Header
from pydantic import BaseModel
import uvicorn
from datetime import datetime
from control import LightController
import locale
from dateutil import tz
#from fakeControl import LightController
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
controller = LightController()
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

@sio.event
def connect(sid, environ):
    print('connect ', sid)

@sio.event
def disconnect(sid):
    print('disconnect ', sid)

@sio.on('lightStatus')
async def getLightStatus(sid, data):
    print('getLightStatus')
    await sio.emit('record', {'lightOn': controller.lightOn })

@sio.on('light')
async def pressLightBtn(sid, data):
    print('pressLightBtn', sid, data)
    username = data['username']
    lightOn = data['lightOn']
    lightOnLabel = ''
    now = datetime.utcnow()
    zone = "Asia/Taipei"
    dtZone = now.astimezone(tz.gettz(zone))
    timeLabel = dtZone.strftime('%H:%M:%S')
    if lightOn == True:
        lightOnLabel = '開'
        controller.turnOnLight()
    else:
        lightOnLabel = '關'
        controller.turnOffLight()
    await sio.emit('record', {'message' : f'[{timeLabel}] {username} {lightOnLabel}了燈', 'lightOn': controller.lightOn})

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=3000)