from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.auth import get_current_user, require_admin
from app.models.user import User
from app.schemas.lab import LabCreate, LabUpdate
from app.services import lab_service
from app.utils.response import success

router = APIRouter(prefix='/lab', tags=['实验室管理'])


@router.get('/list')
def list_labs(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    keyword: str | None = Query(None),
    status: str | None = Query(None),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    """实验室列表"""
    return success(lab_service.list_labs(db, page, page_size, keyword, status))


@router.get('/{lab_id}')
def get_lab(lab_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    """实验室详情"""
    return success(lab_service.get_lab(db, lab_id))


@router.post('')
def create_lab(data: LabCreate, db: Session = Depends(get_db), _: User = Depends(require_admin)):
    """新增实验室（管理员）"""
    return success(lab_service.create_lab(db, data), '新增成功')


@router.put('/{lab_id}')
def update_lab(lab_id: int, data: LabUpdate, db: Session = Depends(get_db), _: User = Depends(require_admin)):
    """修改实验室（管理员）"""
    return success(lab_service.update_lab(db, lab_id, data), '修改成功')


@router.delete('/{lab_id}')
def delete_lab(lab_id: int, db: Session = Depends(get_db), _: User = Depends(require_admin)):
    """删除实验室（管理员）"""
    lab_service.delete_lab(db, lab_id)
    return success(message='删除成功')
