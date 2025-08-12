from pydantic import BaseModel

class InforTypeProductSchema(BaseModel):
    id: int
    name: str
    description: str
    price: float
    image: str
    category_id: int
    category_name: str
    class Config:
        from_attributes = True
