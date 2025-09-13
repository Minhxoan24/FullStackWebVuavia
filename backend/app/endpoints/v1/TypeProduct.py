from app.db.DataBase import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends
from app.schemas.TypeProductSchema.CreateTypeProductSchema import CreateTypeProductSchema
from app.schemas.TypeProductSchema.InforTypeProductSchema import InforTypeProductSchema
from app.schemas.TypeProductSchema.UpdateTypeProductSchema import UpdateTypeProductSchema
from app.schemas.TypeProductSchema.DeleteTypeProductSchema import DeleteTypeProductSchema
from app.schemas.Message.Message import MessageSchema
from app.service.TypeProduct.CreateTypeProductService import CreateTypeProductService
from app.service.TypeProduct.UpdateTypeProductService import UpdateTypeProductService
from app.service.TypeProduct.DeleteTypeProductService import DeleteTypeProductService
from app.service.TypeProduct.ListTypeProduct import ListTypeProductByCategory


from app.service.TypeProduct.DetailTypeProduct import DetailTypeProductService
from app.service.Category.ListCateAndTypeProduct import Detail_List_TypeProduct
from app.schemas.CategorySchema.ListCateAndTypeproduct import ListTypeProductSchema

router = APIRouter(prefix="/type-product", tags=["TypeProduct"])

@router.post("/create", response_model=MessageSchema)
async def create_type_product(type_product_new: CreateTypeProductSchema, db: AsyncSession = Depends(get_async_session)):
    return await CreateTypeProductService(type_product_new, db)

@router.put("/update", response_model=InforTypeProductSchema)
async def update_type_product(type_product_update: UpdateTypeProductSchema, db: AsyncSession = Depends(get_async_session)):
    return await UpdateTypeProductService(type_product_update, db)

@router.delete("/delete", response_model=MessageSchema)
async def delete_type_product(type_product_delete: DeleteTypeProductSchema, db: AsyncSession = Depends(get_async_session)):
    return await DeleteTypeProductService(type_product_delete, db)

@router.get("/Detail/{item_id}", response_model=InforTypeProductSchema)
async def detail_type_product(item_id: int, db: AsyncSession = Depends(get_async_session)): 
    return await DetailTypeProductService(item_id, db)
@router.get("/list-TypeProduct-with-Category", response_model=list[ListTypeProductSchema])
async def list_categories_with_products(db: AsyncSession = Depends(get_async_session)):
    """Lấy danh sách category kèm type products"""
    return await Detail_List_TypeProduct(db)
@router.get("/list-TypeProduct/{id_category}", response_model=list[InforTypeProductSchema])
async def list_type_products_by_category(id_category: int, db: AsyncSession = Depends(get_async_session)):
    return await ListTypeProductByCategory(id_category, db)