from pydantic import BaseModel
from typing import Optional
class ResponseOrderDetailSchema(BaseModel):
    time: str
    quantity: int
    total_amount: int
    type_product_id: int
    total_amount: int
    accounts_info: Optional[dict] = None

    class Config:
        from_attributes = True