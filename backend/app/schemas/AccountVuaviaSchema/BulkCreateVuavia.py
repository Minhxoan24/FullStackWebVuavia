from pydantic import BaseModel
from typing import List
from .CreateVuavia import CreateVuaviaSchema

class BulkCreateVuaviaSchema(BaseModel):
    accounts: List[CreateVuaviaSchema]
    
    class Config:
        from_attributes = True
