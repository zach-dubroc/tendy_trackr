import strawberry
from api.query import Query


schema = strawberry.Schema(query=Query)
