from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select
from sqlalchemy.orm import joinedload
from fastapi import HTTPException
from app.models.TypeProduct import TypeProduct
from app.schemas.TypeProductSchema.InforTypeProductSchema import InforTypeProductSchema
from app.service.AccountVuavias.CountAccount import CountAccountVuaviaService
import json

async def DetailTypeProductService(type_product_id: int, db: AsyncSession) -> InforTypeProductSchema:
    """
    Service lấy thông tin chi tiết TypeProduct kèm số lượng account khả dụng
    """
    try:
        # Query với joinedload để lấy thông tin category (nếu cần)
        query = select(TypeProduct).options(
            joinedload(TypeProduct.category)
        ).where(TypeProduct.id == type_product_id)
        
        result = await db.execute(query)
        type_product = result.scalar_one_or_none()

        if type_product is None:
            raise HTTPException(status_code=404, detail="Type product not found")

        # Đếm số lượng account khả dụng
        count_account = await CountAccountVuaviaService(type_product.id, db)

        # Handle JSONB description field
        description_str = ""
        if type_product.description:
            if isinstance(type_product.description, dict):
                description_str = json.dumps(type_product.description, ensure_ascii=False)
            else:
                description_str = str(type_product.description)

        return InforTypeProductSchema(
            id=type_product.id,
            name=type_product.name,
            description=description_str,
            price=float(type_product.price),  # Đảm bảo convert sang float
            image=type_product.image or "",   # Handle null image
            category_id=type_product.category_id,
            quantity=count_account
        )

    except HTTPException as httpex:
        raise httpex
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting type product detail: {str(e)}")
