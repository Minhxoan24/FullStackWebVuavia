from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.TransactionHistory import TransactionHistory
from app.models.Users import User
from app.schemas.TransactionHistory.ResTransactionHistory import TransactionHistoryResponse

async def GetUserTransactionHistoryService(user: User, db: AsyncSession) -> list[TransactionHistoryResponse]:
    """Service lấy lịch sử giao dịch của user"""
    try:
        # Query lấy tất cả giao dịch của user, sắp xếp từ mới nhất
        query = select(TransactionHistory).where(
            TransactionHistory.user_id == user.id
        ).order_by(TransactionHistory.created_at.desc())
        
        result = await db.execute(query)
        transactions = result.scalars().all()
        
        # Convert sang response schema
        return [TransactionHistoryResponse.model_validate(transaction) for transaction in transactions]
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting transaction history: {str(e)}")