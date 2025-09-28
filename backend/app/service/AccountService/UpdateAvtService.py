from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from app.models.Users import User

async def update_user_avatar(db: AsyncSession, user_id: int, avatar_url: str, avatar_public_id: str | None = None) -> str:
    """
    Cập nhật avatar URL và avatar_public_id cho user.
    """
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="Người dùng không tồn tại")

    user.avatar = avatar_url
    user.avatar_public_id = avatar_public_id

    try:
        await db.flush()
        await db.commit()
        await db.refresh(user)
    except Exception:
        try:
            await db.rollback()
        except Exception:
            pass
        raise HTTPException(status_code=500, detail="Lỗi khi lưu avatar")

    return user.avatar