from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserOut, UserSelfUpdate, UserCreate, UserUpdate
from app.services import ServiceError
from app.utils.security import hash_password


def _dump(user: User) -> dict:
    return UserOut.model_validate(user).model_dump()


def update_info(db: Session, current_user: User, data: UserSelfUpdate) -> dict:
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
    return _dump(current_user)


def list_users(db: Session, page: int, page_size: int, keyword: str | None) -> dict:
    query = db.query(User)
    if keyword:
        query = query.filter((User.username.like(f'%{keyword}%')) | (User.name.like(f'%{keyword}%')))

    total = query.count()
    items = query.order_by(User.id.desc()).offset((page - 1) * page_size).limit(page_size).all()

    return {'total': total, 'items': [_dump(u) for u in items]}


def create_user(db: Session, data: UserCreate) -> dict:
    if db.query(User).filter(User.username == data.username).first():
        raise ServiceError('用户名已存在')

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
    return _dump(user)


def update_user(db: Session, user_id: int, data: UserUpdate) -> dict:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise ServiceError('用户不存在')

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
    return _dump(user)


def delete_user(db: Session, user_id: int, current_user_id: int) -> None:
    if user_id == current_user_id:
        raise ServiceError('不能删除当前登录账号')

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise ServiceError('用户不存在')

    db.delete(user)
    db.commit()
