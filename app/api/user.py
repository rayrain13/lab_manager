from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.auth import get_current_user, require_admin
from app.models.user import User
from app.schemas.user import LoginResponse, UserOut, UserSelfUpdate, UserCreate, UserUpdate
from app.utils.security import hash_password
from app.utils.response import success, error

router = APIRouter(prefix='/user', tags=['用户信息'])


@router.get('/info')
def get_user_info(current_user: User = Depends(get_current_user)):
    """获取当前用户信息"""
    return success(LoginResponse.model_validate(current_user))


@router.put('/info')
def update_user_info(data: UserSelfUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """修改当前用户个人信息"""
    if data.name is not None:
        current_user.name = data.name
    if data.email is not None:
        current_user.email = data.email
    if data.phone is not None:
        current_user.phone = data.phone
    if data.password:
        current_user.password = hash_password(data.password)

    db.commit()
    db.refresh(current_user)
    return success(LoginResponse.model_validate(current_user), '修改成功')


@router.get('/list')
def list_users(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    keyword: str | None = Query(None),
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    """用户列表（管理员）"""
    query = db.query(User)
    if keyword:
        query = query.filter((User.username.like(f'%{keyword}%')) | (User.name.like(f'%{keyword}%')))

    total = query.count()
    items = query.order_by(User.id.desc()).offset((page - 1) * page_size).limit(page_size).all()

    return success({
        'total': total,
        'items': [UserOut.model_validate(u) for u in items]
    })


@router.post('')
def create_user(data: UserCreate, db: Session = Depends(get_db), _: User = Depends(require_admin)):
    """新增用户（管理员）"""
    user = db.query(User).filter(User.username == data.username).first()
    if user:
        return error('用户名已存在')

    user = User(
        username=data.username,
        password=hash_password(data.password),
        name=data.name,
        role=data.role,
        email=data.email,
        phone=data.phone
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return success(UserOut.model_validate(user), '新增成功')


@router.put('/{user_id}')
def update_user(user_id: int, data: UserUpdate, db: Session = Depends(get_db), _: User = Depends(require_admin)):
    """修改用户（管理员）"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return error('用户不存在')

    if data.name is not None:
        user.name = data.name
    if data.role is not None:
        user.role = data.role
    if data.email is not None:
        user.email = data.email
    if data.phone is not None:
        user.phone = data.phone
    if data.password:
        user.password = hash_password(data.password)

    db.commit()
    db.refresh(user)
    return success(UserOut.model_validate(user), '修改成功')


@router.delete('/{user_id}')
def delete_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(require_admin)):
    """删除用户（管理员）"""
    if user_id == current_user.id:
        return error('不能删除当前登录账号')

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return error('用户不存在')

    db.delete(user)
    db.commit()
    return success(message='删除成功')
