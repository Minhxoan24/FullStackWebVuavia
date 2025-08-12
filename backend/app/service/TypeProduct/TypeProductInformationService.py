from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select, delete
from fastapi import HTTPException
from app.models.TypeProduct import TypeProduct
from app.schemas.TypeProductSchema.InforTypeProductSchema import InforTypeProductSchema

async def GetTypeProductInformationService(type_product_id: int, db: AsyncSession):
    try:
        query = select(TypeProduct).where(TypeProduct.id == type_product_id)
        result = await db.execute(query)
        type_product = result.scalar_one_or_none()
        if type_product is None:
            raise HTTPException(status_code=404, detail="Type product not found")
        return InforTypeProductSchema.model_validate(type_product)
    except HTTPException as httpex:
        raise httpex
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
