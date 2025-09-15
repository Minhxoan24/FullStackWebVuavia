from pydantic import BaseModel
    
class MessageSchema(BaseModel):
    status: str
    message: str

    class Config:
        from_attributes = True 