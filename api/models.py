#create student model 
#datesMissed field should be able to use sqlalchemy json type
#if not re-structure to two tables and join on student id
from sqlalchemy import Column, Integer, String, JSON
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

    

