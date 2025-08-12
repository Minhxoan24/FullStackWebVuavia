
from fastapi import APIRouter, Depends 
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.DataBase import get_async_session
from app.schemas.CategorySchema.CreateCategorySchema import CreateCategorySchema 
from app.schemas.CategorySchema.InforCategorySchema import InforCategorySchema
from app.schemas.CategorySchema.UpdateCategorySchema import UpdateCategorySchema
from app.schemas.CategorySchema.DeleteCategorySchema import DeleteCategorySchema
from app.schemas.CategorySchema.MessengeSchema import MessengeSchema
from app.service.Category.DeleteCategory import ServiceDeleteCategory
from app.service.Category.UpdateCategory import ServiceUpdateCategory
from app.service.Category.CreateCategory import ServiceCreatecategory
router = APIRouter(prefix="/category", tags=["Category"])

@router.post("/create", response_model=InforCategorySchema)
async def create_category(category_new: CreateCategorySchema, db: AsyncSession = Depends(get_async_session)):
   return await ServiceCreatecategory(category_new, db)
@router.put("/update", response_model= MessengeSchema)
async def update_category(category_update: UpdateCategorySchema, db: AsyncSession = Depends(get_async_session)):
    return await ServiceUpdateCategory(category_update, db)
@router.delete("/delete", response_model=MessengeSchema)
async def delete_category(category_delete: DeleteCategorySchema, db: AsyncSession = Depends(get_async_session)):
    return await ServiceDeleteCategory(category_delete, db)