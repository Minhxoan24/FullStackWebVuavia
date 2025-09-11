from pydantic import BaseModel


class InforAccountVuaviaSchema(BaseModel):
    """Thông tin tài khoản Vuavia"""
    id: int
    login_name: str
    password: str
    
    class Config:
        from_attributes = True