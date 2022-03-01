#import statements
from fastapi import APIRouter, Depends
import paho.mqtt.client as _mqtt
from bson import ObjectId
from sqlalchemy.orm import Session
from sqlalchemy import desc
import threading
import datetime
import sys

import models.models as _models
from config.database import SessionLocal
import schemas.schemas as _schemas

#FastAPI router
ant_router = APIRouter()

#sensor readings and settings intial values
PH = 0
EC = 0
PH_MIN = 0
PH_MAX = 0
EC_MIN = 0
LIGHT_ON_HOUR = 0
LIGHT_OFF_HOUR = 0

#MQTT Topic for ph and ec readings
PH_TOPIC = 'sensor/ph'
EC_TOPIC = 'sensor/ec'

#MQTT Topics and Qos level
topics = [
    (PH_TOPIC,0),
    (EC_TOPIC,0),    
    ('/PHMINSET',0),
    ('/PHMAXSET',0),
    ('/ECMINSET',0),
    ('/LIGHSTARTSET',0),
    ('/LIGHTENDSTART',0)
]


#thread lock
lock = threading.Lock()

#On message for MQTT, obtain sensor readings and settings from ANT backend through MQTT
def on_message(client, userdata, message):
    global PH
    global EC
    try:
        if(message.topic == PH_TOPIC):
            print(f'The message is {str(message.payload.decode("utf-8"))}')
            lock.acquire()
            PH = round(float(str(message.payload.decode("utf-8"))),2)
            lock.release()
        elif(message.topic == EC_TOPIC):
            print(f'The message is {str(message.payload.decode("utf-8"))}')
            lock.acquire()
            EC = round(float(str(message.payload.decode("utf-8"))),2)
            lock.release()
        elif(message.topic == topics[2][0]):
            print(f'The message is {str(message.payload.decode("utf-8"))}')
            lock.acquire()
            PH_MIN = round(float(str(message.payload.decode("utf-8"))),2)
            print(f'PH Min value changed {PH_MIN}')
            lock.release()
        elif(message.topic ==  topics[3][0]):
            print(f'The message is {str(message.payload.decode("utf-8"))}')
            lock.acquire()
            PH_MAX = round(float(str(message.payload.decode("utf-8"))),2)
            print(f'PH Max value changed {PH_MAX}')
            lock.release()
        elif(message.topic == topics[4][0]):
            print(f'The message is {str(message.payload.decode("utf-8"))}')
            lock.acquire()
            EC_MIN = round(float(str(message.payload.decode("utf-8"))),2)
            print(f'EC Min value changed {EC_MIN}')
            lock.release()
        elif(message.topic == topics[5][0]):
            print(f'The message is {str(message.payload.decode("utf-8"))}')
            lock.acquire()
            LIGHT_ON_HOUR = round(int(str(message.payload.decode("utf-8"))),2)
            print(f'LIGHT Start Hour value changed {LIGHT_ON_HOUR}')
            lock.release()
        elif(message.topic == topics[6][0]):
            print(f'The message is {str(message.payload.decode("utf-8"))}')
            lock.acquire()
            LIGHT_OFF_HOUR = round(int(str(message.payload.decode("utf-8"))),2)
            print(f'LIGHT Off Hour value changed {LIGHT_OFF_HOUR}')
            lock.release()
    except Exception as e:
        print(f"err: {str(e)}")


#Connect to mqtt broker and subscribe to MQTT topics
try:
    client = _mqtt.Client("ANT System Web API")
    client.on_message = on_message
    client.connect("localhost", 1883)
    client.subscribe(topics)
    client.loop_start()
except Exception as e:
    print(e)
    print("Could not connect to Mosquitto broker. Please start MQTT broker")
    sys.exit()

#hello world test
@ant_router.get("/hello")
async def hello_world():
    return "Hello world"

#get local database session
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


# Get a specific max number of query from sqlite database
async def get_recent_sensordatas(maxquery, db: Session = Depends(get_db)):
    sensorDataList = db.query(_models.SensorData).order_by(_models.SensorData.id.desc()).limit(maxquery).all()
    return _schemas.listOfSensorDataEntity(sensorDataList)


#getting latest 30 sensorDatas
@ant_router.get('/sensordatas')
async def get_lastest_sensordatas(db: Session = Depends(get_db)):
    return await get_recent_sensordatas(336, db) #return max data from recent week


#add new sensordata to database
@ant_router.post('/sensordata')
async def add_sensor_data(sensordata: _schemas.SensorDataCreate, db: Session = Depends(get_db)):
    sensordata_model = _models.SensorData() #create variable with same database data format as set in models
    sensordata_model.ph_reading = sensordata.ph
    sensordata_model.ec_reading = sensordata.ec

    db.add(sensordata_model) #add reading to database
    db.commit() #commit to database
    return _schemas.sensorDataEntity(sensordata_model)

#get current sensor readings (ie.last update to PH and EC from MQTT message)
@ant_router.get('/sensordata')
async def get_current_sensordata():
    try:
        today = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ph = PH
        ec = EC
        dat = {"time": today, "PH": ph, "EC" : ec}
        print(f"json: {dat}")
        return dat
    except Exception as e:
        print(f"err: {str(e)}")

#Return settings as gotten from MQTT onmessage calls
@ant_router.get('/settings')
async def get_current_setting():
    try:
        ph_min = PH_MIN
        ph_max = PH_MAX
        ec_min = EC_MIN
        light_hour_on = LIGHT_ON_HOUR
        light_hour_off = LIGHT_OFF_HOUR
        settings = {"phmin":ph_min, "phmax":ph_max, "ecmin":ec_min, "lighthouron":light_hour_on, "lighthouroff":light_hour_off}
        return settings
    except Exception as e:
        print(f"err: {str(e)}")

#Publish new setting values from post to MQTT topics
@ant_router.post('/settings')
async def update_settings(settings: _schemas.Settings):
    client.publish(topics[2][0],settings.phmax)
    client.publish(topics[3][0],settings.phmin)
    client.publish(topics[4][0],settings.ecmin)
    client.publish(topics[5][0],settings.lighthouron)
    client.publish(topics[6][0],settings.lighthouroff)

#Delete record from database base on its id/index
@ant_router.get('/deleteRecord/<int:id>')
async def delete_sensordata(id, db: Session = Depends(get_db)):
    if(db.query(_models.SensorData).filter(_models.SensorData.id == id).delete()):
        db.commit()
        return f"SensorData with id:{id} deleted"

    return f"SensorData with id:{id} does not exist, not deleted"

#Search for list of sensordata from database based on date
@ant_router.get('/searchSensorDatasByDate/<datetime.date:date>')
async def search_sensordata_by_date(date, db: Session = Depends(get_db)):
    sensorDataList = db.query(_models.SensorData).filter(_models.SensorData.date_posted == date).all()
    return _schemas.listOfSensorDataEntity(sensorDataList)
