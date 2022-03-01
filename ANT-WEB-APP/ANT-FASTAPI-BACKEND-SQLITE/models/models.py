#import statements
import sqlalchemy as _sql
import sqlalchemy.orm as _orm
import datetime as _dt
from config.database import Base

#database model for sensor data
class SensorData(Base):
    __tablename__ = "sensor_reading"
    id = _sql.Column(_sql.Integer, primary_key=True, index=True) #id will be index of row added
    ph_reading = _sql.Column(_sql.Float)
    ec_reading = _sql.Column(_sql.Float)
    date_posted =  _sql.Column(_sql.Date, default=_dt.date.today) #database will automatically create and save the date row added
    datetime_posted = _sql.Column(_sql.DateTime, default=_dt.datetime.now) #database will automatically save the datetime added
