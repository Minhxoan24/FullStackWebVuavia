from enum import Enum
from pydantic import BaseModel, field_validator
from typing import Optional, List
from datetime import datetime

class VoucherStatusSchema(str, Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    EXPIRED = "EXPIRED"

class UpdateVoucherSchema(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    max_discount: Optional[int] = None
    min_order_amount: Optional[int] = None
    expiration_date: Optional[datetime] = None
    usage_limit_total: Optional[int] = None
    usage_limit_per_user: Optional[int] = None
    status: Optional[VoucherStatusSchema] = None
    is_active: Optional[bool] = None