import strawberry

@strawberry.type
class User: 
    id: int
    username: str
    password: str

@strawberry.type
class AuthPayload:
    user: User
    access_token: str

    