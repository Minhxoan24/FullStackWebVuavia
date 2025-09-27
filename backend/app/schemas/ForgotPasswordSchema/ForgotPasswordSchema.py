from pydantic import BaseModel, EmailStr, Field

class RequestOTPBody(BaseModel):
    email: EmailStr

class VerifyOTPBody(BaseModel):
    email: EmailStr
    otp: str = Field(min_length=4, max_length=8)

class ResetPasswordBody(BaseModel):
    email: EmailStr
    otp: str = Field(min_length=4, max_length=8)
    new_password: str = Field(min_length=6, max_length=128)

class OTPStatusResponse(BaseModel):
    status: str
    message: str

class ResetPasswordResponse(BaseModel):
    status: str
    message: str
