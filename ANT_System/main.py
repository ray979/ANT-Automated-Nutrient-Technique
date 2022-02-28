import datetime
import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt
import threading

import uvicorn
from fastapi import FastAPI
from starlette.templating import Jinja2Templates
from starlette.requests import Request

GPIO.setmode(GPIO.BCM)

app = FastAPI()

templates = Jinja2Templates(directory="templates")
jinja_env = templates.env

PH = 0
EC = 0
PH_TOPIC = 'sensor/ph'
EC_TOPIC = 'sensor/ec'

lock = threading.Lock()

def on_message(client, userdata, message):
    global PH
    if(message.topic == PH_TOPIC):
        print(f'The message is {str(message.payload.decode("utf-8"))}')
        lock.acquire()
        PH = round(float(str(message.payload.decode("utf-8"))),2)
        lock.release()
    if(message.topic == EC_TOPIC):
        print(f'The message is {str(message.payload.decode("utf-8"))}')
        lock.acquire()
        EC = round(float(str(message.payload.decode("utf-8"))),2)
        lock.release()



client = mqtt.Client("ANT System Web API")
client.on_message = on_message
client.connect("localhost", 1883)
client.subscribe([(PH_TOPIC,0), (EC_TOPIC,0)])
client.loop_start()


@app.get("/")
def root(request: Request):
    return templates.TemplateResponse('index.html',
                                      {'request': request})

@app.get("/sensordata")
def returndata():
    """Returns timestamp and PH value from MQTT"""
    try:
        today = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ph = PH
        ec = EC
        dat = {"time": today, "PH": PH, "EC": EC}
        print(f"json: {dat}")
        return dat
    except Exception as e:
        print(f"err: {str(e)}")

    return None



if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
    client.loop_stop()
