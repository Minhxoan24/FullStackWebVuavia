from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from sqlalchemy import select
from app.models.AccountVuavia import AccountVuavia, StatusAccountVuavia
from app.models.TypeProduct import TypeProduct
from app.schemas.AccountVuaviaSchema.CreateVuavia import BulkCreateVuaviaSchema
from app.schemas.Message.Message import MessageSchema
from passlib.context import CryptContext
from datetime import datetime, timezone

# Tạo context cho hashing (bcrypt)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def BulkCreateAccountVuaviaService(bulk_accounts: BulkCreateVuaviaSchema, db: AsyncSession) -> MessageSchema:
    try:
        if not bulk_accounts.accounts:
            raise HTTPException(status_code=400, detail="No accounts provided")
            
        # 1. Lấy tất cả login_name từ request
        login_names = [acc.login_name for acc in bulk_accounts.accounts]
        
        # 2. Kiểm tra duplicate trong database một lần
        query = select(AccountVuavia.login_name).where(AccountVuavia.login_name.in_(login_names))
        result = await db.execute(query)
        existing_logins = {row[0] for row in result.fetchall()}
        
        # 3. Lọc accounts không duplicate 
        unique_accounts = []
        seen_names = set()
        for acc in bulk_accounts.accounts:
            if acc.login_name not in existing_logins and acc.login_name not in seen_names:
                unique_accounts.append(acc)
                seen_names.add(acc.login_name)
        
        if not unique_accounts:
            raise HTTPException(status_code=400, detail="All accounts already exist or duplicated in request")
        
        # 4. Kiểm tra type_product_id tồn tại
        type_ids = list(set(acc.type_product_id for acc in unique_accounts))
        type_check = await db.execute(select(TypeProduct.id).where(TypeProduct.id.in_(type_ids)))
        existing_types = {row[0] for row in type_check.fetchall()}
        
        # 5. Prepare data với validation
        valid_accounts_data = []
        for acc in unique_accounts:
            if acc.type_product_id in existing_types:
                # Hash password
                hashed_password = pwd_context.hash(acc.password)
                valid_accounts_data.append({
                    'login_name': acc.login_name,
                    'password': hashed_password,
                    'type_product_id': acc.type_product_id,
                    'status': StatusAccountVuavia.AVAILABLE,
                    'created_at': datetime.now(timezone.utc),
                    'updated_at': datetime.now(timezone.utc)
                })
        
        if not valid_accounts_data:
            raise HTTPException(status_code=404, detail="No valid type product IDs found")
        
        # 6. Bulk insert với batch
        batch_size = 100  # Tăng batch size cho hiệu suất
        created_count = 0
        
        for i in range(0, len(valid_accounts_data), batch_size):
            batch = valid_accounts_data[i:i + batch_size]
            
            # Sử dụng bulk_insert_mappings cho hiệu suất tối đa
            db.bulk_insert_mappings(AccountVuavia, batch)
            created_count += len(batch)
            await db.flush()
        
        await db.commit()
        
        skipped_count = len(bulk_accounts.accounts) - created_count
        message = f"Successfully created {created_count} accounts"
        if skipped_count > 0:
            message += f" (skipped {skipped_count} duplicates/invalid)"
            
        return MessageSchema(message=message)
        
    except HTTPException as httpex: 
        await db.rollback()
        raise httpex
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Bulk create failed: {str(e)}")
        existing_logins = {row[0] for row in result.fetchall()}
        
        # 3. Lọc accounts không duplicate
        new_accounts_data = []
        for acc in bulk_accounts.accounts:
            if acc.login_name not in existing_logins:
                # Kiểm tra type_product_id tồn tại
                type_check = await db.execute(select(TypeProduct).where(TypeProduct.id == acc.type_product_id))
                if not type_check.scalar_one_or_none():
                    raise HTTPException(status_code=404, detail=f"Type product ID {acc.type_product_id} not found")
                
                # Hash password và thêm vào list
                hashed_password = pwd_context.hash(acc.password)
                new_accounts_data.append({
                    'login_name': acc.login_name,
                    'password': hashed_password,
                    'type_product_id': acc.type_product_id,
                    'status': 'AVAILABLE'  # Default status
                })
        
        if not new_accounts_data:
            raise HTTPException(status_code=400, detail="All accounts already exist or invalid")
        
        # 4. Bulk insert với batch
        batch_size = 50
        for i in range(0, len(new_accounts_data), batch_size):
            batch = new_accounts_data[i:i + batch_size]
            db.bulk_insert_mappings(AccountVuavia, batch)
            await db.flush()
        
        await db.commit()
        
        return MessageSchema(message=f"Successfully created {len(new_accounts_data)} accounts")
        
    except HTTPException as httpex: 
        raise httpex
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
