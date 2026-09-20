from pydantic import BaseModel,ConfigDict

class LoginResponse(BaseModel):
    id:int
    username:str
    name:str
    role:str
    email:str
    phone:str

    model_config = ConfigDict(from_attributes=True)