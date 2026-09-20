from fastapi import APIRouter, Depends

from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.user import LoginResponse


router = APIRouter(prefix='/user',tags = ['用户信息'])

@router.get('/info')
def get_user_info(current_user:User= Depends(get_current_user)):
    """获取当前用户信息"""
    return {
        "code":200,
        "message":'请求成功',
        'data':LoginResponse.model_validate(current_user)
    }
