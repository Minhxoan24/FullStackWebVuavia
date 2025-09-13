from pydantic import BaseModel, field_validator
from typing import Optional, List

class CreateVuaviaSchema(BaseModel):
    login_name: str
    password: str
    type_product_id: int  # Thêm trường này

    @field_validator("login_name")
    def validate_login_name(cls, value):
        if not value or not value.strip():
            raise ValueError("Login name cannot be empty")
        if len(value.strip()) > 200:
            raise ValueError("Login name must be at most 200 characters")
        return value.strip()

    @field_validator("password")
    def validate_password(cls, value):
        if not value or not value.strip():
            raise ValueError("Password cannot be empty")
        if len(value.strip()) > 200:
            raise ValueError("Password must be at most 200 characters")
        return value.strip()

    @field_validator("type_product_id")
    def validate_type_product_id(cls, value):
        if value <= 0:
            raise ValueError("Type product ID must be a positive integer")
        return value

class BulkCreateVuaviaSchema(BaseModel):
    accounts: List[CreateVuaviaSchema]
    
    @field_validator("accounts")
    def validate_accounts(cls, value):
        if not value:
            raise ValueError("Accounts list cannot be empty")
        if len(value) > 1000:  # Giới hạn để tránh overload
            raise ValueError("Cannot create more than 1000 accounts at once")
        return value
