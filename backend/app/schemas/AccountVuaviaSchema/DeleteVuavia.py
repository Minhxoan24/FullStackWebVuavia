from pydantic import BaseModel
from typing import Optional

class DeleteVuaviaSchema(BaseModel):
    id: Optional[int] = None
    login_name: Optional[str] = None
