from pydantic import BaseModel
from typing import Optional
from app.models.Roles import RoleEnum 

class CreateDefaultRoles(BaseModel):
    name: RoleEnum 
