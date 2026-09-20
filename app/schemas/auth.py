from pydantic import BaseModel

class LoginRequest(BaseModel):
    username:str
    password:str


class RegisterRequest(BaseModel):
    username: str
    password: str
    name: str
    role: str = "user"
    email: str
    phone: str