from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.InforTypeProduct import InforTypeProduct
from app.schemas.Message.Message import MessageSchema 

async def delete_information_type_product(information_type_product_id: int, db: AsyncSession) -> MessageSchema:
    try:
        # Kiểm tra tồn tại
        result = await db.execute(select(InforTypeProduct).where(InforTypeProduct.id == information_type_product_id))
        information_type_product = result.scalar_one_or_none()
        if not information_type_product:
            raise HTTPException(status_code=404, detail="Information type product not found")

        # Xóa
        await db.delete(information_type_product)
        await db.commit()

        return MessageSchema(
            status="success",
            message="Information type product deleted successfully"
        )

    except HTTPException as httpex:
        await db.rollback()
        raise httpex
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
