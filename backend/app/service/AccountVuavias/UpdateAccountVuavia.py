from fastapi import HTTPException 
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from app.models.AccountVuavia import AccountVuavia
from app.models.TypeProduct import TypeProduct  # Thêm import
from app.schemas.AccountVuaviaSchema.UpdateVuavia import UpdateVuaviaSchema
from app.schemas.Message.Message import MessageSchema
from passlib.context import CryptContext  # Thêm import cho hashing

# Tạo context cho hashing (bcrypt)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def UpdateAccountVuaviaService(account_id: int, account_update: UpdateVuaviaSchema, db: AsyncSession) -> MessageSchema:
    try:
        # Lấy account theo account_id từ path
        result = await db.execute(select(AccountVuavia).where(AccountVuavia.id == account_id))
        account = result.scalar_one_or_none()
        if not account:
            raise HTTPException(status_code=404, detail="Account not found")
        
        # Chỉ update fields được cung cấp
        update_data = {}
        if account_update.login_name is not None:
            # Kiểm tra duplicate nếu login_name thay đổi
            if account.login_name != account_update.login_name:
                existing_result = await db.execute(
                    select(AccountVuavia).where(
                        AccountVuavia.login_name == account_update.login_name,
                        AccountVuavia.id != account_id
                    )
                )
                if existing_result.scalar_one_or_none():
                    raise HTTPException(status_code=400, detail="Login name already exists")
            update_data['login_name'] = account_update.login_name
        
        if account_update.password is not None:
            # Hash password trước khi update
            hashed_password = pwd_context.hash(account_update.password)
            update_data['password'] = hashed_password
        
        if account_update.type_product_id is not None:
            # Kiểm tra type_product tồn tại
            type_result = await db.execute(select(TypeProduct).where(TypeProduct.id == account_update.type_product_id))
            if not type_result.scalar_one_or_none():
                raise HTTPException(status_code=404, detail="Type product not found")
            update_data['type_product_id'] = account_update.type_product_id
        
        if update_data:
            await db.execute(
                update(AccountVuavia)
                .where(AccountVuavia.id == account_id)
                .values(**update_data)
            )
            await db.commit()

        return MessageSchema(
            status="success",
            message="Account updated successfully"
        )

    except HTTPException as httpex:
        await db.rollback()
        raise httpex  
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))