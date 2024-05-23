from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()

class Gesture(Base):
    __tablename__ = 'gestures'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String, nullable=True)

    frames = relationship('GestureFrame', back_populates='gesture')

class GestureFrame(Base):
    __tablename__ = 'gesture_frames'
    id = Column(Integer, primary_key=True)
    gesture_id = Column(Integer, ForeignKey('gestures.id'))
    frame_number = Column(Integer)
    timestamp = Column(Float, nullable=True)

    gesture = relationship('Gesture', back_populates='frames')
    landmarks = relationship('Landmark', back_populates='gesture_frame')

class Landmark(Base):
    __tablename__ = 'landmarks'
    id = Column(Integer, primary_key=True)
    gesture_frame_id = Column(Integer, ForeignKey('gesture_frames.id'))
    index = Column(Integer)
    x = Column(Float)
    y = Column(Float)
    z = Column(Float, nullable=True)

    gesture_frame = relationship('GestureFrame', back_populates='landmarks')

engine = create_engine('sqlite:///gestures.db')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
