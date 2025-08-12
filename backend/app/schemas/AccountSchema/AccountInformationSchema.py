from pydantic import BaseModel
from typing import Optional


class InformationAccountSchema(BaseModel):
    name: str
    surname: str
    accountname: str
    email: str
    avatar: Optional[str] = None
    phone: str

    class Config:
        from_attributes = True
