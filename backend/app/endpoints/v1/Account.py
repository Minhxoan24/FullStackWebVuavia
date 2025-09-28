from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.sql import select

from app.db.DataBase import get_async_session
from app.core.auth import get_current_user
from app.models.Users import User
from app.schemas.AccountSchema.AccountRegisterSchema import CreateUserRegisterSchema , ResponseRegisterSchema
from app.schemas.AccountSchema.AccountInformationSchema import InformationAccountSchema 
from app.schemas.AccountSchema.AccountLoginSchema import LoginReponseSchema  , LoginUserSchema
from app.schemas.AccountSchema.AccountUpdateSchema import AccountUpdateSchema, MessegeUpdateSchema
from app.schemas.AccountSchema.ChangePassword import ChangePasswordSchema , ChangePasswordResponse
from app.schemas.Message.Message import MessageSchema


from app.service.AccountService.AccountRegisterService import RegisterAccountService
from app.service.AccountService.AccountInformationService import GetAccountInformationService
from app.service.AccountService.AccountLoginService import LoginAccountService
from app.service.AccountService.AccountUpdateService import UpdateAccountInformationService 
from app.service.AccountService.ChangePasswordService import ChangePasswordService
from app.service.CloudinaryService.CloudinaryService import update_user_avatar_service

# Forgot password imports
from app.schemas.ForgotPasswordSchema.ForgotPasswordSchema import (
    RequestOTPBody, VerifyOTPBody, ResetPasswordBody,
    OTPStatusResponse, ResetPasswordResponse
)
from app.service.ForgotPasswordService.ForgotPasswordService import (
    request_password_reset_otp,
    verify_password_reset_otp,
    reset_password_with_otp
)
from app.schemas.AccountSchema.RefreshSchema import RefreshTokenRequest, RefreshTokenResponse
from app.core.JWT import verify_refresh_token, create_full_token

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
    refresh_request: RefreshTokenRequest,
    db: AsyncSession = Depends(get_async_session)
):
    """Endpoint làm mới access token"""
    try:
        payload = verify_refresh_token(refresh_request.refresh_token)
        user_id = payload.get("id")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid refresh token")
        
        # Query user
        query = select(User).options(selectinload(User.roles)).where(User.id == user_id)
        result = await db.execute(query)
        user = result.scalar_one_or_none()
        
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        
        # Get roles
        roles = [role.name.value for role in user.roles] if user.roles else ["USER"]
        
        # Create new tokens
        token = create_full_token({
            "id": user.id,
            "roles": roles,
            "accountname": user.accountname
        })
        
        return LoginReponseSchema(
            access_token=token["access_token"],
            refresh_token=token["refresh_token"],
            token_type="bearer"
        )
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")

# ===== Forgot Password endpoints (moved under Account) =====
@router.post("/forgot-password/request-otp", response_model=OTPStatusResponse)
async def request_otp(body: RequestOTPBody, db: AsyncSession = Depends(get_async_session)):
    res = await request_password_reset_otp(body.email, db)
    # Service may return a pydantic model instance or a dict
    if hasattr(res, "dict"):
        return res
    return OTPStatusResponse(**res)

@router.post("/forgot-password/verify-otp", response_model=OTPStatusResponse)
async def verify_otp(body: VerifyOTPBody):
    res = await verify_password_reset_otp(body.email, body.otp)
    if hasattr(res, "dict"):
        return res
    return OTPStatusResponse(**res)

@router.post("/forgot-password/reset", response_model=ResetPasswordResponse)
async def reset_password(body: ResetPasswordBody, db: AsyncSession = Depends(get_async_session)):
    res = await reset_password_with_otp(body.email, body.otp, body.new_password, db)
    if hasattr(res, "dict"):
        return res
    return ResetPasswordResponse(**res)
@router.post("/avatar", response_model=MessageSchema)
async def update_avatar(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(get_current_user),
):
    """
    Upload avatar image to Cloudinary, update user record and return message.
    Service handles validation, upload and error handling (raises HTTPException on error).
    """
    new_url = await update_user_avatar_service(db, user.id, file)
    return MessageSchema(status="success", message="Ảnh đại diện đã được cập nhật.")
