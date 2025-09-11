from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class VoucherUsageResponseSchema(BaseModel):
    id: int
    voucher_code: str
    voucher_name: str
    discount_amount: int
    used_at: datetime
    order_id: Optional[int]
    is_valid: bool

    class Config:
        from_attributes = True