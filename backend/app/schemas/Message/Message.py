from pydantic import BaseModel
    
class MessageSchema(BaseModel):
    message: str

    class Config:
        from_attributes = True 