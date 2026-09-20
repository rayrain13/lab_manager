from datetime import datetime

from sqlalchemy.orm import Session

from app.models.user import User
from app.models.lab import Lab
from app.models.reservation import Reservation
from app.schemas.reservation import ReservationCreate
from app.services import ServiceError


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


def list_reservations(db: Session, current_user: User, page: int, page_size: int, status: str | None, lab_id: int | None) -> dict:
    query = db.query(Reservation)
    if current_user.role == 'student':
        query = query.filter(Reservation.user_id == current_user.id)
    if status:
        query = query.filter(Reservation.status == status)
    if lab_id:
        query = query.filter(Reservation.lab_id == lab_id)

    total = query.count()
    items = query.order_by(Reservation.id.desc()).offset((page - 1) * page_size).limit(page_size).all()

    return {'total': total, 'items': _build_out_list(db, items)}


def create_reservation(db: Session, current_user: User, data: ReservationCreate) -> dict:
    if data.end_time <= data.start_time:
        raise ServiceError('结束时间必须晚于开始时间')

    lab = db.query(Lab).filter(Lab.id == data.lab_id).first()
    if not lab:
        raise ServiceError('实验室不存在')
    if lab.status != 'available':
        raise ServiceError('该实验室当前不可预约')

    conflicts = db.query(Reservation).filter(
        Reservation.lab_id == data.lab_id,
        Reservation.date == data.date,
        Reservation.status.in_(['pending', 'approved'])
    ).all()
    for c in conflicts:
        if data.start_time < c.end_time and data.end_time > c.start_time:
            raise ServiceError('该时段已被预约，请选择其他时间')

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

    return _to_out(reservation, current_user.name, lab)


def cancel_reservation(db: Session, current_user: User, reservation_id: int) -> None:
    reservation = db.query(Reservation).filter(Reservation.id == reservation_id).first()
    if not reservation:
        raise ServiceError('预约不存在')

    if reservation.user_id != current_user.id and current_user.role != 'admin':
        raise ServiceError('只能取消自己的预约')

    if reservation.status not in ('pending', 'approved'):
        raise ServiceError('当前状态不可取消')

    reservation.status = 'cancelled'
    db.commit()


def approve_reservation(db: Session, current_user: User, reservation_id: int) -> None:
    reservation = db.query(Reservation).filter(Reservation.id == reservation_id).first()
    if not reservation:
        raise ServiceError('预约不存在')

    if reservation.status != 'pending':
        raise ServiceError('当前状态不可审核')

    reservation.status = 'approved'
    reservation.reviewer_id = current_user.id
    reservation.review_time = datetime.now()
    db.commit()


def reject_reservation(db: Session, current_user: User, reservation_id: int, review_comment: str | None) -> None:
    reservation = db.query(Reservation).filter(Reservation.id == reservation_id).first()
    if not reservation:
        raise ServiceError('预约不存在')

    if reservation.status != 'pending':
        raise ServiceError('当前状态不可审核')

    reservation.status = 'rejected'
    reservation.reviewer_id = current_user.id
    reservation.review_time = datetime.now()
    reservation.review_comment = review_comment
    db.commit()
