from pydantic import BaseModel, field_validator
from typing import Optional
import re 
class AccountUpdateSchema(BaseModel):
    name: Optional[str] = None
    surname: Optional[str] = None
    avatar: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
  
    @field_validator("email")
    def validate_email(cls, value):
        if value is not None:
            email_regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
            if not re.match(email_regex, value):
                raise ValueError("Invalid email format")
        return value
    @field_validator("phone")
    def validate_phone(cls, value):
        if value is not None:
            value = value.strip().replace(" ", "")
            if value.startswith("+84"):
                value = value.replace("+84", "0", 1)
            phone_regex = r"^0\d{9}$"
            if not re.match(phone_regex, value):
                raise ValueError("Phone number must start with 0 and contain exactly 10 digits")
        return value
    @field_validator("name", "surname")
    def validate_name_surname(cls, value):
        if value is not None:
            value = value.strip()
            if len(value) < 2:
                raise ValueError("Name and surname must be at least 2 characters long")
            if len(value) > 100:
                raise ValueError("Name and surname must be at most 100 characters long")
        return value
class MessegeUpdateSchema(BaseModel):
    message: str

    class Config:
        from_attributes = True
      