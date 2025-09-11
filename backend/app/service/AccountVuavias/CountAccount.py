from app.models.AccountVuavia import AccountVuavia, StatusAccountVuavia
from fastapi import HTTPException
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession


async def CountAccountVuaviaService(type_product_id: int, db: AsyncSession) -> int:
    """Đếm số lượng account khả dụng theo type product"""
    try:
        query = await db.execute(
            select(func.count(AccountVuavia.id))
            .where(
                AccountVuavia.status == StatusAccountVuavia.AVAILABLE,
                AccountVuavia.type_product_id == type_product_id
            )
        )
        return query.scalar() or 0
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error counting accounts: {str(e)}")
