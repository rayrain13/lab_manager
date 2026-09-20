from datetime import datetime

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.auth import get_current_user, require_reviewer
from app.models.user import User
from app.models.lab import Lab
from app.models.reservation import Reservation
from app.schemas.reservation import ReservationCreate, ReviewRequest
from app.utils.response import success, error

router = APIRouter(prefix='/reservation', tags=['预约管理'])


def _to_out(r: Reservation, user_name: str | None = None, lab: Lab | None = None, reviewer_name: str | None = None) -> dict:
    return {
        'id': r.id,
        'user_id': r.user_id,
        'lab_id': r.lab_id,
        'date': r.date.isoformat() if r.date else None,
        'start_time': r.start_time.strftime('%H:%M') if r.start_time else None,
        'end_time': r.end_time.strftime('%H:%M') if r.end_time else None,
        'purpose': r.purpose,
        'status': r.status,
        'review_comment': r.review_comment,
        'reviewer_id': r.reviewer_id,
        'review_time': r.review_time.isoformat() if r.review_time else None,
        'user_name': user_name,
        'lab_name': lab.name if lab else None,
        'lab_location': lab.location if lab else None,
        'reviewer_name': reviewer_name,
    }


def _build_out_list(db: Session, reservations: list[Reservation]) -> list[dict]:
    user_ids = {r.user_id for r in reservations} | {r.reviewer_id for r in reservations if r.reviewer_id}
    lab_ids = {r.lab_id for r in reservations}
    user_map = {u.id: u for u in db.query(User).filter(User.id.in_(user_ids)).all()} if user_ids else {}
    lab_map = {l.id: l for l in db.query(Lab).filter(Lab.id.in_(lab_ids)).all()} if lab_ids else {}

    result = []
    for r in reservations:
        user = user_map.get(r.user_id)
        reviewer = user_map.get(r.reviewer_id) if r.reviewer_id else None
        lab = lab_map.get(r.lab_id)
        result.append(_to_out(r, user.name if user else None, lab, reviewer.name if reviewer else None))
    return result


@router.get('/list')
def list_reservations(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    status: str | None = Query(None),
    lab_id: int | None = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """预约列表：学生查看自己的，管理员/教师查看全部"""
    query = db.query(Reservation)
    if current_user.role == 'student':
        query = query.filter(Reservation.user_id == current_user.id)
    if status:
        query = query.filter(Reservation.status == status)
    if lab_id:
        query = query.filter(Reservation.lab_id == lab_id)

    total = query.count()
    items = query.order_by(Reservation.id.desc()).offset((page - 1) * page_size).limit(page_size).all()

    return success({
        'total': total,
        'items': _build_out_list(db, items)
    })


@router.post('')
def create_reservation(
    data: ReservationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """学生发起预约"""
    if data.end_time <= data.start_time:
        return error('结束时间必须晚于开始时间')

    lab = db.query(Lab).filter(Lab.id == data.lab_id).first()
    if not lab:
        return error('实验室不存在')
    if lab.status != 'available':
        return error('该实验室当前不可预约')

    # 冲突校验：同一实验室、同一日期、待审核/已通过且时间段重叠
    conflicts = db.query(Reservation).filter(
        Reservation.lab_id == data.lab_id,
        Reservation.date == data.date,
        Reservation.status.in_(['pending', 'approved'])
    ).all()
    for c in conflicts:
        if data.start_time < c.end_time and data.end_time > c.start_time:
            return error('该时段已被预约，请选择其他时间')

    reservation = Reservation(
        user_id=current_user.id,
        lab_id=data.lab_id,
        date=data.date,
        start_time=data.start_time,
        end_time=data.end_time,
        purpose=data.purpose,
        status='pending'
    )
    db.add(reservation)
    db.commit()
    db.refresh(reservation)

    return success(_to_out(reservation, current_user.name, lab), '预约提交成功，等待审核')


@router.post('/{reservation_id}/cancel')
def cancel_reservation(
    reservation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """本人取消预约"""
    reservation = db.query(Reservation).filter(Reservation.id == reservation_id).first()
    if not reservation:
        return error('预约不存在')

    if reservation.user_id != current_user.id and current_user.role not in ('admin',):
        return error('只能取消自己的预约')

    if reservation.status not in ('pending', 'approved'):
        return error('当前状态不可取消')

    reservation.status = 'cancelled'
    db.commit()
    return success(message='取消成功')


@router.post('/{reservation_id}/approve')
def approve_reservation(
    reservation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_reviewer),
):
    """审核通过"""
    reservation = db.query(Reservation).filter(Reservation.id == reservation_id).first()
    if not reservation:
        return error('预约不存在')

    if reservation.status != 'pending':
        return error('当前状态不可审核')

    reservation.status = 'approved'
    reservation.reviewer_id = current_user.id
    reservation.review_time = datetime.now()
    db.commit()
    return success(message='已通过')


@router.post('/{reservation_id}/reject')
def reject_reservation(
    reservation_id: int,
    data: ReviewRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_reviewer),
):
    """审核驳回"""
    reservation = db.query(Reservation).filter(Reservation.id == reservation_id).first()
    if not reservation:
        return error('预约不存在')

    if reservation.status != 'pending':
        return error('当前状态不可审核')

    reservation.status = 'rejected'
    reservation.reviewer_id = current_user.id
    reservation.review_time = datetime.now()
    reservation.review_comment = data.review_comment
    db.commit()
    return success(message='已驳回')
