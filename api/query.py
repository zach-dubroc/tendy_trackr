#TODO 
#after db connection is made update mock resolver
import strawberry
import typing
from api.types.student import Student

#mock resolver
def get_students(self):
    return [
        Student(
        fname='pancho',
        lname='veldez',
        absences=0,
        tardy=0,
        nocalls=0,
        currentStatus=0,
        datesMissed=["1902-05-05", "2021-04-20"],
        ),
                
        Student(
        fname='flaco',
        lname='elron',
        absences=0,
        tardy=0,
        nocalls=0,
        currentStatus=0,
        datesMissed=["1902-05-05", "2021-04-20"],
        )
    ]

@strawberry.type
class Query:
    students: typing.List[Student] = strawberry.field(resolver=get_students)