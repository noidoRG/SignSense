# models/database.py
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()
engine = create_engine('sqlite:///gestures.db')
Session = sessionmaker(bind=engine)
session = Session()

class Gesture(Base):
    __tablename__ = 'gestures'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

class Landmark(Base):
    __tablename__ = 'landmarks'
    id = Column(Integer, primary_key=True)
    gesture_id = Column(Integer, ForeignKey('gestures.id'))
    index = Column(Integer, nullable=False)
    x = Column(Float, nullable=False)
    y = Column(Float, nullable=False)

    gesture = relationship('Gesture', back_populates='landmarks')

Gesture.landmarks = relationship('Landmark', order_by=Landmark.index, back_populates='gesture')

Base.metadata.create_all(engine)
