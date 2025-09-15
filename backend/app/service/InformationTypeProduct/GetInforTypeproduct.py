from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.InforTypeProduct import InforTypeProduct
from app.schemas.Message.Message import MessageSchema 
from app.schemas.InformationTypeProduct.InformationTypeProduct import InformationTypeProductBase

async def GetInforTypeproductService(id: int, db: AsyncSession) -> InformationTypeProductBase:
    try:
        result = await db.execute(select(InforTypeProduct).where(InforTypeProduct.type_product_id == id))
        info = result.scalar_one_or_none()
        if not info:
            raise HTTPException(status_code=404, detail="Information type product not found")
        return InformationTypeProductBase(
            describe=info.describe,
            type_product_id=info.type_product_id
        )
    except HTTPException as httpex:
        raise httpex
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))