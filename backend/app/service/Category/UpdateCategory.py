from app.schemas.CategorySchema.UpdateCategorySchema import UpdateCategorySchema
from app.schemas.Message.Message import MessageSchema
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from app.models.Category import Category

async def ServiceUpdateCategory(Category_id: int, category_update: UpdateCategorySchema, db: AsyncSession):
    try:
        # 1. Lấy category theo id
        query = select(Category).where(Category.id == Category_id)
        result = await db.execute(query)
        category = result.scalar_one_or_none()
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")

        # 2. Kiểm tra tên category có trùng với bản ghi khác không (chỉ nếu name được cung cấp)
        if category_update.name is not None:
            query_test = select(Category).where(
                Category.name == category_update.name,
                Category.id != Category_id  # Sửa: dùng Category_id thay vì category_update.id
            )
            result_test = await db.execute(query_test)
            existing_category = result_test.scalar_one_or_none()
            if existing_category:
                raise HTTPException(status_code=400, detail="Category name already exists")

        # 3. Cập nhật các trường chỉ nếu chúng được cung cấp
        if category_update.name is not None:
            category.name = category_update.name
        if category_update.description is not None:
            category.description = category_update.description

        # 4. Commit thay đổi
        await db.commit()
        await db.refresh(category)  # Làm mới đối tượng nếu cần

        return MessageSchema(message="Category updated successfully")
    except HTTPException as httpex:
        raise httpex
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
