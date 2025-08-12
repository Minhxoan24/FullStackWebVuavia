from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select, delete
from fastapi import HTTPException
from app.models.TypeProduct import TypeProduct
from app.schemas.TypeProductSchema.UpdateTypeProductSchema import UpdateTypeProductSchema
from app.schemas.TypeProductSchema.MessengeSchema import MessengeSchema
async def UpdateTypeProductService(type_product_data: UpdateTypeProductSchema, db: AsyncSession):
    try:
        query = select(TypeProduct).where(TypeProduct.id == type_product_data.id)
        result = await db.execute(query)
        type_product = result.scalar_one_or_none()
        if type_product is None:
            raise HTTPException(status_code=404, detail="Type product not found")
        # Cập nhật thông tin loại sản phẩm
        type_product.name = type_product_data.name
        type_product.description = type_product_data.description
        type_product.price = type_product_data.price
        type_product.image = type_product_data.image
        type_product.category_id = type_product_data.category_id
        db.add(type_product)
        await db.commit()
        return MessengeSchema(message="Type product updated successfully")
    except HTTPException as httpex:
        raise httpex
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))