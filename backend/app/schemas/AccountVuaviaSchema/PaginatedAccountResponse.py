from pydantic import BaseModel
from typing import List, Optional
from app.schemas.AccountVuaviaSchema.InforAccountVuaviaSchema import InforAccountVuaviaSchema

class PaginatedAccountVuaviaResponse(BaseModel):
    """Response schema cho danh sách accounts với pagination"""
    accounts: List[InforAccountVuaviaSchema]
    total: int
    page: int
    size: int
    total_pages: int
    
    class Config:
        from_attributes = True

class AccountFilterRequest(BaseModel):
    """Filter params cho accounts"""
    page: Optional[int] = 1
    size: Optional[int] = 50
    status: Optional[str] = None  # AVAILABLE, HOLD, SOLD, EXPIRED
    type_product_id: Optional[int] = None
    
    class Config:
        from_attributes = True
