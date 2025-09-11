from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.DataBase import get_async_session
from app.core.auth import get_current_user
from app.models.Users import User
from app.schemas.AccountSchema.AccountRegisterSchema import CreateUserRegisterSchema , ResponseRegisterSchema
from app.schemas.AccountSchema.AccountInformationSchema import InformationAccountSchema 
from app.schemas.AccountSchema.AccountLoginSchema import LoginReponseSchema  , LoginUserSchema
from app.schemas.AccountSchema.AccountUpdateSchema import AccountUpdateSchema, MessegeUpdateSchema
from app.schemas.AccountSchema.ChangePassword import ChangePasswordSchema , ChangePasswordResponse


from app.service.AccountService.AccountRegisterService import RegisterAccountService
from app.service.AccountService.AccountInformationService import GetAccountInformationService
from app.service.AccountService.AccountLoginService import LoginAccountService
from app.service.AccountService.AccountUpdateService import UpdateAccountInformationService 
from app.service.AccountService.ChangePasswordService import ChangePasswordService
router = APIRouter(tags=["Account"] , prefix="/Account")

@router.post("/register" , response_model=ResponseRegisterSchema)
async def register_account(new_account: CreateUserRegisterSchema, db: AsyncSession = Depends(get_async_session)):
    """
    Endpoint đăng ký tài khoản người dùng mới
    """
    return await RegisterAccountService(new_account, db)
@router.post("/login", response_model=LoginReponseSchema)
async def login_account(login_user: LoginUserSchema, db: AsyncSession = Depends(get_async_session)):
    """
    Endpoint đăng nhập tài khoản người dùng
    """
    return await LoginAccountService(login_user, db)

@router.get("/information", response_model=InformationAccountSchema)
async def get_account_information(user: User = Depends(get_current_user)):

    return await GetAccountInformationService(user)
@router.put("/update", response_model=MessegeUpdateSchema)
async def update_account_information(data: AccountUpdateSchema, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_async_session)):
    """
    Endpoint cập nhật thông tin tài khoản người dùng
    """
    return await UpdateAccountInformationService(data , user, db)
@router.put("/change-password", response_model=ChangePasswordResponse)
async def change_password(
    data: ChangePasswordSchema, 
    user: User = Depends(get_current_user), 
    db: AsyncSession = Depends(get_async_session)
):
    """Endpoint thay đổi mật khẩu người dùng"""
    return await ChangePasswordService(data, user, db)
@router.post("/refresh", response_model=LoginReponseSchema)
async def refresh_access_token(
    user: User = Depends(get_current_user), 
    db: AsyncSession = Depends(get_async_session)
):
    """Endpoint làm mới access token"""
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    # Sửa: dùng accountname thay vì username
    login_data = LoginUserSchema(
        accountname=user.accountname, 
        password=""  # Không cần password khi refresh
    )
    return await LoginAccountService(login_data, db)
