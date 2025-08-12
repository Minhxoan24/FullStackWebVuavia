from app.schemas.CategorySchema.DeleteCategorySchema import DeleteCategorySchema
from app.schemas.CategorySchema.MessengeSchema import MessageSchema
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from app.models.Category import Category
async def ServiceDeleteCategory(category_delete: DeleteCategorySchema, db: AsyncSession):
    try:
        # Kiểm tra xem category có tồn tại không
        query = select(Category).where(Category.id == category_delete.id)
        result = await db.execute(query)
        category = result.scalar()
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
        # Xóa category
        delete_query = delete(Category).where(Category.id == category_delete.id)
        await db.execute(delete_query)
        await db.commit()
        return MessageSchema(message="Category deleted successfully")
    except HTTPException as httpex:
        raise httpex
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    