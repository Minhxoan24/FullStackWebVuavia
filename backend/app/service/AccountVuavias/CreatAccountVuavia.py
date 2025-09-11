from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from sqlalchemy import select
from app.models.AccountVuavia import AccountVuavia
from app.schemas.AccountVuaviaSchema.CreateVuavia import CreateVuaviaSchema
from app.schemas.Message.Message import MessageSchema


async def CreateAccountVuaviaService(account_vuavia: CreateVuaviaSchema, db: AsyncSession) -> MessageSchema:
    try: 
        query = await db.execute(select(AccountVuavia).where(AccountVuavia.login_name == account_vuavia.login_name))
        existing_account = query.scalar_one_or_none()
        
        if existing_account is not None:
            raise HTTPException(status_code=400, detail="Account with this login name already exists")
        
        new_account = AccountVuavia(
            login_name=account_vuavia.login_name,
            password=account_vuavia.password,
        )
        db.add(new_account)
        await db.commit()
        await db.refresh(new_account)
        
        return MessageSchema(message="Account created successfully")
        
    except HTTPException as httpex: 
        raise httpex
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))