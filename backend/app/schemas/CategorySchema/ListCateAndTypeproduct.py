from pydantic import BaseModel
from app.schemas.CategorySchema.InforCategorySchema import InforCategorySchema
from app.schemas.TypeProductSchema.InforTypeProductSchema import InforTypeProductSchema 

class ListTypeProductSchema(BaseModel):
    id: int                    # Thay đổi từ id_category
    name: str                  # Thay đổi từ name_category
    description: str           # Thay đổi từ description_category
    type_products: list[InforTypeProductSchema] = []  # Thay đổi từ type_products_category
    
    class Config:
        from_attributes = True



