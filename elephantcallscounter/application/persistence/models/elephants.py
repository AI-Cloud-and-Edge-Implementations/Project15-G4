from elephantcallscounter.app_factory import db

from sqlalchemy import Column, DateTime, Integer, Float, Text


class Elephants(db.Model):
    __tablename__ = 'elephants'

    id = Column(Integer, primary_key = True, autoincrement = True)
    latitude = Column(Float, default=0.0)
    longitude = Column(Float, default=0.0)
    start_time = Column(DateTime)
    end_time = Column(DateTime, default=0)
    device_id = Column(Text, nullable = False)
    number_of_elephants = Column(Integer, default=0)


def delete_all_elephants():
    print('Deleting all elephant data')
    db.session.query(Elephants).delete()
    db.session.commit()
