from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select
from app.models.Users import User, StatusUserEnum
from app.models.Roles import RoleEnum
from app.schemas.AccountSchema.AccountRegisterSchema import (
    CreateUserRegisterSchema, 
    ResponseRegisterSchema
)
from app.Utils.HashPassword import hash_password
from app.core.JWT import create_full_token


async def RegisterAccountService(
    new_account: CreateUserRegisterSchema, 
    db: AsyncSession, 
    role_name: RoleEnum = RoleEnum.USER
):
    """
    Dịch vụ đăng ký tài khoản người dùng mới
    """
    try:
        # Kiểm tra trùng lặp email, phone, accountname
        for field, value in [
            ("email", new_account.email),
            ("phone", new_account.phone),
            ("accountname", new_account.accountname),
        ]:
            query = select(User).where(getattr(User, field) == value)
            result = await db.execute(query)
            if result.scalar_one_or_none() is not None:
                raise HTTPException(status_code=400, detail=f"{field.capitalize()} already exists")

        # Mã hóa mật khẩu
        password = hash_password(new_account.password)

        # Tạo user mới
        new_user = User(
            name=new_account.name,
            surname=new_account.surname,
            accountname=new_account.accountname,
            email=new_account.email,
            phone=new_account.phone,
            password=password,
            status=StatusUserEnum.ACTIVE,
        )

        # Lưu user vào DB
        db.add(new_user)
        await db.flush()       # để có ID
        await db.refresh(new_user)  

        # Tạo token sau khi đã có user.id
        token = create_full_token({
            "id": new_user.id,
            "roles": [role_name.value],
            "accountname": new_user.accountname,
        })

        await db.commit()

        # Trả về token và thông tin user
        return ResponseRegisterSchema(
            access_token=token["access_token"],
            refresh_token=token["refresh_token"],
            token_type="bearer"
        )

    except HTTPException as httpex:
        raise httpex
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
