from pydantic import BaseModel
from datetime import datetime

class OrderResponseSchema(BaseModel):
    order_id: int
    time: datetime
    quantity: int
    total_amount: float
    order_detail_id: int
    status: str
    
    class Config:
        from_attributes = True
