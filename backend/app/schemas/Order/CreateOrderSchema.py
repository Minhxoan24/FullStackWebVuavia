from pydantic import BaseModel, field_validator
from typing import Optional

class CreateOrderSchema(BaseModel):
    """Schema cho order trực tiếp - KHÔNG cần giỏ hàng"""
    type_product_id: int
    quantity: int
    voucher_id: Optional[int] = None  # ID của voucher (nếu có)

    class Config:
        from_attributes = True 
        
    @field_validator("quantity")
    def quantity_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError("Quantity must be positive")
        return v
    
    @field_validator("type_product_id")
    def type_product_id_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError("Type product ID must be positive")
        return v
