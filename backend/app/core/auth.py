from fastapi import Depends, HTTPException 
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from .JWT import verify_access_token
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.sql import select
from app.models.Users import User
from jose import jwt, JWTError, ExpiredSignatureError
from app.db.DataBase import get_async_session

security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: AsyncSession = Depends(get_async_session)):
    """
    Lấy thông tin người dùng hiện tại từ token
    """
    token = credentials.credentials
    if not token:
        raise HTTPException(status_code=401, detail="Token is missing")
    try:
        payload = verify_access_token(token)  # Giải mã token
        user_id = payload.get("id")  # Lấy ID người dùng từ payload
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        # Truy vấn người dùng từ cơ sở dữ liệu với eager loading roles
        query = select(User).options(selectinload(User.roles)).where(User.id == user_id)
        result = await db.execute(query)
        user = result.scalar_one_or_none()
        
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        
        return user
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    except HTTPException as httpex:
        
        raise httpex
    except Exception as e:

        raise HTTPException(status_code=500, detail=f"Error getting current user: {str(e)}")