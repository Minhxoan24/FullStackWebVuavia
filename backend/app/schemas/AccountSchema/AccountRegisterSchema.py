from pydantic import BaseModel, field_validator
from typing import Optional
import re

class CreateUserRegisterSchema(BaseModel):
    name: str 
    surname: str
    accountname: str
    email: str
    password: str
    phone: Optional[str] = None 

    @field_validator("email")
    def validate_email(cls, value):
        if not value:
            raise ValueError("Email cannot be empty")
        email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(email_pattern, value.strip()):
            raise ValueError("Invalid email address format")
        return value.strip()

    @field_validator("phone")
    def validate_phone(cls, value):
        if not value:
            raise ValueError("Phone number cannot be empty")
        
        value = value.strip().replace(" ", "")
        if value.startswith("+84"):
            value = value.replace("+84", "0", 1)

        phone_pattern = r"^0\d{9}$"  # Số điện thoại phải bắt đầu bằng 0 và có 10 chữ số
        if not re.match(phone_pattern, value):
            raise ValueError("Phone number must start with 0 and contain exactly 10 digits")
        
        return value

    @field_validator("accountname")
    def validate_accountname(cls, value):
        if not value:
            raise ValueError("Account name cannot be empty")
        if len(value.strip()) < 3:
            raise ValueError("Account name must be at least 3 characters long")
        if len(value.strip()) > 30:
            raise ValueError("Account name must be at most 30 characters long")
        return value.strip().replace(" ", "")

    @field_validator("name", "surname")
    def validate_name_surname(cls, value):
        if not value:
            raise ValueError("Name and surname cannot be empty")
        if len(value.strip()) < 2:
            raise ValueError("Name and surname must be at least 2 characters long")
        if len(value.strip()) > 100:
            raise ValueError("Name and surname must be at most 100 characters long")
        return value.strip()

    @field_validator("password")    
    def validate_password(cls, value):
        if not value:
            raise ValueError("Password cannot be empty")
        if len(value.strip()) < 6:
            raise ValueError("Password must be at least 6 characters long")
        if len(value.strip()) > 100:
            raise ValueError("Password must be at most 100 characters long")
        return value.strip().replace(" ", "")
class MessegeRegisterSchema(BaseModel):
    message: str
    class Config:
        from_attributes = True
    