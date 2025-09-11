from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.AccountVuavia import AccountVuavia, StatusAccountVuavia
from typing import List


async def SelectAccountVuaviaService(
    quantity_account: int, 
    type_product_id: int,
    db: AsyncSession
) -> List[AccountVuavia]:
    """Select available accounts for order"""
    try:
        # Sử dụng transaction để đảm bảo consistency
        query = select(AccountVuavia).where(
            AccountVuavia.status == StatusAccountVuavia.AVAILABLE,
            AccountVuavia.type_product_id == type_product_id
        ).limit(quantity_account).with_for_update(skip_locked=True)
        
        result = await db.execute(query)
        accounts = result.scalars().all()
        
        if not accounts:
            raise HTTPException(status_code=404, detail="No available accounts found")
            
        if len(accounts) < quantity_account:
            raise HTTPException(
                status_code=400, 
                detail=f"Not enough available accounts. Required: {quantity_account}, Available: {len(accounts)}"
            )

        # Cập nhật status tạm thời sang HOLD
        for account in accounts:
            account.status = StatusAccountVuavia.HOLD

        await db.flush()
        return accounts

    except HTTPException as httpex:
        raise httpex
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Error selecting accounts: {str(e)}")
# from fastapi import HTTPException
# from sqlalchemy import select
# from sqlalchemy.ext.asyncio import AsyncSession
# from app.models.AccountVuavia import AccountVuavia , StatusAccountVuavia

# async def SelectAccountVuaviaService(quantity_account : int , db: AsyncSession) -> AccountVuavia:
#    try : 
#        with  db.begin():
#            query = select(AccountVuavia).where(AccountVuavia.status == StatusAccountVuavia.AVAILABLE).limit(quantity_account).with_for_update(skip_locked=True)
#            result = await db.execute(query)
#            accounts = result.scalars().all()
#            if not accounts:
               
#                raise HTTPException(status_code=404, detail="No available accounts found")
#            if len(accounts) < quantity_account:
#                 raise HTTPException(status_code=400, detail="Not enough available accounts")
#            for account in accounts:
#                account.status = StatusAccountVuavia.HOLD
#            await db.flush()

#            return accounts
#    except HTTPException as httpex:
#         await db.rollback()
#         raise httpex
#    except Exception as e:
#         await db.rollback()
#         raise HTTPException(status_code=500, detail=f"Error selecting accounts: {str(e)}")
        
   


        
   
