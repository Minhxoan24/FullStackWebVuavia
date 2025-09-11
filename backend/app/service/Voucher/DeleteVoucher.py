from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException
from app.models.Vouchers import Voucher
from app.schemas.Message.Message import MessageSchema 

async def delete_voucher(db: AsyncSession, voucher_id: int):
    """
    Xóa voucher theo ID.
    """
    voucher = await db.scalar(select(Voucher).where(Voucher.id == voucher_id))
    if not voucher:
        raise HTTPException(status_code=404, detail="Voucher not found")

    try:
        await db.delete(voucher)
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    return MessageSchema.model_validate({ "message": "Voucher deleted successfully" })