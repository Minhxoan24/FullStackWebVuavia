from pydantic import BaseModel
class MessegeSchema(BaseModel):
    message: str

    class Config:
        from_attributes = True