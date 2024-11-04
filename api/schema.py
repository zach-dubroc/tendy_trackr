# api/schema.py
import strawberry
from api.mutations import Mutation
from api.query import Query
schema = strawberry.Schema(query=Query, mutation=Mutation)
