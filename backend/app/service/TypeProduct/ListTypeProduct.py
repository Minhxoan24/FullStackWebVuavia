from sqlalchemy.ext.asyncio import AsyncSession 
from fastapi import HTTPException
from sqlalchemy import select
from app.schemas.TypeProductSchema.InforTypeProductSchema import InforTypeProductSchema
from app.models.TypeProduct import TypeProduct
from app.service.AccountVuavias.CountAccount import CountAccountVuaviaService

async def ListTypeProductService(db: AsyncSession):
    try: 
        query = await db.execute(select(TypeProduct))
        type_products = query.scalars().all()
        if not type_products:
            raise HTTPException(status_code=404, detail="No products found")

        # Sửa: Dùng vòng lặp để await quantity cho từng sản phẩm
        results = []
        for type_product in type_products:
            quantity = await CountAccountVuaviaService(type_product.id, db)
            results.append(InforTypeProductSchema(
                id=type_product.id,
                name=type_product.name,
                description=type_product.description,
                price=type_product.price,
                image=type_product.image,
                category_id=type_product.category_id,
                quantity=quantity
            ))
        return results

    except HTTPException as httpex:
        raise httpex
    except Exception as e:
        # Xóa db.rollback() vì không cần cho read query
        raise HTTPException(status_code=500, detail=str(e))

async def ListTypeProductByCategory(id_category: int, db: AsyncSession):
    try: 
        # Sửa từ TypeProduct.category thành TypeProduct.category_id
        query = await db.execute(select(TypeProduct).where(TypeProduct.category_id == id_category))
        type_products = query.scalars().all()
        
        if not type_products:
            raise HTTPException(status_code=404, detail=f"No products found for category {id_category}")
        
        # Thêm quantity để nhất quán với hàm trên (nếu schema yêu cầu)
        results = []
        for type_product in type_products:
            quantity = await CountAccountVuaviaService(type_product.id, db)
            results.append(InforTypeProductSchema(
                id=type_product.id,
                name=type_product.name,
                description=type_product.description,
                price=type_product.price,
                image=type_product.image,
                category_id=type_product.category_id,
                quantity=quantity
            ))
        return results
    except HTTPException as httpex:
        raise httpex
    except Exception as e:
        # Xóa db.rollback()
        raise HTTPException(status_code=500, detail=str(e))