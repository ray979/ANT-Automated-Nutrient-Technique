#import statements
from fastapi import APIRouter
from models.sensordata import SensorData
from config.database import connection
from schemas.sensordata import sensorDataEntity, listOfSensorDataEntity
from bson import ObjectId

import datetime
import paho.mqtt.client as mqtt
import threading

ant_router = APIRouter()

PH = 0
EC = 0
PH_TOPIC = 'sensor/ph'
EC_TOPIC = 'sensor/ec'

topics = [(PH_TOPIC,0),(EC_TOPIC,0)]

lock = threading.Lock()

def on_message(client, userdata, message):
    global PH
    global EC
    try:
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
    except Exception as e:
        print(f"err: {str(e)}")


client = mqtt.Client("ANT System Web API")
client.on_message = on_message
client.connect("localhost", 1883)
client.subscribe(topics)
client.loop_start()

#hello world test
@ant_router.get("/hello")
async def hello_world():
    return "Hello world"

#getting latest 30 sensorDatas
@ant_router.get('/sensordatas')
async def get_lastest_sensordatas():
    return listOfSensorDataEntity(connection.local.sensorData.find().sort("_id",-1).limit(30))

@ant_router.get('/sensordata')
async def get_latest_sensordata():
    try:
        today = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ph = PH
        ec = EC
        dat = {"time": today, "PH": ph, "EC" : ec}
        print(f"json: {dat}")
        return dat
    except Exception as e:
        print(f"err: {str(e)}")


#get one sensorData with matching sensorData id
@ant_router.get('/sensordata/{sensorDataId}')
async def get_sensordata_by_id(sensorDataId):
    return sensorDataEntity(connection.local.sensorData.find_one({"_id": ObjectId(sensorDataId)}))


#creating a sensorData
@ant_router.post('/sensordata')
async def create_sensordata(sensorData: SensorData):
    connection.local.sensorData.insert_one(dict(sensorData))
    return listOfSensorDataEntity(connection.local.sensorData.find())

#update a sensorData
@ant_router.put('/sensorDatas/{sensorDataId}')
async def update_sensorData(sensorDataId, sensorData: SensorData):
    #find the sensorData and then update it with new sensorData data
    connection.local.sensorData.find_one_and_update(
        {"_id": ObjectId(sensorDataId)},
        {"$set": dict(sensorData)}
    )

    return sensorDataEntity(connection.local.sensorData.find_one({"_id": ObjectId(sensorDataId)}))

#@ant_router.put('/settings/{settingsID}')
#async def update_settings(settingsID, settings: Setting):


#Delete a sensorData
@ant_router.delete('/sensorDatas/{sensorDataId}')
async def delete_sensorData(sensorDataId):
    #finds the sensorData, deletes it and also returns the same sensorData object
    return sensorDataEntity(connection.local.sensorData.find_one_and_delete({"_id": ObjectId(sensorDataId)}))
