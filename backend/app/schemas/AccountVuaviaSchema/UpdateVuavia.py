from pydantic import BaseModel

class UpdateVuaviaSchema(BaseModel):
    id: int
    login_name: str
    password: str