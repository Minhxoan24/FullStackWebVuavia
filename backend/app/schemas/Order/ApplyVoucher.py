


from pydantic import BaseModel
from typing import Optional


class ApplyVoucherRequest(BaseModel):
    voucher_code: str  # Mã voucher (ví dụ: "FIXED100K")
    cart_amount: int  # Tổng giá giỏ hàng trước giảm giá
    category_id: Optional[int] = None  # ID danh mục (nếu voucher áp dụng cho danh mục)

    class Config:
        from_attributes = True
class ApplyVoucherResponse(BaseModel):
    voucher_id: int  # ID của voucher
    code: str  # Mã voucher
    discount_amount: int  # Số tiền giảm giá
    total_after_discount: int  # Tổng giá sau giảm giá

    class Config:
        from_attributes = True