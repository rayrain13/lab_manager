from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.auth import get_current_user, require_admin
from app.models.user import User
from app.schemas.equipment import EquipmentCreate, EquipmentUpdate
from app.services import equipment_service
from app.utils.response import success

router = APIRouter(prefix='/equipment', tags=['设备管理'])


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
    return success(equipment_service.list_equipments(db, page, page_size, keyword, lab_id, status))


@router.get('/{equipment_id}')
def get_equipment(equipment_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    """设备详情"""
    return success(equipment_service.get_equipment(db, equipment_id))


@router.post('')
def create_equipment(data: EquipmentCreate, db: Session = Depends(get_db), _: User = Depends(require_admin)):
    """新增设备（管理员）"""
    return success(equipment_service.create_equipment(db, data), '新增成功')


@router.put('/{equipment_id}')
def update_equipment(equipment_id: int, data: EquipmentUpdate, db: Session = Depends(get_db), _: User = Depends(require_admin)):
    """修改设备（管理员）"""
    return success(equipment_service.update_equipment(db, equipment_id, data), '修改成功')


@router.delete('/{equipment_id}')
def delete_equipment(equipment_id: int, db: Session = Depends(get_db), _: User = Depends(require_admin)):
    """删除设备（管理员）"""
    equipment_service.delete_equipment(db, equipment_id)
    return success(message='删除成功')
