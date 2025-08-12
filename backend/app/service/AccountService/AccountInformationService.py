from fastapi import HTTPException
from app.models.Users import User
from app.schemas.AccountSchema.AccountInformationSchema import InformationAccountSchema

async def GetAccountInformationService(user: User):
    """
    Service lấy thông tin tài khoản người dùng
    """
    try:
        return InformationAccountSchema.model_validate(user)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting account information: {str(e)}")
