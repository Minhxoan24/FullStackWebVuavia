from pydantic import BaseModel

class CreateVuaviaSchema(BaseModel):
    login_name : str
    password : str
    