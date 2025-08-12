from pydantic import BaseModel
class InforCategorySchema(BaseModel):
    id: int
    name: str
    description: str
    
    class Config:
        from_attributes = True