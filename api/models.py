# api/models.py
from sqlalchemy import Column, Integer, String, JSON, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class StudentModel(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, index=True)
    fname = Column(String(255))
    lname = Column(String(255))
    absences = Column(Integer)
    tardy = Column(Integer)
    nocalls = Column(Integer)
    currentStatus = Column(Integer)
    datesMissed = Column(JSON)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, index=True)
    email = Column(String(255), unique=True, index=True)
    hashed_password = Column(String(255))
    is_active = Column(Boolean, default=True)

