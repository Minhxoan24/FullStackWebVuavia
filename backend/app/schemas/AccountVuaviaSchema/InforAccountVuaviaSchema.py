from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class InforAccountVuaviaSchema(BaseModel):
    id: int
    login_name: str
    status: str
    type_product_id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    # Loại bỏ password khỏi response vì bảo mật
    
    class Config:
        from_attributes = True