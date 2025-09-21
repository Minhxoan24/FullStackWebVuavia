from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import datetime

class ResponseOrderDetailSchema(BaseModel):
    id: int
    time: datetime
    quantity: int
    total_amount: float
    type_product_id: int
    accounts_info: List[Dict]

    class Config:
        from_attributes = True