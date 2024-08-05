# api/query.py
import strawberry
from typing import List
from api.types.student import Student
from api.models import StudentModel
from api.database import get_db


@strawberry.type
class Query:
    @strawberry.field
    def students(self) -> List[Student]:
        with get_db() as db:  # Using the context manager
            students = db.query(StudentModel).all()
            return [
                Student(
                    id=student.id,
                    fname=student.fname,
                    lname=student.lname,
                    absences=student.absences,
                    tardy=student.tardy,
                    nocalls=student.nocalls,
                    currentStatus=student.currentStatus,
                    datesMissed=student.datesMissed  # Directly use the JSON array
                ) for student in students
            ]
    @strawberry.field
    def student(self, id: int) -> Student:
        with get_db() as db:  # Using the context manager
            student = db.query(StudentModel).filter(StudentModel.id == id).first()
            if student:
                return Student(
                    id=student.id,
                    fname=student.fname,
                    lname=student.lname,
                    absences=student.absences,
                    tardy=student.tardy,
                    nocalls=student.nocalls,
                    currentStatus=student.currentStatus,
                    datesMissed=student.datesMissed  # Directly use the JSON array
                )
            return None

