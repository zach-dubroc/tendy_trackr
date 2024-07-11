# api/query.py
import strawberry
from typing import List
from fastapi import Depends
from sqlalchemy.orm import Session
from api.types.student import Student
from api.models import StudentModel
from api.database import get_db, DatabaseSession

@strawberry.type
class Query:
    @strawberry.field
    def students(self) -> List[Student]:
        with get_db() as db:  # Using the context manager
            students = db.query(StudentModel).all()
            return [
                Student(
                    fname=student.fname,
                    lname=student.lname,
                    absences=student.absences,
                    tardy=student.tardy,
                    nocalls=student.nocalls,
                    currentStatus=student.currentStatus,
                    datesMissed=student.datesMissed  # Directly use the JSON array
                ) for student in students
            ]
