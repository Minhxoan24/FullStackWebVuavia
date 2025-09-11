from fastapi import HTTPException  
from sqlalchemy import select 
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from app.models.Category import Category
from app.schemas.CategorySchema.ListCateAndTypeproduct import ListTypeProductSchema 
from app.schemas.TypeProductSchema.InforTypeProductSchema import InforTypeProductSchema
import json

async def Detail_List_TypeProduct(db: AsyncSession) -> list[ListTypeProductSchema]:
    """
    Service lấy danh sách category kèm type products
    """
    try:
        query = await db.execute(
            select(Category).options(
                joinedload(Category.type_products)
            )
        )

        # Thêm .unique() để loại bỏ duplicate rows khi sử dụng joinedload
        categories = query.scalars().unique().all()
        
        # Manual mapping với field names mới
        result = []
        for category in categories:
            # Tạo list InforTypeProductSchema objects
            type_products_list = []
            for tp in category.type_products:
                # Handle JSONB description field
                description_str = ""
                if tp.description:
                    if isinstance(tp.description, dict):
                        description_str = json.dumps(tp.description)
                    else:
                        description_str = str(tp.description)
                
                # Tạo InforTypeProductSchema object
                type_product_obj = InforTypeProductSchema(
                    id=tp.id,
                    name=tp.name,
                    description=description_str,
                    price=float(tp.price),
                    image=tp.image or "",
                    category_id=tp.category_id,
                    quantity=None  # Có thể tính quantity từ AccountVuavia nếu cần
                )
                type_products_list.append(type_product_obj)
            
            # Tạo ListTypeProductSchema object với field names mới
            category_obj = ListTypeProductSchema(
                id=category.id,                    # Thay đổi từ id_category
                name=category.name,                # Thay đổi từ name_category
                description=category.description or "",  # Thay đổi từ description_category
                type_products=type_products_list   # Thay đổi từ type_products_category
            )
            result.append(category_obj)
        
        return result

    except HTTPException as httpex:
        raise httpex
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting categories with type products: {str(e)}")