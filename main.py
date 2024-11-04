# main.py
# test query for postman @  https://tendytrackrbackend-production.up.railway.app/api
# {
#     "query": "{ students { fname lname datesMissed} }"
# }

# test mutation to add a student
# {
#   "query": "mutation { createStudent(input: { fname: \"Jimmy\", lname: \"Neutron\", absences: 0, tardy: 0, nocalls: 0, currentStatus: 1, datesMissed: [\"2024-01-01\", \"2024-01-15\", \"2024-02-01\"] }) { id fname lname absences tardy nocalls currentStatus datesMissed } }"
# }

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from strawberry.fastapi import GraphQLRouter
from api.auth import create_user, authenticate_user, create_access_token, UserCreate, UserAuthenticate
from api.schema import schema
from api.database import SessionLocal
from api.models import StudentModel
from sqlalchemy.orm import Session
import uvicorn
import os
from dotenv import load_dotenv

# grab .env 
load_dotenv()

ENV = os.getenv("ENV", "development")
PORT = int(os.getenv("PORT", 8000 if ENV == "development" else 80))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close

def get_context(db: Session = Depends(get_db)):
    return{"db": db}

app = FastAPI()
graphql_app = GraphQLRouter(schema, context_getter=get_context)

#graphql here
app.include_router(graphql_app, prefix="/api")

#middleware(CORS) Config
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Replace with your Next.js frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "hi, I am endpoint"}

@app.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    new_user = create_user(db, user)
    return {"id": new_user.id, "username": new_user.username, "email": new_user.email}

@app.post("/token")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    auth_data = UserAuthenticate(username=form_data.username, password=form_data.password)
    user = authenticate_user(db, auth_data)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type":"bearer"}

#placeholder
@app.get("/unprotected")
def unprotected():
    return {"hello": "world"}

#should just be able to wrap /api inside?
@app.get("/protected")
def protected(token: str = Depends(oauth2_scheme)):
    return {"message": "You are authenticated"}


#all students
@app.get("/stds")
def list_students(db: Session = Depends(get_db)):
    students = db.query(StudentModel).all()
    return [{"id": student.id, "fname": student.fname, "lname": student.lname, 
             "absences": student.absences, "tardy": student.tardy,
             "nocalls": student.nocalls, "currentStatus": student.currentStatus,
             "datesMissed": student.datesMissed} for student in students]

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=PORT)

