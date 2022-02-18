#import statements
from fastapi import APIRouter
from models.sensordata import SensorData
from config.database import connection
from schemas.sensordata import sensorDataEntity, listOfSensorDataEntity
from bson import ObjectId

ant_router = APIRouter()

#hello world test
@ant_router.get("/hello")
async def hello_world():
    return "Hello world"

#getting latest 30 sensorDatas
@ant_router.get('/sensordata')
async def get_lastest_sensordata():
    return listOfSensorDataEntity(connection.local.sensorData.find().sort("_id",-1).limit(30))

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


#Delete a sensorData
@ant_router.delete('/sensorDatas/{sensorDataId}')
async def delete_sensorData(sensorDataId):
    #finds the sensorData, deletes it and also returns the same sensorData object
    return sensorDataEntity(connection.local.sensorData.find_one_and_delete({"_id": ObjectId(sensorDataId)}))