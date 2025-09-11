from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.DataBase import get_async_session
from app.core.auth import get_current_user
from app.models.Users import User

from app.schemas.TransactionHistory.ResTransactionHistory import TransactionHistoryResponse
from app.service.TransactionHistory.GetTransactionHistory import GetUserTransactionHistoryService

router = APIRouter(tags=["TransactionHistory"], prefix="/transaction-history")

@router.get("/my-transactions", response_model=list[TransactionHistoryResponse])
async def get_my_transactions(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session)
):
    """
    Lấy lịch sử giao dịch của người dùng hiện tại
    """
    try:
        return await GetUserTransactionHistoryService(current_user, db)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting transactions: {str(e)}")