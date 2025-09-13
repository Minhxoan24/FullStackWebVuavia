from pydantic import BaseModel, field_validator
from typing import Optional

class UpdateVuaviaSchema(BaseModel):
    login_name: Optional[str] = None
    password: Optional[str] = None
    type_product_id: Optional[int] = None  # Thêm nếu cần update type

    @field_validator("login_name")
    def validate_login_name(cls, value):
        if value and len(value.strip()) > 200:
            raise ValueError("Login name must be at most 200 characters")
        return value.strip() if value else value

    @field_validator("password")
    def validate_password(cls, value):
        if value and len(value.strip()) > 200:
            raise ValueError("Password must be at most 200 characters")
        return value.strip() if value else value

    @field_validator("type_product_id")
    def validate_type_product_id(cls, value):
        if value is not None and value <= 0:
            raise ValueError("Type product ID must be a positive integer")
        return value