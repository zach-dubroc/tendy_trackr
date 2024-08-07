#api/auth.py
#not used yet, re-factor after login page
#will wrap /api endpoint in /protected
import os 
import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from .models import User
from pydantic import BaseModel, EmailStr, Field

load_dotenv()
print(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=3)

class UserAuthenticate(BaseModel):
    username: str
    password: str

#auth functions
def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_user(db: Session, user_data: UserCreate):
    hashed_password = get_password_hash(user_data.password)
    db_user = User(username = user_data.username, email=user_data.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, auth_data: UserAuthenticate):
    user = db.query(User).filter(User.username == auth_data.username).first()
    if not user: 
        return False
    if not verify_password(auth_data.password, user.hashed_password):
        return False
    return user
