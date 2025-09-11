from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select
from app.models.Users import User
from app.schemas.AccountSchema.AccountUpdateSchema import AccountUpdateSchema, MessegeUpdateSchema

async def UpdateAccountInformationService(
    data: AccountUpdateSchema, 
    user: User, 
    db: AsyncSession
) -> MessegeUpdateSchema:
    """
    Service cập nhật thông tin tài khoản người dùng
    """
    try:
        # Kiểm tra xem có thay đổi nào không
        changes_made = False
        
        # Cập nhật các field nếu có giá trị mới
        if data.name is not None and data.name != user.name:
            user.name = data.name
            changes_made = True
            
        if data.surname is not None and data.surname != user.surname:
            user.surname = data.surname
            changes_made = True
            
        if data.email is not None and data.email != user.email:
            # Kiểm tra email đã tồn tại chưa
            query = select(User).where(User.email == data.email, User.id != user.id)
            result = await db.execute(query)
            existing_user = result.scalar_one_or_none()
            
            if existing_user:
                raise HTTPException(status_code=400, detail="Email already exists")
            
            user.email = data.email
            changes_made = True
            
        if data.phone is not None and data.phone != user.phone:
            # Kiểm tra số điện thoại đã tồn tại chưa
            query = select(User).where(User.phone == data.phone, User.id != user.id)
            result = await db.execute(query)
            existing_user = result.scalar_one_or_none()
            
            if existing_user:
                raise HTTPException(status_code=400, detail="Phone number already exists")
                
            user.phone = data.phone
            changes_made = True
            
        if data.avatar is not None and data.avatar != user.avatar:
            user.avatar = data.avatar
            changes_made = True
        
        if not changes_made:
            raise HTTPException(status_code=400, detail="No changes detected")

        # Lưu thay đổi
        db.add(user)
        await db.commit()
        await db.refresh(user)

        return MessegeUpdateSchema(message="User information updated successfully")
        
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=500, 
            detail=f"Internal Server Error: {str(e)}"
        )