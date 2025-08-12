from pydantic import BaseModel, field_validator
from typing import Optional

class ChangePasswordSchema(BaseModel):
    oldPassword: str
    newPassword: str
    confirmPassword: str
    @field_validator("oldPassword", "newPassword", "confirmPassword")
    def validate_passwords(cls, value):
        if not value:
            raise ValueError("Password cannot be empty")
        if len(value.strip()) < 6:
            raise ValueError("Password must be at least 6 characters long")
        if len(value.strip()) > 100:
            raise ValueError("Password must be at most 100 characters long")
        return value.strip().replace(" ", "")
