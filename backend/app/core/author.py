from JWT import  verify_token
from fastapi import Depends ,  HTTPException 
from sqlalchemy.ext.asyncio import AsyncSession
from JWT import verify_access_token, verify_refresh_token 
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.sql import select
from app.models.Users import User
from jose import jwt, JWTError, ExpiredSignatureError
from app.db.DataBase import get_async_session
from .auth import get_current_user

def is_admin(user : User) ->bool:
    """
    Kiểm tra người dùng có phải là admin hay không
    """
    user_roles = [role.name for role in user.roles]
    return User.RoleEnum.ADMIN in user_roles
def is_user(user : User) ->bool:
    """
    Kiểm tra người dùng có phải là user hay không
    """
    user_roles = [role.name for role in user.roles]
    return User.RoleEnum.USER in user_roles
def has_role(user: User, role: User.RoleEnum) -> bool:
    """
    Kiểm tra người dùng có vai trò cụ thể hay không
    """
    user_roles = [r.name for r in user.roles]
    return role in user_roles
def has_any_role(user: User, roles: list[User.RoleEnum]) -> bool:
    """
    Kiểm tra người dùng có bất kỳ vai trò nào trong danh sách roles hay không
    """
    user_roles = [r.name for r in user.roles]
    return any(role in user_roles for role in roles)

async def require_admin_role(user: User = Depends(get_current_user)):
    user_roles = [role.name for role in user.roles]
    if User.RoleEnum.ADMIN not in user_roles:
        raise HTTPException(status_code=403, detail="You do not have permission to perform this action")

    return user  # Trả về người dùng nếu có quyền admin
     