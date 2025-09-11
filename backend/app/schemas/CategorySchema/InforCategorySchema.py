from pydantic import BaseModel
from app.schemas.TypeProductSchema.InforTypeProductSchema import InforTypeProductSchema
class InforCategorySchema(BaseModel):
    id: int
    name: str
    description: str
    
    class Config:
        from_attributes = True
