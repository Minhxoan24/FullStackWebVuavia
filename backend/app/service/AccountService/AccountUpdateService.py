from fastapi import Depends, HTTPException
from app.core.JWT import verify_access_token, verify_refresh_token
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select
from app.models.Users import User
from app.schemas.AccountSchema.AccountUpdateSchema import AccountUpdateSchema, MessegeUpdateSchema

async def UpdateAccountInformationService(data: AccountUpdateSchema, user: User, db: AsyncSession):

    # Cập nhật thông tin người dùng
    if data.email == user.email:
        raise HTTPException(status_code=400, detail="No changes detected in email")
    try: 
        user.email = data.email
        user.fullname = data.fullname
        user.phone = data.phone
        user.address = data.address

        db.add(user)  # Thêm người dùng đã cập nhật vào phiên làm việc
        await db.commit()  # Commit các thay đổi
        await db.refresh(user)  # Lấy dữ liệu mới nhất từ database

        return MessegeUpdateSchema(message="User information updated successfully") 
    except HTTPException as httpex:
        
        raise httpex  
    except Exception as e:

        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

