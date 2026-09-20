from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.auth import get_current_user, require_admin
from app.models.user import User
from app.models.lab import Lab
from app.schemas.lab import LabCreate, LabUpdate, LabOut
from app.utils.response import success, error

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
    query = db.query(Lab)
    if keyword:
        query = query.filter((Lab.name.like(f'%{keyword}%')) | (Lab.code.like(f'%{keyword}%')))
    if status:
        query = query.filter(Lab.status == status)

    total = query.count()
    items = query.order_by(Lab.id.desc()).offset((page - 1) * page_size).limit(page_size).all()

    return success({
        'total': total,
        'items': [LabOut.model_validate(l) for l in items]
    })


@router.get('/{lab_id}')
def get_lab(lab_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    """实验室详情"""
    lab = db.query(Lab).filter(Lab.id == lab_id).first()
    if not lab:
        return error('实验室不存在')
    return success(LabOut.model_validate(lab))


@router.post('')
def create_lab(data: LabCreate, db: Session = Depends(get_db), _: User = Depends(require_admin)):
    """新增实验室（管理员）"""
    if db.query(Lab).filter(Lab.code == data.code).first():
        return error('实验室编号已存在')

    lab = Lab(**data.model_dump())
    db.add(lab)
    db.commit()
    db.refresh(lab)
    return success(LabOut.model_validate(lab), '新增成功')


@router.put('/{lab_id}')
def update_lab(lab_id: int, data: LabUpdate, db: Session = Depends(get_db), _: User = Depends(require_admin)):
    """修改实验室（管理员）"""
    lab = db.query(Lab).filter(Lab.id == lab_id).first()
    if not lab:
        return error('实验室不存在')

    if data.code and data.code != lab.code and db.query(Lab).filter(Lab.code == data.code).first():
        return error('实验室编号已存在')

    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(lab, field, value)

    db.commit()
    db.refresh(lab)
    return success(LabOut.model_validate(lab), '修改成功')


@router.delete('/{lab_id}')
def delete_lab(lab_id: int, db: Session = Depends(get_db), _: User = Depends(require_admin)):
    """删除实验室（管理员）"""
    lab = db.query(Lab).filter(Lab.id == lab_id).first()
    if not lab:
        return error('实验室不存在')

    db.delete(lab)
    db.commit()
    return success(message='删除成功')
