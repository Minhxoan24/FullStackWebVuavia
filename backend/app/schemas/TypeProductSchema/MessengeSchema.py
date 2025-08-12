from pydantic import BaseModel
class MessengeSchema(BaseModel):
    message: str
    