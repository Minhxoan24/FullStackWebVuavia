from pydantic import BaseModel
from typing import Optional

from typing import Any, Optional, Union, List, Dict
from pydantic import BaseModel, field_validator, ConfigDict

# Cho phép description là chuỗi hoặc JSON (dict/list)
JsonType = Union[str, Dict[str, Any], List[Any]]


class InforTypeProductSchema(BaseModel):
    id: int
    name: str
    description: Optional[JsonType] = None
    price: float
    image: str
    category_id: int
    quantity : Optional[int] = None

    class Config:
        from_attributes = True
