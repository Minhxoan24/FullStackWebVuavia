from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.DataBase import get_async_session
from app.core.auth import get_current_user
from app.core.author import get_current_admin_user
from app.models.Users import User

# Schema imports
from app.schemas.AccountVuaviaSchema.CreateVuavia import CreateVuaviaSchema
from app.schemas.AccountVuaviaSchema.UpdateVuavia import UpdateVuaviaSchema
from app.schemas.AccountVuaviaSchema.DeleteVuavia import DeleteVuaviaSchema
from app.schemas.AccountVuaviaSchema.InforAccountVuaviaSchema import InforAccountVuaviaSchema
from app.schemas.Message.Message import MessageSchema

# Service imports
from app.service.AccountVuavias.CreatAccountVuavia import CreateAccountVuaviaService
from app.service.AccountVuavias.UpdateAccountVuavia import UpdateAccountVuaviaService
from app.service.AccountVuavias.DeleteAccountVuavia import DeleteAccountVuaviaService
from app.service.AccountVuavias.InformationAccountVuavia import InformationAccountVuaviaService
from app.service.AccountVuavias.CountAccount import CountAccountVuaviaService

router = APIRouter(tags=["AccountVuavia"], prefix="/account-vuavia")

@router.post("/create", response_model=MessageSchema)
async def create_account_vuavia(
    account_vuavia: CreateVuaviaSchema,
    db: AsyncSession = Depends(get_async_session),
    admin_user: User = Depends(get_current_admin_user)  # Chỉ admin mới được thêm
):
    """Thêm tài khoản mới vào kho tài khoản Vuavia"""
    return await CreateAccountVuaviaService(account_vuavia, db)

@router.get("/list", response_model=list[InforAccountVuaviaSchema])
async def list_account_vuavia(
    db: AsyncSession = Depends(get_async_session),
    admin_user: User = Depends(get_current_admin_user)
):
    """Lấy danh sách tất cả tài khoản trong kho"""
    return await InformationAccountVuaviaService(db)

@router.get("/count")
async def count_account_vuavia(
    db: AsyncSession = Depends(get_async_session),
    admin_user: User = Depends(get_current_admin_user)
):
    """Đếm số lượng tài khoản trong kho"""
    return await CountAccountVuaviaService(db)



@router.put("/update", response_model=MessageSchema)
async def update_account_vuavia(
    account_update: UpdateVuaviaSchema,
    db: AsyncSession = Depends(get_async_session),
    admin_user: User = Depends(get_current_admin_user)
):
    """Cập nhật thông tin tài khoản trong kho"""
    return await UpdateAccountVuaviaService(account_update, db)

@router.delete("/delete", response_model=MessageSchema)
async def delete_account_vuavia(
    account_delete: DeleteVuaviaSchema,
    db: AsyncSession = Depends(get_async_session),
    admin_user: User = Depends(get_current_admin_user)
):
    """Xóa tài khoản khỏi kho"""
    return await DeleteAccountVuaviaService(account_delete, db)