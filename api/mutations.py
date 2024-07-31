# api/mutations.py
import strawberry
from sqlalchemy.orm import Session
from api.types.student import Student
from api.types.add_student import AddStudentInput
from api.models import StudentModel


@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_student(self, input: AddStudentInput, info: strawberry.types.Info) -> Student:
        db: Session = info.context["db"]
        student = StudentModel(
            fname=input.fname,
            lname=input.lname,
            absences=input.absences,
            tardy=input.tardy,
            nocalls=input.nocalls,
            currentStatus=input.currentStatus,
            datesMissed=input.datesMissed
        )
        try:
            db.add(student)
            db.commit()
            db.refresh(student)
        except Exception as e:
            raise Exception(f"Database error: {str(e)}")
        return Student(
            id=student.id,
            fname=student.fname,
            lname=student.lname,
            absences=student.absences,
            tardy=student.tardy,
            nocalls=student.nocalls,
            currentStatus=student.currentStatus,
            datesMissed=student.datesMissed
        )
    @strawberry.mutation
    def delete_student(self, id:int, info: strawberry.types.Info) -> str:
        db: Session = info.context["db"]
        student = db.query(StudentModel).filter(StudentModel.id == id).first()
        if not student:
            raise Exception("not found")
        try:
            db.delete(student)
            db.commit()
        except Exception as e:
            raise Exception(f"database error: {str(e)}")
        return f"student id#{id}: {student.fname} {student.lname} has been deleted"