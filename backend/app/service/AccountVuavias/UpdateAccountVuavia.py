from fastapi import HTTPException 
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from app.models.AccountVuavia import AccountVuavia
from app.schemas.AccountVuaviaSchema.UpdateVuavia import UpdateVuaviaSchema
from app.schemas.Message.Message import MessageSchema

async def UpdateAccountVuaviaService(account_update: UpdateVuaviaSchema, db: AsyncSession) -> MessageSchema:
    try:
        # Kiểm tra xem tài khoản có tồn tại không
        result = await db.execute(select(AccountVuavia).where(AccountVuavia.id == account_update.id))
        account = result.scalar_one_or_none()
        if not account:
            raise HTTPException(status_code=404, detail="Account not found")
        
        # Kiểm tra login_name không trùng lặp (nếu thay đổi)
        if account.login_name != account_update.login_name:
            existing_result = await db.execute(
                select(AccountVuavia).where(
                    AccountVuavia.login_name == account_update.login_name,
                    AccountVuavia.id != account_update.id
                )
            )
            existing_account = existing_result.scalar_one_or_none()
            if existing_account:
                raise HTTPException(status_code=400, detail="Login name already exists")
        
        # Cập nhật tài khoản
        await db.execute(
            update(AccountVuavia)
            .where(AccountVuavia.id == account_update.id)
            .values(
                login_name=account_update.login_name,
                password=account_update.password
            )
        )
        await db.commit()
        
        return MessageSchema(message="Account updated successfully")
        
    except HTTPException as httpex:
        await db.rollback()
        raise httpex  
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))