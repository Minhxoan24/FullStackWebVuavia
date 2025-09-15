from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.DataBase import get_async_session
from app.schemas.InformationTypeProduct.InformationTypeProduct import InformationTypeProductCreate , InformationTypeProductUpdate , InformationTypeProductBase
from app.service.InformationTypeProduct.CreateInformationTypeProduct import CreateInformationTypeProductService
from app.service.InformationTypeProduct.UpdateInformationTypeProduct import UpdateInformationTypeProductService
from app.service.InformationTypeProduct.DeleteInformationTypeProduct import delete_information_type_product
from app.service.InformationTypeProduct.GetInforTypeproduct import GetInforTypeproductService
from app.schemas.Message.Message import MessageSchema
 
from sqlalchemy import select

router = APIRouter(
    prefix="/information-type-products",
    tags=["InformationTypeProduct"]
)

@router.post("/", response_model=MessageSchema)
async def create_information_type_product(info: InformationTypeProductCreate, db: AsyncSession = Depends(get_async_session)):
    return await CreateInformationTypeProductService(info, db)
@router.put("/{information_type_product_id}", response_model=MessageSchema)
async def update_information_type_product(information_type_product_id: int, info: InformationTypeProductUpdate, db: AsyncSession = Depends(get_async_session)):
    return await UpdateInformationTypeProductService(information_type_product_id, info, db)
@router.delete("/{information_type_product_id}", response_model=MessageSchema)
async def delete_information_type_product_endpoint(information_type_product_id: int, db: AsyncSession = Depends(get_async_session)):
    return await delete_information_type_product(information_type_product_id, db)
@router.get("/{information_type_product_id}", response_model=InformationTypeProductBase)
async def get_information_type_product_endpoint(information_type_product_id: int, db: AsyncSession = Depends(get_async_session)):
    return await GetInforTypeproductService(information_type_product_id, db)
