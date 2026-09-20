from sqlalchemy.orm import Session

from app.models.lab import Lab
from app.models.equipment import Equipment
from app.schemas.equipment import EquipmentCreate, EquipmentUpdate
from app.services import ServiceError


def _dump(e: Equipment, lab_name: str | None = None) -> dict:
    return {
        'id': e.id,
        'name': e.name,
        'code': e.code,
        'model': e.model,
        'lab_id': e.lab_id,
        'status': e.status,
        'description': e.description,
        'lab_name': lab_name,
    }


def _lab_name(db: Session, lab_id: int) -> str | None:
    lab = db.query(Lab).filter(Lab.id == lab_id).first()
    return lab.name if lab else None


def list_equipments(db: Session, page: int, page_size: int, keyword: str | None, lab_id: int | None, status: str | None) -> dict:
    query = db.query(Equipment)
    if keyword:
        query = query.filter((Equipment.name.like(f'%{keyword}%')) | (Equipment.code.like(f'%{keyword}%')))
    if lab_id:
        query = query.filter(Equipment.lab_id == lab_id)
    if status:
        query = query.filter(Equipment.status == status)

    total = query.count()
    items = query.order_by(Equipment.id.desc()).offset((page - 1) * page_size).limit(page_size).all()

    lab_map = {l.id: l.name for l in db.query(Lab).all()}

    return {'total': total, 'items': [_dump(e, lab_map.get(e.lab_id)) for e in items]}


def get_equipment(db: Session, equipment_id: int) -> dict:
    equipment = db.query(Equipment).filter(Equipment.id == equipment_id).first()
    if not equipment:
        raise ServiceError('设备不存在')
    return _dump(equipment, _lab_name(db, equipment.lab_id))


def create_equipment(db: Session, data: EquipmentCreate) -> dict:
    if db.query(Equipment).filter(Equipment.code == data.code).first():
        raise ServiceError('设备编号已存在')

    equipment = Equipment(**data.model_dump())
    db.add(equipment)
    db.commit()
    db.refresh(equipment)
    return _dump(equipment, _lab_name(db, equipment.lab_id))


def update_equipment(db: Session, equipment_id: int, data: EquipmentUpdate) -> dict:
    equipment = db.query(Equipment).filter(Equipment.id == equipment_id).first()
    if not equipment:
        raise ServiceError('设备不存在')

    if data.code and data.code != equipment.code and db.query(Equipment).filter(Equipment.code == data.code).first():
        raise ServiceError('设备编号已存在')

    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(equipment, field, value)

    db.commit()
    db.refresh(equipment)
    return _dump(equipment, _lab_name(db, equipment.lab_id))


def delete_equipment(db: Session, equipment_id: int) -> None:
    equipment = db.query(Equipment).filter(Equipment.id == equipment_id).first()
    if not equipment:
        raise ServiceError('设备不存在')

    db.delete(equipment)
    db.commit()
