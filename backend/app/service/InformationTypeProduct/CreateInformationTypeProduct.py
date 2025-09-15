from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.InforTypeProduct import InforTypeProduct
from app.schemas.Message.Message import MessageSchema 
from app.schemas.InformationTypeProduct.InformationTypeProduct import InformationTypeProductCreate 
async def CreateInformationTypeProductService(info: InformationTypeProductCreate, db: AsyncSession) -> MessageSchema:
  try:
     new_info = InforTypeProduct(
         describe=info.describe,
         type_product_id=info.type_product_id
     )
     db.add(new_info)
     await db.commit()
     await db.refresh(new_info)
     return MessageSchema(
         status="success",
         message="Information Type Product created successfully"
     )
  except Exception as e:
     await db.rollback()
     raise HTTPException(status_code=500, detail=str(e))

