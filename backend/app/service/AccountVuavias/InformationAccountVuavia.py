from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, Query
from sqlalchemy import select, func
from app.models.AccountVuavia import AccountVuavia, StatusAccountVuavia
from app.schemas.AccountVuaviaSchema.InforAccountVuaviaSchema import InforAccountVuaviaSchema
from typing import Optional

class PaginatedAccountResponse:
    def __init__(self, accounts: list[InforAccountVuaviaSchema], total: int, page: int, size: int):
        self.accounts = accounts
        self.total = total
        self.page = page
        self.size = size
        self.total_pages = (total + size - 1) // size

async def InformationAccountVuaviaService(
    db: AsyncSession, 
    page: int = 1, 
    size: int = 50,
    status: Optional[str] = None,
    type_product_id: Optional[int] = None
) -> PaginatedAccountResponse:
    """Lấy danh sách tài khoản với pagination và filter"""
    try:
        # Validate pagination params
        if page < 1:
            page = 1
        if size < 1 or size > 100:  # Giới hạn max 100 items per page
            size = 50
            
        # Build query với filter
        query = select(AccountVuavia)
        count_query = select(func.count(AccountVuavia.id))
        
        if status:
            query = query.where(AccountVuavia.status == status)
            count_query = count_query.where(AccountVuavia.status == status)
            
        if type_product_id:
            query = query.where(AccountVuavia.type_product_id == type_product_id)
            count_query = count_query.where(AccountVuavia.type_product_id == type_product_id)
        
        # Get total count
        total_result = await db.execute(count_query)
        total = total_result.scalar()
        
        # Get paginated results
        offset = (page - 1) * size
        query = query.order_by(AccountVuavia.id.desc()).offset(offset).limit(size)
        result = await db.execute(query)
        accounts = result.scalars().all()
        
        account_schemas = [InforAccountVuaviaSchema.model_validate(account) for account in accounts]
        
        return PaginatedAccountResponse(
            accounts=account_schemas,
            total=total,
            page=page,
            size=size
        )
    
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