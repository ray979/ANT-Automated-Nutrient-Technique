#schemas helps to serailize and also convert sqlite format json to the format our React frontend will read

#import statements
from pydantic import BaseModel, Field
import datetime

#convert database object to dictionary output
def sensorDataEntity(db_item) -> dict:
    return {
        "id": db_item.id,
        "ph": db_item.ph_reading,
        "ec": db_item.ec_reading,
        "date_posted": db_item.date_posted,
        "time_posted": db_item.datetime_posted.strftime('%H:%M:%S'),
        "datetime_posted":db_item.datetime_posted

    }

#convert list of database object to list of sensordataentity
def listOfSensorDataEntity(db_item_list) -> list:
    list_sens_entity = []
    for item in db_item_list:
        list_sens_entity.append(sensorDataEntity(item))

    return list_sens_entity

#Schemas for specifying the specific format and types of values that can used in post requests
#format for entering sensordata into post request
class SensorData(BaseModel):
    ph: float = Field(ge = 0, le = 14)
    ec: float

#format for passing a new sensordata for creating
class SensorDataCreate(SensorData):
    pass

#format for passing settings values into post
class Settings(BaseModel):
    phmin:float = Field(ge = 0)
    phmax:float = Field(le = 14)
    ecmin:float = Field(ge = 0)
    lighthouron:int = Field(ge = 0, le = 23)
    lighthouroff:int = Field(ge = 0, le = 23)


