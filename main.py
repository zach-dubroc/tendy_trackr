# main.py
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from strawberry.fastapi import GraphQLRouter
from api.auth import create_user, authenticate_user, create_access_token, UserCreate, UserAuthenticate
from api.schema import schema
from api.database import SessionLocal
from sqlalchemy.orm import Session
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
# update .env again
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


