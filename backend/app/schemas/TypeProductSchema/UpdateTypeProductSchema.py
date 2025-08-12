from pydantic import BaseModel 
from pydantic import field_validator

class UpdateTypeProductSchema(BaseModel):
    name : str
    description : str
    price : float
    image : str
    category_id : int
    @field_validator("name")
    def validate_name(cls, value):
        if not value or not value.strip():
            raise ValueError("Name cannot be empty")
        if len(value.strip()) > 200 : 
            raise ValueError("Name must be at most 200 characters long")
        return value.strip()
    @field_validator("description")
    def validate_description(cls, value):
        if value and len(value.strip()) > 1000: 
            raise ValueError("Description must be at most 1000 characters long")
        return value.strip() 
    @field_validator("price")
    def validate_price(cls, value):
        if value <= 0:
            raise ValueError("Price must be a positive number")
        return value
    