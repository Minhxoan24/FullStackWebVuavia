from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from app.models.AccountVuavia import AccountVuavia
from app.schemas.AccountVuaviaSchema.CreateVuavia import CreateVuaviaSchema


async def CreateAccountVuaviaService(account_vuavia: CreateVuaviaSchema, db: AsyncSession):
 try: 
    query = await db.execute(select(AccountVuavia).where(AccountVuavia.login_name == account_vuavia.login_name))
    existing_account = query.one_or_none()
    if existing_account is not None:
        raise HTTPException(status_code=400, detail="Account with this login name already exists")
    new_account = AccountVuavia(
        login_name=account_vuavia.login_name,
        password=account_vuavia.password,
    )
    db.add(new_account)
    await db.commit()
    await db.refresh(new_account)
    return new_account
 except HTTPException as httpex: 
     
     raise httpex  # Preserve the HTTPException raised above:
 except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))