from pydantic import BaseModel
from typing import Optional
class CreateOrderSchema(BaseModel):
   id_TypeProduct : int 
   quanlity : int
   voucher_code: Optional[str] = None
   