
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.Category import Category
from app.schemas.CategorySchema.CreateCategorySchema import CreateCategorySchema
from app.schemas.CategorySchema.MessengeSchema import MessegeSchema
from app.schemas.CategorySchema.InforCategorySchema import InforCategorySchema

async def CreatecategoryServices( category_new : CreateCategorySchema ,  db : AsyncSession):
    try:
        # Kiểm tra xem category đã tồn tại chưa
        existing_category = await db.execute(
            select(Category).where(Category.name == category_new.name)
        )
        if existing_category.scalar():
            raise HTTPException(status_code=400, detail="Category already exists")
        # Tạo mới category
        new_category = Category(
            name=category_new.name,
            description=category_new.description
        ) 
        db.add(new_category)
        await db.commit()
        await db.refresh(new_category)
        return InforCategorySchema.model_validate(new_category)
    except HTTPException as httpex:
        raise httpex
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail="Internal Server Error")
    