# schema.py
import strawberry
from api.mutations import Mutation


from api.query import Query
from api.mutations import Mutation
schema = strawberry.Schema(query=Query, mutation=Mutation)
