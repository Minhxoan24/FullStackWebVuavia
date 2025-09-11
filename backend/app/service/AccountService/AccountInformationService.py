from fastapi import HTTPException, Depends
from app.models.Users import User
from app.schemas.AccountSchema.AccountInformationSchema import InformationAccountSchema
from app.core.auth import get_current_user 

async def GetAccountInformationService(infor_user: User = Depends(get_current_user)):
    try:
        user = InformationAccountSchema(
            name=infor_user.name,
            surname=infor_user.surname,
            accountname=infor_user.accountname,
            email=infor_user.email,
            avatar=infor_user.avatar,
            phone=infor_user.phone,
            balance=infor_user.balance
        )
        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting user information: {str(e)}")  