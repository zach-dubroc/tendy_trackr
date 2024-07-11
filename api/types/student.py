import strawberry

@strawberry.type
class Student():
        fname: str
        lname: str
        absences: int
        tardy: int
        nocalls: int 
        currentStatus: int
        datesMissed: list[str]
        