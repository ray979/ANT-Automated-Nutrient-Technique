#import statements
from pydantic import BaseModel

class SensorData(BaseModel):
    ant_ph: float
    ant_ec: float