from pydantic import BaseModel


class RefreshTokenRequest(BaseModel):
    refresh_token: str

class RefreshTokenResponse(BaseModel):
    access_token: str
    token_type: str = "Bearer"
    class Config:
        from_attributes = True