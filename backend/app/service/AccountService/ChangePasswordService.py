from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.Users import User
from app.schemas.AccountSchema.ChangePassword import ChangePasswordSchema, ChangePasswordResponse
from app.Utils.HashPassword import hash_password, verify_password

async def ChangePasswordService(
    password_data: ChangePasswordSchema,
    current_user: User,
    db: AsyncSession
) -> ChangePasswordResponse:
    """
    Service để thay đổi mật khẩu người dùng
    """
    try:
        # Kiểm tra mật khẩu hiện tại
        if not verify_password(password_data.current_password, current_user.password):
            raise HTTPException(
                status_code=400, 
                detail="Mật khẩu hiện tại không đúng"
            )
        
        # Mã hóa mật khẩu mới
        hashed_new_password = hash_password(password_data.new_password)
        
        # Cập nhật mật khẩu trong database
        current_user.password = hashed_new_password
        
        # Sử dụng async methods
        db.add(current_user)
        await db.commit()
        await db.refresh(current_user)
        
        return ChangePasswordResponse(
            message="Mật khẩu đã được thay đổi thành công",
            status ="success"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()  # Async rollback
        raise HTTPException(
            status_code=500, 
            detail=f"Lỗi khi thay đổi mật khẩu: {str(e)}"
        )