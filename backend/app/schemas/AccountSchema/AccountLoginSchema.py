from pydantic import BaseModel, field_validator
from typing import Optional
import re

 
class LoginUserSchema(BaseModel):
    
    accountname: str
    password: str
   

    @field_validator("accountname")
    def validate_accountname(cls, value):
        if not value:
            raise ValueError("Account name cannot be empty")
        if len(value.strip()) < 3:
            raise ValueError("Account name must be at least 3 characters long")
        if len(value.strip()) > 30:
            raise ValueError("Account name must be at most 30 characters long")
        return value.strip().replace(" ", "")

    @field_validator("password")
    def validate_password(cls, value):
        if not value:
            raise ValueError("Password cannot be empty")
        if len(value.strip()) < 6:
            raise ValueError("Password must be at least 6 characters long")
        if len(value.strip()) > 100:
            raise ValueError("Password must be at most 100 characters long")
        return value.strip().replace(" ", "")
class LoginReponseSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    class Config:
        from_attributes = True