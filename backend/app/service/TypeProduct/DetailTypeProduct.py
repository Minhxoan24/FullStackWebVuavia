from sqlalchemy import select
from sqlalchemy.orm import joinedload  # hoặc selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
import json

from app.models.TypeProduct import TypeProduct
from app.schemas.TypeProductSchema.InforTypeProductSchema import InforTypeProductDetailSchema
from app.service.AccountVuavias.CountAccount import CountAccountVuaviaService

async def DetailTypeProductService(type_product_id: int, db: AsyncSession) -> InforTypeProductDetailSchema:
    try:
        query = await db.execute(
            select(TypeProduct).where(TypeProduct.id == type_product_id))
        type_product = query.scalars().first()

        if type_product is None:
            raise HTTPException(status_code=404, detail="Type product not found")

        # Đếm số lượng account khả dụng (đảm bảo hàm này cũng async và dùng cùng AsyncSession)
        count_account = await CountAccountVuaviaService(type_product.id, db)

        # Handle JSONB description -> trả về string
        description_str = ""
        if type_product.description:
            if isinstance(type_product.description, dict):
                description_str = json.dumps(type_product.description, ensure_ascii=False)
            else:
                description_str = str(type_product.description)

        return InforTypeProductDetailSchema( 
            id=type_product.id,
            name=type_product.name,
            description=description_str,
            price=float(type_product.price) if type_product.price is not None else 0.0,
            image=type_product.image or "",
            category_id=type_product.category_id,
            quantity=count_account,
            
        )

    except HTTPException:
        raise
    except Exception as e:
        # giữ nguyên message để debug
        raise HTTPException(status_code=500, detail=f"Error getting type product detail: {e}")
