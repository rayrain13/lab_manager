from pydantic import BaseModel, ConfigDict


class EquipmentCreate(BaseModel):
    name: str
    code: str
    model: str | None = None
    lab_id: int
    status: str = 'available'
    description: str | None = None


class EquipmentUpdate(BaseModel):
    name: str | None = None
    code: str | None = None
    model: str | None = None
    lab_id: int | None = None
    status: str | None = None
    description: str | None = None


class EquipmentOut(BaseModel):
    id: int
    name: str
    code: str
    model: str | None = None
    lab_id: int
    status: str
    description: str | None = None
    lab_name: str | None = None

    model_config = ConfigDict(from_attributes=True)
