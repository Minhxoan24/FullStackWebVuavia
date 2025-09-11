from typing import Any, Optional, Union, List, Dict
from pydantic import BaseModel, field_validator, ConfigDict

# Cho phép description là chuỗi hoặc JSON (dict/list)
JsonType = Union[str, Dict[str, Any], List[Any]]

class CreateTypeProductSchema(BaseModel):
    name: str
    price: int                      # DB là Integer
    image: Optional[str] = None     # DB nullable -> optional
    category_id: int
    description: Optional[JsonType] = None  # DB JSONB -> cho phép dict/list hoặc str

    # Cấu hình: không cho thừa field
    model_config = ConfigDict(extra='forbid')

    @field_validator("name")
    def validate_name(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Name cannot be empty")
        if len(v) > 200:
            raise ValueError("Name must be at most 200 characters long")
        return v

    @field_validator("image")
    def validate_image(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        v = v.strip()
        if len(v) > 500:
            raise ValueError("Image URL must be at most 500 characters long")
        return v

    @field_validator("price")
    def validate_price(cls, v: int) -> int:
        if v <= 0:
            raise ValueError("Price must be a positive integer")
        return v

    @field_validator("description")
    def validate_description(cls, v: Optional[JsonType]) -> Optional[JsonType]:
        if v is None:
            return v
        # Cho phép: string hoặc JSON (dict/list). Giới hạn ~1000 ký tự sau khi serialize.
        if isinstance(v, str):
            s = v.strip()
            if len(s) > 1000:
                raise ValueError("Description must be at most 1000 characters long")
            return s
        elif isinstance(v, (dict, list)):
            import json
            try:
                s = json.dumps(v, ensure_ascii=False)
            except Exception:
                raise ValueError("Description must be valid JSON")
            if len(s) > 1000:
                raise ValueError("Description JSON is too long (max 1000 chars when serialized)")
            return v
        else:
            raise ValueError("Description must be a string, object, or array")
