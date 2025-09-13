from  pydantic import BaseModel , field_validator
from typing import Optional

class UpdateCategorySchema(BaseModel): 
    name : Optional[str] = None
    description: Optional[str]= None 
    @field_validator("name")
    def validate_name(cls, value):
        if not value or not value.strip():
            raise ValueError("Name cannot be empty")
        if len(value.strip()) < 3:
            raise ValueError("Name must be at least 3 characters long")
        if len(value.strip()) > 200 : 
            raise ValueError("Name must be at most 200 characters long")
        return value.strip()
    @field_validator("description")
    def validate_description(cls, value):
        if value and len(value.strip()) > 1000:
            raise ValueError("Description must be at most 1000 characters long")
        return value.strip() if value else value