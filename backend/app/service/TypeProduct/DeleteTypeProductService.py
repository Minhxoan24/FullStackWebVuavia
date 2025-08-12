from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select, delete
from fastapi import HTTPException
from app.models.TypeProduct import TypeProduct
from app.schemas.TypeProductSchema.DeleteTypeProductSchema import DeleteTypeProductSchema
from app.schemas.TypeProductSchema.MessengeSchema import MessengeSchema
async def DeleteTypeProductService(type_product_data: DeleteTypeProductSchema, db: AsyncSession):
    try:
        query = select(TypeProduct).where(TypeProduct.id == type_product_data.id)
        result = await db.execute(query)
        type_product = result.scalar_one_or_none()
        if type_product is None:
            raise HTTPException(status_code=404, detail="Type product not found")

        delete_query = delete(TypeProduct).where(TypeProduct.id == type_product_data.id)
        await db.execute(delete_query)
        await db.commit()
        return MessengeSchema(message="Type product deleted successfully")
    except HTTPException as httpex:
        raise httpex
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
