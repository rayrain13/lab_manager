from curses.ascii import US

from fastapi import Depends, HTTPException,status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.utils.jwt import decode_access_token


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/auth/login')

def get_current_user(token:str = Depends(oauth2_scheme),db:Session = Depends(get_db))->User:
    """验证前端传的token是否合法"""
    try:
        payload = decode_access_token(token)
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='登录已失效，请重新登录')

    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='无效登录凭证')
    user_id = payload.get('user_id')
    user = db.query(User).filter(User.id == user_id).first()

    return user
