from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from sqlalchemy import select, update
from app.models.AccountVuavia import AccountVuavia
from app.models.TypeProduct import TypeProduct
from app.schemas.AccountVuaviaSchema.SellAccountSchema import SellAccountRequestSchema, AccountSelectionSchema
from typing import List

async def SellAccountService(sell_request: SellAccountRequestSchema, db: AsyncSession) -> List[AccountSelectionSchema]:
    """
    Service để bán accounts - assign accounts AVAILABLE cho customer
    """
    try:
        # 1. Kiểm tra type_product_id tồn tại
        type_check = await db.execute(select(TypeProduct).where(TypeProduct.id == sell_request.type_product_id))
        if not type_check.scalar_one_or_none():
            raise HTTPException(status_code=404, detail="Type product not found")
        
        # 2. Lấy accounts AVAILABLE từ type_product_id
        query = select(AccountVuavia).where(
            AccountVuavia.type_product_id == sell_request.type_product_id,
            AccountVuavia.status == 'AVAILABLE'
        ).limit(sell_request.quantity)
        
        result = await db.execute(query)
        available_accounts = result.scalars().all()
        
        if len(available_accounts) < sell_request.quantity:
            raise HTTPException(
                status_code=400, 
                detail=f"Not enough accounts available. Requested: {sell_request.quantity}, Available: {len(available_accounts)}"
            )
        
        # 3. Update status của accounts thành SOLD
        account_ids = [acc.id for acc in available_accounts]
        await db.execute(
            update(AccountVuavia)
            .where(AccountVuavia.id.in_(account_ids))
            .values(status='SOLD')
        )
        
        await db.commit()
        
        # 4. Trả về thông tin accounts (bao gồm password để customer sử dụng)
        return [AccountSelectionSchema.model_validate(acc) for acc in available_accounts]
        
    except HTTPException as httpex:
        await db.rollback()
        raise httpex
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

async def GetAvailableCountByType(type_product_id: int, db: AsyncSession) -> int:
    """
    Service để đếm số accounts AVAILABLE theo type
    """
    try:
        query = select(AccountVuavia).where(
            AccountVuavia.type_product_id == type_product_id,
            AccountVuavia.status == 'AVAILABLE'
        )
        result = await db.execute(query)
        accounts = result.scalars().all()
        return len(accounts)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
