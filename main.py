from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
from api.schema import schema

app = FastAPI()

graphql_app = GraphQLRouter(schema)

app.include_router(graphql_app, prefix="/graphql")

@app.get("/")
def read_root():
    return {"message": "hi, I am endpoint"}

