from pydantic import BaseModel
from typing import Any, Dict, Union , List, Optional
JsonType = Union[str, Dict[str, Any], List[Any]]
class InformationTypeProductBase(BaseModel):
    describe:  JsonType   # cho phép mọi key, value
    type_product_id: int

class InformationTypeProductCreate(InformationTypeProductBase):
    pass

class InformationTypeProductUpdate(InformationTypeProductBase):
    pass
