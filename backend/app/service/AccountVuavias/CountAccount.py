from app.models.AccountVuavia import AccountVuavia, StatusAccountVuavia
from fastapi import HTTPException
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, Dict

async def CountAccountVuaviaService(type_product_id: Optional[int] = None, db: AsyncSession = None) -> int:
    """Đếm số lượng account khả dụng theo type product"""
    try:
        query = select(func.count(AccountVuavia.id)).where(
            AccountVuavia.status == StatusAccountVuavia.AVAILABLE
        )
        
        if type_product_id:
            query = query.where(AccountVuavia.type_product_id == type_product_id)
            
        result = await db.execute(query)
        return result.scalar() or 0
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error counting accounts: {str(e)}")

async def GetAccountStatsService(db: AsyncSession) -> Dict[str, int]:
    """Lấy thống kê tổng quan về accounts"""
    try:
        # Count by status
        stats_query = select(
            AccountVuavia.status,
            func.count(AccountVuavia.id).label('count')
        ).group_by(AccountVuavia.status)
        
        result = await db.execute(stats_query)
        stats = {row.status.value: row.count for row in result}
        
        # Ensure all statuses are present
        for status in StatusAccountVuavia:
            if status.value not in stats:
                stats[status.value] = 0
                
        # Total count
        total_query = select(func.count(AccountVuavia.id))
        total_result = await db.execute(total_query)
        stats['TOTAL'] = total_result.scalar() or 0
        
        return stats
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting account stats: {str(e)}")

async def GetAvailableCountByType(type_product_id: int, db: AsyncSession) -> int:
    """Đếm số accounts AVAILABLE cho một type product cụ thể"""
    return await CountAccountVuaviaService(type_product_id, db)
