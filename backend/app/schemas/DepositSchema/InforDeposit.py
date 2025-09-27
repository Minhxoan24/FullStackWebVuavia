
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class DepositResponse(BaseModel):
    id: int
    amount: float
    transaction_code: str
    status: str
    qr_code_url: Optional[str] = None
    bank_info: dict 
    created_at: datetime