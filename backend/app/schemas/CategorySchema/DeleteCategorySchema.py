from pydantic import BaseModel

class DeleteCategorySchema(BaseModel):
    id: int

