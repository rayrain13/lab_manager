from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.auth import LoginRequest, RegisterRequest
from app.services import auth_service
from app.utils.response import success

router = APIRouter(prefix='/auth', tags=['权限验证'])


@router.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    return success(auth_service.login(db, data.username, data.password), '登陆成功')


@router.post("/register")
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    auth_service.register(db, data.username, data.password, data.name, data.email, data.phone)
    return success(message='注册成功')
