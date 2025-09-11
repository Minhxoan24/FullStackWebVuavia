from pydantic import BaseModel
from typing import Optional


class InformationAccountSchema(BaseModel):
    name: str
    surname: str
    accountname: str
    email: str
    avatar: Optional[str] = None
    phone: str
    balance : int

    class Config:
        from_attributes = True
