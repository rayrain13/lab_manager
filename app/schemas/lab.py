from pydantic import BaseModel, ConfigDict


class LabCreate(BaseModel):
    name: str
    code: str
    location: str
    capacity: int = 0
    description: str | None = None
    status: str = 'available'


class LabUpdate(BaseModel):
    name: str | None = None
    code: str | None = None
    location: str | None = None
    capacity: int | None = None
    description: str | None = None
    status: str | None = None


class LabOut(BaseModel):
    id: int
    name: str
    code: str
    location: str
    capacity: int
    description: str | None = None
    status: str

    model_config = ConfigDict(from_attributes=True)
