from pydantic import BaseModel, field_validator
from typing import Optional
import re

class ForgotPasswordRequestSchema(BaseModel):
    email: Optional[str] = None
    accountname: Optional[str] = None

    @field_validator("email")
    def validate_email(cls, value):
        if not value:
            raise ValueError("Email cannot be empty")
        email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(email_pattern, value.strip()):
            raise ValueError("Invalid email address format")
        return value.strip()


    @field_validator("accountname")
    def validate_accountname(cls, value):
        if not value:
            raise ValueError("Account name cannot be empty")
        if len(value.strip()) < 3:
            raise ValueError("Account name must be at least 3 characters long")
        if len(value.strip()) > 30:
            raise ValueError("Account name must be at most 30 characters long")
        return value.strip().replace(" ", "")
class Code(BaseModel): 
    code: str

    @field_validator("code")
    def validate_code(cls, value):
        if not value:
            raise ValueError("Code cannot be empty")
        if len(value.strip()) != 6:
            raise ValueError("Code must be exactly 6 characters long")
        return value.strip()
class ResetPasswordSchema(BaseModel):
    new_password: str
    confirm_password: str
    @field_validator("new_password", "confirm_password")
    def validate_passwords(cls, value):
        if not value:
            raise ValueError("Password cannot be empty")
        if len(value.strip()) < 6:
            raise ValueError("Password must be at least 6 characters long")
        if len(value.strip()) > 100:
            raise ValueError("Password must be at most 100 characters long")
        return value.strip().replace(" ", "")
    