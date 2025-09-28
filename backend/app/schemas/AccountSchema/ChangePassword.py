from pydantic import BaseModel, Field, field_validator 
from typing import Optional

class ChangePasswordSchema(BaseModel):
    current_password: str = Field(..., min_length=1, description="Mật khẩu hiện tại", alias="currentPassword")
    new_password: str = Field(..., min_length=8, description="Mật khẩu mới (tối thiểu 8 ký tự)", alias="newPassword")
    confirm_password: str = Field(..., min_length=8, description="Xác nhận mật khẩu mới", alias="confirmPassword")

    class Config:
        allow_population_by_field_name = True

    @field_validator('confirm_password')
    @classmethod
    def passwords_match(cls, v, info):
        if 'new_password' in info.data and v != info.data['new_password']:
            raise ValueError('Mật khẩu xác nhận không khớp')
        return v
    
    @field_validator('new_password')
    @classmethod
    def validate_new_password(cls, v, info):
        if 'current_password' in info.data and v == info.data['current_password']:
            raise ValueError('Mật khẩu mới phải khác mật khẩu hiện tại')
        return v

class ChangePasswordResponse(BaseModel):
    message: str
    success: bool