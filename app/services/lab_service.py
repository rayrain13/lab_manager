from sqlalchemy.orm import Session

from app.models.lab import Lab
from app.schemas.lab import LabOut, LabCreate, LabUpdate
from app.services import ServiceError


def _dump(lab: Lab) -> dict:
    return LabOut.model_validate(lab).model_dump()


def list_labs(db: Session, page: int, page_size: int, keyword: str | None, status: str | None) -> dict:
    query = db.query(Lab)
    if keyword:
        query = query.filter((Lab.name.like(f'%{keyword}%')) | (Lab.code.like(f'%{keyword}%')))
    if status:
        query = query.filter(Lab.status == status)

    total = query.count()
    items = query.order_by(Lab.id.desc()).offset((page - 1) * page_size).limit(page_size).all()

    return {'total': total, 'items': [_dump(l) for l in items]}


def get_lab(db: Session, lab_id: int) -> dict:
    lab = db.query(Lab).filter(Lab.id == lab_id).first()
    if not lab:
        raise ServiceError('实验室不存在')
    return _dump(lab)


def create_lab(db: Session, data: LabCreate) -> dict:
    if db.query(Lab).filter(Lab.code == data.code).first():
        raise ServiceError('实验室编号已存在')

    lab = Lab(**data.model_dump())
    db.add(lab)
    db.commit()
    db.refresh(lab)
    return _dump(lab)


def update_lab(db: Session, lab_id: int, data: LabUpdate) -> dict:
    lab = db.query(Lab).filter(Lab.id == lab_id).first()
    if not lab:
        raise ServiceError('实验室不存在')

    if data.code and data.code != lab.code and db.query(Lab).filter(Lab.code == data.code).first():
        raise ServiceError('实验室编号已存在')

    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(lab, field, value)

    db.commit()
    db.refresh(lab)
    return _dump(lab)


def delete_lab(db: Session, lab_id: int) -> None:
    lab = db.query(Lab).filter(Lab.id == lab_id).first()
    if not lab:
        raise ServiceError('实验室不存在')

    db.delete(lab)
    db.commit()
