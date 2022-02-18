#schemas helps to serailize and also convert mongodb format json to our UI needed json

def sensorDataEntity(db_item) -> dict:
    return {
        "id": str(db_item["_id"]),
        "ph": db_item["ant_ph"],
        "ec": db_item["ant_ec"],

    }

def listOfSensorDataEntity(db_item_list) -> list:
    list_sens_entity = []
    for item in db_item_list:
        list_sens_entity.append(sensorDataEntity(item))

    return list_sens_entity
