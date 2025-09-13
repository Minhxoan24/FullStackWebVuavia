from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from sqlalchemy import select, delete
from app.models.AccountVuavia import AccountVuavia
from app.schemas.Message.Message import MessageSchema

async def DeleteAccountVuaviaService(account_id: int, db: AsyncSession):
    try:
        # Kiểm tra tồn tại
        result = await db.execute(select(AccountVuavia).where(AccountVuavia.id == account_id))
        account = result.scalar_one_or_none()
        if not account:
            raise HTTPException(status_code=404, detail="Account not found")

        # Xóa
        await db.execute(delete(AccountVuavia).where(AccountVuavia.id == account_id))
        await db.commit()

        return MessageSchema(message="Account deleted successfully")

    except HTTPException as httpex:
        raise httpex
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
