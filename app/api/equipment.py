from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.auth import get_current_user, require_admin
from app.models.user import User
from app.models.lab import Lab
from app.models.equipment import Equipment
from app.schemas.equipment import EquipmentCreate, EquipmentUpdate
from app.utils.response import success, error

router = APIRouter(prefix='/equipment', tags=['设备管理'])


def _to_out(e: Equipment, lab_name: str | None = None) -> dict:
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


@router.get('/list')
def list_equipments(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    keyword: str | None = Query(None),
    lab_id: int | None = Query(None),
    status: str | None = Query(None),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    """设备列表"""
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

    return success({
        'total': total,
        'items': [_to_out(e, lab_map.get(e.lab_id)) for e in items]
    })


@router.get('/{equipment_id}')
def get_equipment(equipment_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    """设备详情"""
    equipment = db.query(Equipment).filter(Equipment.id == equipment_id).first()
    if not equipment:
        return error('设备不存在')
    lab = db.query(Lab).filter(Lab.id == equipment.lab_id).first()
    return success(_to_out(equipment, lab.name if lab else None))


@router.post('')
def create_equipment(data: EquipmentCreate, db: Session = Depends(get_db), _: User = Depends(require_admin)):
    """新增设备（管理员）"""
    if db.query(Equipment).filter(Equipment.code == data.code).first():
        return error('设备编号已存在')

    equipment = Equipment(**data.model_dump())
    db.add(equipment)
    db.commit()
    db.refresh(equipment)

    lab = db.query(Lab).filter(Lab.id == equipment.lab_id).first()
    return success(_to_out(equipment, lab.name if lab else None), '新增成功')


@router.put('/{equipment_id}')
def update_equipment(equipment_id: int, data: EquipmentUpdate, db: Session = Depends(get_db), _: User = Depends(require_admin)):
    """修改设备（管理员）"""
    equipment = db.query(Equipment).filter(Equipment.id == equipment_id).first()
    if not equipment:
        return error('设备不存在')

    if data.code and data.code != equipment.code and db.query(Equipment).filter(Equipment.code == data.code).first():
        return error('设备编号已存在')

    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(equipment, field, value)

    db.commit()
    db.refresh(equipment)

    lab = db.query(Lab).filter(Lab.id == equipment.lab_id).first()
    return success(_to_out(equipment, lab.name if lab else None), '修改成功')


@router.delete('/{equipment_id}')
def delete_equipment(equipment_id: int, db: Session = Depends(get_db), _: User = Depends(require_admin)):
    """删除设备（管理员）"""
    equipment = db.query(Equipment).filter(Equipment.id == equipment_id).first()
    if not equipment:
        return error('设备不存在')

    db.delete(equipment)
    db.commit()
    return success(message='删除成功')
