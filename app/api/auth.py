from fastapi import APIRouter, Depends
from app.schemas.auth import LoginRequest, RegisterRequest
from app.schemas.user import LoginResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.utils.jwt import create_access_token
from app.utils.security import hash_password, verify_password
from app.utils.response import success, error

router = APIRouter(prefix='/auth', tags=['权限验证'])


@router.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == data.username).first()

    if not user or not verify_password(data.password, user.password):
        return error('账号或密码错误')

    # 创建token
    token = create_access_token(user.id)

    return success({
        'token': token,
        'user': LoginResponse.model_validate(user)
    }, '登陆成功')


@router.post("/register")
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    # 1. 检查用户名是否已经存在
    user = db.query(User).filter(User.username == data.username).first()

    if user:
        return error('用户名已存在')

    # 2. 创建用户（公开注册固定为学生角色）
    user = User(
        username=data.username,
        password=hash_password(data.password),
        name=data.name,
        role='student',
        email=data.email,
        phone=data.phone
    )

    # 3. 保存到数据库
    db.add(user)
    db.commit()
    db.refresh(user)

    return success(message='注册成功')
