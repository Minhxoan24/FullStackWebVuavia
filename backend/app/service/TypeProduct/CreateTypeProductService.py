from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select 
from fastapi import HTTPException
from app.models.TypeProduct import TypeProduct
from app.schemas.TypeProductSchema.CreateTypeProductSchema import CreateTypeProductSchema 
from app.schemas.TypeProductSchema.InforTypeProductSchema import InforTypeProductSchema
from app.schemas.Message.Message import MessageSchema
async def CreateTypeProductService(type_product_data: CreateTypeProductSchema, db: AsyncSession):
    try:
        query = select(TypeProduct).where(TypeProduct.name == type_product_data.name)
        result = await db.execute(query)
        Tp = result.scalar_one_or_none()
        if Tp is not None:
            raise HTTPException(status_code=400, detail="Type product already exists")

        new_type_product = TypeProduct(
            name=type_product_data.name, 
            description=type_product_data.description,
            price=type_product_data.price,
            image=type_product_data.image,
            category_id=type_product_data.category_id
        )
        db.add(new_type_product)
        await db.commit()
        await db.refresh(new_type_product)
        return MessageSchema(message="Type product created successfully")
    except HTTPException as httpex:
        raise httpex
    except Exception as e:
        await db.rollback()  
        raise HTTPException(status_code=500, detail=str(e))
