# main.py
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from strawberry.fastapi import GraphQLRouter
from api.auth import create_user, authenticate_user, create_access_token
from api.schema import schema
from api.database import SessionLocal
from sqlalchemy.orm import Session

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

app.include_router(graphql_app, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "hi, I am endpoint"}

@app.post("/register")
def register(username: str, email: str, password: str, db: Session = Depends(get_db)):
    user = create_user(db, username, email, password)
    return {"id": user.id, "username": user.username, "email": user.email}

@app.post("/token")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type":"bearer"}


@app.get("/unprotected")
def unprotected():
    return {"hello": "world"}

@app.get("/protected")
def protected(token: str = Depends(oauth2_scheme)):
    return {"message": "You are authenticated"}


