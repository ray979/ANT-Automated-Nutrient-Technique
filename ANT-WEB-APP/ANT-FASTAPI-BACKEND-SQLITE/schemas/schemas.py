#schemas helps to serailize and also convert sqlite format json to our UI needed json

from pydantic import BaseModel, Field
import datetime

def sensorDataEntity(db_item) -> dict:
    return {
        "id": db_item.id,
        "ph": db_item.ph_reading,
        "ec": db_item.ec_reading,
        "date_posted": db_item.date_posted,
        "time_posted": db_item.datetime_posted.strftime('%H:%M:%S'),
        "datetime_posted":db_item.datetime_posted

    }

def listOfSensorDataEntity(db_item_list) -> list:
    list_sens_entity = []
    for item in db_item_list:
        list_sens_entity.append(sensorDataEntity(item))

    return list_sens_entity

class SensorData(BaseModel):
    ph: float = Field(ge = 0, le = 14)
    ec: float

class SensorDataCreate(SensorData):
    pass

class Settings(BaseModel):
    phmin:float = Field(ge = 0)
    phmax:float = Field(le = 14)
    ecmin:float = Field(ge = 0)
    lighthouron:int = Field(ge = 0, le = 23)
    lighthouroff:int = Field(ge = 0, le = 23)


