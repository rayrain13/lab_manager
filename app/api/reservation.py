from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.auth import get_current_user, require_reviewer
from app.models.user import User
from app.schemas.reservation import ReservationCreate, ReviewRequest
from app.services import reservation_service
from app.utils.response import success

router = APIRouter(prefix='/reservation', tags=['预约管理'])


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
    return success(reservation_service.list_reservations(db, current_user, page, page_size, status, lab_id))


@router.post('')
def create_reservation(
    data: ReservationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """学生发起预约"""
    return success(reservation_service.create_reservation(db, current_user, data), '预约提交成功，等待审核')


@router.post('/{reservation_id}/cancel')
def cancel_reservation(
    reservation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """本人取消预约"""
    reservation_service.cancel_reservation(db, current_user, reservation_id)
    return success(message='取消成功')


@router.post('/{reservation_id}/approve')
def approve_reservation(
    reservation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_reviewer),
):
    """审核通过"""
    reservation_service.approve_reservation(db, current_user, reservation_id)
    return success(message='已通过')


@router.post('/{reservation_id}/reject')
def reject_reservation(
    reservation_id: int,
    data: ReviewRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_reviewer),
):
    """审核驳回"""
    reservation_service.reject_reservation(db, current_user, reservation_id, data.review_comment)
    return success(message='已驳回')
