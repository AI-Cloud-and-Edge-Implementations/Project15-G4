from elephantcallscounter.app_factory import db

from sqlalchemy import Column, DateTime, Integer, Float


class Elephants(db.Model):
    __tablename__ = 'elephants'

    id = Column(Integer, primary_key = True)
    latitude = Column(Float, default=0.0)
    longitude = Column(Float, default=0.0)
    start_time = Column(DateTime)
    end_time = Column(DateTime, default=0)
    device_id = Column(Integer, nullable = False)
    number_of_elephants = Column(Integer, default=0)
