from pydantic import BaseModel, ConfigDict


class LoginResponse(BaseModel):
    id: int
    username: str
    name: str
    role: str
    email: str | None = None
    phone: str | None = None

    model_config = ConfigDict(from_attributes=True)


class UserOut(BaseModel):
    id: int
    username: str
    name: str
    role: str
    email: str | None = None
    phone: str | None = None

    model_config = ConfigDict(from_attributes=True)


class UserSelfUpdate(BaseModel):
    name: str | None = None
    email: str | None = None
    phone: str | None = None
    password: str | None = None


class UserCreate(BaseModel):
    username: str
    password: str
    name: str
    role: str = 'student'
    email: str | None = None
    phone: str | None = None


class UserUpdate(BaseModel):
    name: str | None = None
    role: str | None = None
    email: str | None = None
    phone: str | None = None
    password: str | None = None
