import sqlalchemy as _sql
import sqlalchemy.orm as _orm
import datetime as _dt

from config.database import Base

class SensorData(Base):
    __tablename__ = "sensor_reading"
    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    ph_reading = _sql.Column(_sql.Float)
    ec_reading = _sql.Column(_sql.Float)
    date_posted =  _sql.Column(_sql.Date, default=_dt.date.today)
    datetime_posted = _sql.Column(_sql.DateTime, default=_dt.datetime.now)