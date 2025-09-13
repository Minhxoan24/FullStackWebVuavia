from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from sqlalchemy import select
from app.models.AccountVuavia import AccountVuavia
from app.schemas.AccountVuaviaSchema.CreateVuavia import CreateVuaviaSchema
from app.schemas.Message.Message import MessageSchema
from app.models.TypeProduct import TypeProduct  # Thêm import
from passlib.context import CryptContext  # Thêm import cho hashing

# Tạo context cho hashing (bcrypt)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def CreateAccountVuaviaService(account_vuavia: CreateVuaviaSchema, db: AsyncSession) -> MessageSchema:
    try: 
        query = await db.execute(select(AccountVuavia).where(AccountVuavia.login_name == account_vuavia.login_name))
        existing_account = query.scalar_one_or_none()
        
        if existing_account is not None:
            raise HTTPException(status_code=400, detail="Account with this login name already exists")
        
        # Kiểm tra type_product_id tồn tại
        type_product_query = await db.execute(select(TypeProduct).where(TypeProduct.id == account_vuavia.type_product_id))
        type_product = type_product_query.scalar_one_or_none()
        if not type_product:
            raise HTTPException(status_code=404, detail="Type product not found")
        
        # Hash password trước khi lưu
        hashed_password = pwd_context.hash(account_vuavia.password)
        
        # Tạo account với password đã hash
        new_account = AccountVuavia(
            login_name=account_vuavia.login_name,
            password=hashed_password,  # Lưu hashed thay vì plain
            type_product_id=account_vuavia.type_product_id
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

