from pydantic import BaseModel,field_validator  
from enum import Enum
from typing import Optional
from datetime import datetime

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

class CreateVoucherRequest(BaseModel):
    code: str
    name: str
    description: Optional[str] = None
    discount_type: VoucherDiscountType
    discount_value: int
    max_discount: Optional[int] = None
    min_order_amount: int = 0
    voucher_type: VoucherType = VoucherType.PUBLIC
    start_date: datetime
    expiration_date: datetime
    usage_limit_total: Optional[int] = None
    usage_limit_per_user: int = 1
    is_active: bool = True

    @field_validator("code")
    def code_must_be_unique(cls, v):
        if not v.strip():
            raise ValueError("Code cannot be empty")
        return v

    @field_validator("discount_value")
    def discount_value_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError("Discount value must be positive")
        return v

    @field_validator("expiration_date")
    def expiration_date_must_be_after_start_date(cls, v, values):
        if "start_date" in values and v <= values["start_date"]:
            raise ValueError("Expiration date must be after start date")
        return v
class CreateVoucherResponse(BaseModel):
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
    class config :
        from_attributes = True