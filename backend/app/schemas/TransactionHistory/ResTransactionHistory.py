from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TransactionHistoryResponse(BaseModel):
    """Schema đơn giản cho lịch sử giao dịch"""
    id: int
    user_id: int
    type: str  # "PURCHASE" hoặc "DEPOSIT"
    amount: float
    description: Optional[str] = None
    order_id: Optional[int] = None
    created_at: datetime
    
    class Config:
        from_attributes = True