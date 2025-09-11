from sqlalchemy.ext.asyncio import AsyncSession 
from fastapi import HTTPException
from sqlalchemy import select
from app.schemas.TypeProductSchema.InforTypeProductSchema import InforTypeProductSchema
from app.models.TypeProduct import TypeProduct

async def ListTypeProductService( db : AsyncSession = AsyncSession):
    try : 
        query = await db.execute(select(TypeProduct))
        type_products = query.scalars().all()
        return [InforTypeProductSchema.model_validate(type_product) for type_product in type_products]
    except HTTPException as httpex:
        raise httpex
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))