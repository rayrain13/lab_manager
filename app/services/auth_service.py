from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import LoginResponse
from app.services import ServiceError
from app.utils.jwt import create_access_token
from app.utils.security import hash_password, verify_password


def login(db: Session, username: str, password: str) -> dict:
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.password):
        raise ServiceError('账号或密码错误')

    return {
        'token': create_access_token(user.id),
        'user': LoginResponse.model_validate(user).model_dump()
    }


def register(db: Session, username: str, password: str, name: str, email: str | None, phone: str | None) -> None:
    if db.query(User).filter(User.username == username).first():
        raise ServiceError('用户名已存在')

    user = User(
        username=username,
        password=hash_password(password),
        name=name,
        role='student',
        email=email,
        phone=phone
    )
    db.add(user)
    db.commit()
