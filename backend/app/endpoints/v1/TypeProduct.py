from app.db.DataBase import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends
from app.schemas.TypeProductSchema.CreateTypeProductSchema import CreateTypeProductSchema
from app.schemas.TypeProductSchema.InforTypeProductSchema import InforTypeProductSchema
from app.schemas.TypeProductSchema.UpdateTypeProductSchema import UpdateTypeProductSchema
from app.schemas.TypeProductSchema.DeleteTypeProductSchema import DeleteTypeProductSchema
from app.schemas.TypeProductSchema.MessengeSchema import MessengeSchema 
from app.service.TypeProduct.CreateTypeProductService import CreateTypeProductService
from app.service.TypeProduct.UpdateTypeProductService import UpdateTypeProductService
from app.service.TypeProduct.DeleteTypeProductService import DeleteTypeProductService
from app.service.TypeProduct.TypeProductInformationService import GetTypeProductInformationService
router = APIRouter(prefix="/type-product", tags=["TypeProduct"])
@router.post("/create", response_model=MessengeSchema )
async def create_type_product(type_product_new: CreateTypeProductSchema, db: AsyncSession = Depends(get_async_session)):
    return await CreateTypeProductService(type_product_new, db)
@router.put("/update", response_model=InforTypeProductSchema)
async def update_type_product(type_product_update: UpdateTypeProductSchema, db: AsyncSession = Depends(get_async_session)):
    return await UpdateTypeProductService(type_product_update, db)
@router.delete("/delete", response_model=MessengeSchema)
async def delete_type_product(type_product_delete: DeleteTypeProductSchema, db: AsyncSession = Depends(get_async_session)):
    return await DeleteTypeProductService(type_product_delete, db) 