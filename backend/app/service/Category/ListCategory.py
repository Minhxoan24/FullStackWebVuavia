from sqlalchemy.ext.asyncio import AsyncSession 
from sqlalchemy import select
from app.models.Category import Category
from app.schemas .CategorySchema.InforCategorySchema import InforCategorySchema
from fastapi import HTTPException

async def ListCategoryService( db : AsyncSession = AsyncSession):
    try : 
        query = await db.execute(select(Category))
        categories = query.scalars().all()
        return [InforCategorySchema.model_validate(category) for category in categories]
    except HTTPException as httpex:
        raise httpex
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))