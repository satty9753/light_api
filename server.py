from importlib.resources import path
from socket import socket
from time import timezone
from urllib import request
from fastapi import FastAPI
import socketio
from typing import Optional
from fastapi import FastAPI, Header
from pydantic import BaseModel
import uvicorn
from datetime import datetime
from control import LightController
from dateutil import tz
# from fakeControl import LightController
from fastapi.middleware.cors import CORSMiddleware
import time

app = FastAPI()
controller = LightController()
sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins='*', logger=True, engineio_logger=True)
socket_app = socketio.ASGIApp(sio)
# app.mount("/", socket_app)
app.mount("/connect", socket_app, name='connect')

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/test")
def firstPage():
    return "test"

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
    now = datetime.utcnow()
    zone = "Asia/Taipei"
    dtZone = now.astimezone(tz.gettz(zone))
    timeLabel = dtZone.strftime('%H:%M:%S')
    requestNowTime = time.time()
    interval = requestNowTime - controller.timeInterval
    lightOnLabel = getlightOnLabel(lightOn)
    # 與現在同狀態
    if lightOn == controller.lightOn:
       await sio.emit('record', {'message' : f'[{timeLabel}] {username} 成功{lightOnLabel}了燈', 'lightOn': controller.lightOn}) 
    else :
    # 隔一秒才能操作
        if interval > 1:
            if lightOn == True:
                controller.turnOnLight()
            else:
                controller.turnOffLight()
            controller.timeInterval = requestNowTime
            await sio.emit('record', {'message' : f'[{timeLabel}] {username} 成功{lightOnLabel}了燈', 'lightOn': controller.lightOn})
        else:
            await sio.emit('record', {'message' : f'[{timeLabel}] {username} {lightOnLabel}燈失敗，其他人正在操作', 'lightOn': controller.lightOn})

def getlightOnLabel(lightOn):
    if lightOn == True:
        return '開'
    else:
        return '關'
        

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=3000)