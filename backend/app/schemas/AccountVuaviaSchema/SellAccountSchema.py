from pydantic import BaseModel
from typing import Optional

class AccountSelectionSchema(BaseModel):
    """Schema cho việc bán account - chỉ trả về thông tin cần thiết"""
    id: int
    login_name: str
    password: str  # Chỉ trả password khi bán thực sự
    type_product_id: int
    
    class Config:
        from_attributes = True

class SellAccountRequestSchema(BaseModel):
    """Schema cho request bán account"""
    type_product_id: int
    quantity: int = 1
    
    class Config:
        from_attributes = True
