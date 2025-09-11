from app.schemas.Message.Message import MessageSchema
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from app.service.RedisService.RedisService import redis_service

async def cancel_voucher(user_id: int, db: AsyncSession) -> MessageSchema:
    try:
        await redis_service.delete_voucher_cache(user_id)
        return MessageSchema(message="Voucher cancelled successfully")
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")