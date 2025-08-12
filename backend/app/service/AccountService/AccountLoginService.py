from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select
from sqlalchemy.orm import selectinload
from app.models.Users import StatusUserEnum, User
from app.schemas.AccountSchema.AccountLoginSchema import LoginUserSchema, LoginReponseSchema
from app.Utils.HashPassword import verify_password
from app.core.JWT import create_full_token

async def LoginAccountService(login_user: LoginUserSchema, db: AsyncSession):
    query = select(User).options(selectinload(User.roles)).where(User.accountname == login_user.accountname)
    result = await db.execute(query)
    user = result.scalar_one_or_none()

    # Không tìm thấy tài khoản
    if user is None:
        raise HTTPException(status_code=404, detail="Account not found")

    # Sai mật khẩu
    if not verify_password(login_user.password, user.password):
        raise HTTPException(status_code=400, detail="Incorrect password")

    # Tài khoản chưa được kích hoạt
    if user.status != StatusUserEnum.ACTIVE:
        raise HTTPException(status_code=403, detail="Account is not active")

    # Lấy roles của user - bây giờ đã được eager load
    try:
        roles = [role.name.value for role in user.roles] if user.roles else ["USER"]
    except Exception as e:
        # Fallback nếu có lỗi với roles
        roles = ["USER"]
    
    # Tạo token
    token = create_full_token({
        "id": user.id,
        "roles": roles,
        "accountname": user.accountname
    })

    return LoginReponseSchema(
        access_token=token["access_token"],
        refresh_token=token["refresh_token"],
        token_type="bearer"
    )