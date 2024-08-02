# api/mutations.py
import strawberry
from sqlalchemy.orm import Session
from api.types.student import Student
from api.types.user import User, AuthPayload
from api.types.add_student import AddStudentInput
from api.models import StudentModel
from api.auth import create_user, authenticate_user, create_access_token


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
    
@strawberry.type
class AuthMutation:
    @strawberry.mutation
    def register(self, username: str, email: str, password: str, info: strawberry.types.Info)-> User:
        db: Session = info.context["db"]
        user = create_user(db, username, email, password)
        access_token = create_access_token(data={"sub": user.username})
        return {"access_token": access_token, "token_type": "bearer"}
    
    @strawberry.mutation
    def login(self, username: str, password: str, info: strawberry.types.Info) -> AuthPayload:
        db: Session = info.context["db"]
        user = authenticate_user(db, username, password)
        if not user:
            raise Exception("Invalied creds bruh")
        access_token = create_access_token(data={"sub": user.username})
        return AuthPayload(user=User(id=user.id, username = user.username, email=user.email), access_token=access_token)