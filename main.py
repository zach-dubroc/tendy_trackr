# main.py
from fastapi import FastAPI, Depends
from strawberry.fastapi import GraphQLRouter
from api.schema import schema
from api.database import SessionLocal
from sqlalchemy.orm import Session

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

