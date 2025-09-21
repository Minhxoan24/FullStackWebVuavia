# app/service/AccountVuavias/SelectAccount.py
from fastapi import HTTPException
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from datetime import datetime, timezone, timedelta
from app.models.AccountVuavia import AccountVuavia, StatusAccountVuavia

HOLD_TIMEOUT_MINUTES = 10

async def SelectAccountVuaviaService(
    type_product_id: int,  # Thay đổi thứ tự
    quantity_account: int,  # Thay đổi thứ tự
    db: AsyncSession
) -> List[AccountVuavia]:
    try:
        # 1) Cleanup HOLD quá hạn
        timeout_threshold = datetime.now(timezone.utc) - timedelta(minutes=HOLD_TIMEOUT_MINUTES)
        await db.execute(
            update(AccountVuavia)
            .where(
                AccountVuavia.status == StatusAccountVuavia.HOLD,
                AccountVuavia.updated_at < timeout_threshold
            )
            .values(status=StatusAccountVuavia.AVAILABLE,
                    
                    orderdetail_id=None)
        )
        await db.flush()

        # 2) Chọn AVAILABLE theo type + khoá bi quan (skip_locked)
        q = (
            select(AccountVuavia)
            .where(
                AccountVuavia.status == StatusAccountVuavia.AVAILABLE,
                AccountVuavia.type_product_id == type_product_id  # Giữ nguyên
            )
            .order_by(AccountVuavia.id.asc())
            .limit(quantity_account)  # Giữ nguyên
            .with_for_update(skip_locked=True)
        )
        result = await db.execute(q)
        accounts = result.scalars().all()

        if not accounts:
            raise HTTPException(status_code=404, detail="No available accounts found")

        if len(accounts) < quantity_account:  # Thay đổi từ new_order.quantity (vì không có new_order ở đây)
            raise HTTPException(
                status_code=400,
                detail=f"Not enough accounts. Requested: {quantity_account}, Available: {len(accounts)}"
            )

        # 3) Đặt HOLD
        now = datetime.now(timezone.utc)
        for acc in accounts:
            acc.status = StatusAccountVuavia.HOLD
            acc.updated_at = now
        await db.flush()

        return accounts

    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Error selecting accounts: {str(e)}")


async def ReleaseHoldAccountsService(account_ids: List[int], db: AsyncSession):
    try:
        await db.execute(
            update(AccountVuavia)
            .where(
                AccountVuavia.id.in_(account_ids),
                AccountVuavia.status == StatusAccountVuavia.HOLD
            )
            .values(
                status=StatusAccountVuavia.AVAILABLE,
                
                orderdetail_id=None
            )
        )
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Error releasing accounts: {str(e)}")
async def MarkAccountsAsSoldService(account_ids: List[int] ,  db: AsyncSession):
    try:
        await db.execute(
            update(AccountVuavia)
            .where(
                AccountVuavia.id.in_(account_ids),
                AccountVuavia.status == StatusAccountVuavia.HOLD
            )
            .values(
                status=StatusAccountVuavia.SOLD,
            
            
            )
        )
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Error marking accounts as sold: {str(e)}")
