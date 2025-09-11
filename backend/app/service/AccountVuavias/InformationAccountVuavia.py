from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from sqlalchemy import select
from app.models.AccountVuavia import AccountVuavia
from app.schemas.AccountVuaviaSchema.InforAccountVuaviaSchema import InforAccountVuaviaSchema

async def InformationAccountVuaviaService(db: AsyncSession) -> list[InforAccountVuaviaSchema]:
    """Lấy danh sách tất cả tài khoản"""
    try:
        query = select(AccountVuavia)
        result = await db.execute(query)
        accounts = result.scalars().all()
        
        return [InforAccountVuaviaSchema.model_validate(account) for account in accounts]
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting accounts: {str(e)}")

async def GetAccountVuaviaDetailService(account_id: int, db: AsyncSession) -> InforAccountVuaviaSchema:
    """Lấy thông tin chi tiết một tài khoản"""
    try:
        query = select(AccountVuavia).where(AccountVuavia.id == account_id)
        result = await db.execute(query)
        account = result.scalar_one_or_none()

        if not account:
            raise HTTPException(status_code=404, detail="Account not found")

        return InforAccountVuaviaSchema.model_validate(account)
    
    except HTTPException as httpex:
        raise httpex
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))