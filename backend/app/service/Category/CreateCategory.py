from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.Category import Category
from app.schemas.CategorySchema.CreateCategorySchema import CreateCategorySchema
from app.schemas.Message.Message import MessageSchema
from app.schemas.CategorySchema.InforCategorySchema import InforCategorySchema
import logging

logger = logging.getLogger(__name__)

async def CreatecategoryServices( category_new : CreateCategorySchema ,  db : AsyncSession):
    try:
        logger.info(f"Creating category: {category_new.name}")
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
        logger.info(f"Category created successfully: {new_category.id}")
        return InforCategorySchema.model_validate(new_category)
    except HTTPException as httpex:
        logger.warning(f"HTTP error creating category: {httpex.detail}")
        raise httpex
    except Exception as e:
        logger.error(f"Error creating category: {e}", exc_info=True)
        await db.rollback()
        raise HTTPException(status_code=500, detail="Internal Server Error")
