from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.InforTypeProduct import InforTypeProduct
from app.schemas.Message.Message import MessageSchema 
from app.schemas.InformationTypeProduct.InformationTypeProduct import InformationTypeProductUpdate

async def UpdateInformationTypeProductService(information_type_product_id: int, info: InformationTypeProductUpdate, db: AsyncSession) -> MessageSchema:
     try:
        result = await db.execute(select(InforTypeProduct).where(InforTypeProduct.id == information_type_product_id))
        information_type_product = result.scalar_one_or_none()
        if not information_type_product:
            raise HTTPException(status_code=404, detail="Information type product not found")

        information_type_product.describe = info.describe
        information_type_product.type_product_id = info.type_product_id

        db.add(information_type_product)
        await db.commit()
        await db.refresh(information_type_product)

        return MessageSchema(
            status="success",
            message="Information type product updated successfully"
        )
     except HTTPException as httpex:
            await db.rollback()
            return MessageSchema(
                status="error",
                message=str(httpex.detail)
            )
     except Exception as e:
            await db.rollback()
            return MessageSchema(
                status="error",
                message=str(e)
            )
