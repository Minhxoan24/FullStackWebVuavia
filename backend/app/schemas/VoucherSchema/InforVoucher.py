from pydantic import BaseModel
from datetime import datetime
from enum import Enum
from typing import Optional

class VoucherDiscountType(str, Enum):
    PERCENTAGE = "PERCENTAGE"
    FIXED = "FIXED"

class VoucherType(str, Enum):
    PUBLIC = "PUBLIC"
    PERSONAL = "PERSONAL"
    FIRST_TIME = "FIRST_TIME"
    CATEGORY = "CATEGORY"

class VoucherStatus(str, Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    EXPIRED = "EXPIRED"

class VoucherResponseSchema(BaseModel):  # Đổi từ VoucherResponse thành VoucherResponseSchema
    id: int
    code: str
    name: str
    description: Optional[str]
    discount_type: VoucherDiscountType
    discount_value: int
    max_discount: Optional[int]
    min_order_amount: int
    voucher_type: VoucherType
    start_date: datetime
    expiration_date: datetime
    usage_limit_total: Optional[int]
    usage_limit_per_user: int
    used_count: int
    status: VoucherStatus
    is_active: bool
    created_at: datetime
    
    class Config:  # Sửa từ config thành Config
        from_attributes = True