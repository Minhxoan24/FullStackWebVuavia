from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime
from app.schemas.AccountVuaviaSchema.InforAccountVuaviaSchema import InforAccountVuaviaSchema  # Sửa import này

class ResponseOrderDetailSchema(BaseModel):
    id: int
    time: datetime
    quantity: int
    total_amount: int
    type_product_id: int
    accounts_info: Optional[List[Dict[str, Any]]] = None

    class Config:
        from_attributes = True

class OrderResponseSchema(BaseModel):
    id: int
    user_id: int
    total_amount: int
    status: str
    created_at: datetime
    order_details: List[ResponseOrderDetailSchema]
    
    class Config:
        from_attributes = True
