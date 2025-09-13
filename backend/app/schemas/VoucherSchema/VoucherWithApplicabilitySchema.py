from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.Vouchers import VoucherDiscountType, VoucherType, VoucherStatus

class VoucherWithApplicabilitySchema(BaseModel):
    """Schema trả về voucher kèm thông tin có thể áp dụng hay không"""
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
    
    # Thông tin áp dụng cho đơn hàng hiện tại
    can_apply: bool  # True/False - có thể áp dụng hay không
    reason_cannot_apply: Optional[str] = None  # Lý do không thể áp dụng
    discount_amount_preview: Optional[int] = None  # Số tiền giảm dự kiến
    total_after_discount_preview: Optional[int] = None  # Tổng tiền sau giảm

    class Config:
        from_attributes = True
