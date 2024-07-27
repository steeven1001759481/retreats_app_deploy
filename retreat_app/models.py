from django.db import models
from django.db.models import UniqueConstraint
from sqlalchemy import create_engine, Column, Integer, String, Float, Date, ARRAY
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Create your models here.
engine = create_engine('postgresql://postgres:steevP152088@localhost/retreatDB')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

class Retreats(Base):
    __tablename__ = 'Retreats'
    title = Column('title', String)
    description = Column('description',String, nullable=True)
    date = Column('date',Integer, nullable=True)
    location = Column('location',String)
    price = Column('price',Float)
    retype = Column('retype',String)
    condition = Column('condition',String)
    image = Column('image',String)
    tag = Column('tag',String)
    duration = Column('duration',Integer)
    id = Column('id',String, primary_key=True)

class Bookings(Base):
    __tablename__ = 'Bookings'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    user_name = Column(String)
    user_email = Column(String)
    user_phone = Column(String, nullable=True)
    retreat_id = Column(Integer)
    retreat_title = Column(String)
    retreat_location = Column(String)
    retreat_price = Column(String)
    retreat_duration = Column(Integer)
    payment_details = Column(String, nullable=True)
    booking_date = Column(Integer)


Base.metadata.create_all(engine)