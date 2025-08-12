from app.schemas.CategorySchema.UpdateCategorySchema import UpdateCategorySchema
from app.schemas.CategorySchema.MessengeSchema import MessageSchema
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from app.models.Category import Category

async def ServiceUpdateCategory(category_update: UpdateCategorySchema, db: AsyncSession):
    try:
        # 1. Lấy category theo id
        query = select(Category).where(Category.id == category_update.id)
        result = await db.execute(query)
        category = result.scalar_one_or_none()
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")

        # 2. Kiểm tra tên category có trùng với bản ghi khác không
        query_test = select(Category).where(
            Category.name == category_update.name,
            Category.id != category_update.id
        )
        result_test = await db.execute(query_test)
        existing_category = result_test.scalar_one_or_none()
        if existing_category:
            raise HTTPException(status_code=400, detail="Category name already exists")

        # 3. Cập nhật các trường
        category.name = category_update.name
        category.description = category_update.description

        # 4. Commit thay đổi
        await db.commit()
        await db.refresh(category)  # làm mới đối tượng nếu cần

        return MessageSchema(message="Category updated successfully")
    except HTTPException as httpex:
        raise httpex
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
