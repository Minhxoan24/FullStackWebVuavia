from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from sqlalchemy import select, delete
from app.models.AccountVuavia import AccountVuavia

async def InformationAccountVuaviaService(account_id: int, db: AsyncSession):
  try :
    query = select(AccountVuavia).where(AccountVuavia.id == account_id)
    result = await db.execute(query)
    account = result.scalar_one_or_none()

    if not account:
        raise HTTPException(status_code=404, detail="Account not found")

    return account
  except HTTPException as httpex:
    raise httpex
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))