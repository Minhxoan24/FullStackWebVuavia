from pydantic import BaseModel, field_validator
from typing import Optional

from pydantic import BaseModel
from typing import Optional

class CreateOrderSchema(BaseModel):
    type_product_id: int
    quantity: int
    price: int  # Tổng giá trước giảm giá (type_product.price * quantity)
    discount_amount: Optional[int] = 0  # Số tiền giảm giá từ voucher
    voucher_id: Optional[int] = None  # ID của voucher (nếu có)

    class Config:
        from_attributes = True 
    @field_validator("quantity")
    def quantity_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError("Quantity must be positive")
        return v
    @field_validator("price")
    def price_must_be_non_negative(cls, v):
        if v < 0:
            raise ValueError("Price must be non-negative")
        return v
    @field_validator("discount_amount")
    def discount_amount_must_be_non_negative(cls, v):
        if v is not None and v < 0:
            raise ValueError("Discount amount must be non-negative")
        return v
    