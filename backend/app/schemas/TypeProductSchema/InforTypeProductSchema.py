from pydantic import BaseModel
from typing import Optional 


class InforTypeProductSchema(BaseModel):
    id: int
    name: str
    description: str
    price: float
    image: str
    category_id: int
    quantity : Optional[int] = None

    class Config:
        from_attributes = True
