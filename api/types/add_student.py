# api/types/add_student.py
import strawberry

@strawberry.input
class AddStudentInput:
        fname: str = strawberry.field(description="first name")
        lname: str = strawberry.field(description="last name")
        absences: int = strawberry.field(description="abensce count")
        tardy: int = strawberry.field(description="tardy count")
        nocalls: int = strawberry.field(description="no call count")
        currentStatus: int = strawberry.field(description="status")
        datesMissed: list[str] = strawberry.field(description="list of absence dates")