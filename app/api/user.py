from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.auth import get_current_user, require_admin
from app.models.user import User
from app.schemas.user import LoginResponse, UserSelfUpdate, UserCreate, UserUpdate
from app.services import user_service
from app.utils.response import success

router = APIRouter(prefix='/user', tags=['用户信息'])


@router.get('/info')
def get_user_info(current_user: User = Depends(get_current_user)):
    """获取当前用户信息"""
    return success(LoginResponse.model_validate(current_user))


@router.put('/info')
def update_user_info(data: UserSelfUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """修改当前用户个人信息"""
    return success(user_service.update_info(db, current_user, data), '修改成功')


@router.get('/list')
def list_users(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    keyword: str | None = Query(None),
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    """用户列表（管理员）"""
    return success(user_service.list_users(db, page, page_size, keyword))


@router.post('')
def create_user(data: UserCreate, db: Session = Depends(get_db), _: User = Depends(require_admin)):
    """新增用户（管理员）"""
    return success(user_service.create_user(db, data), '新增成功')


@router.put('/{user_id}')
def update_user(user_id: int, data: UserUpdate, db: Session = Depends(get_db), _: User = Depends(require_admin)):
    """修改用户（管理员）"""
    return success(user_service.update_user(db, user_id, data), '修改成功')


@router.delete('/{user_id}')
def delete_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(require_admin)):
    """删除用户（管理员）"""
    user_service.delete_user(db, user_id, current_user.id)
    return success(message='删除成功')
