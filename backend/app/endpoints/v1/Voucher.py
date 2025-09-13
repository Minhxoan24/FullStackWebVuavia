from app.db.DataBase import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException
import logging

from app.core.author import get_current_admin_user
from app.core.auth import get_current_user
from app.models.Users import User
from app.models.Vouchers import Voucher
from app.models.VoucherUsage import VoucherUsage

# Schema imports
from app.schemas.VoucherSchema.CreateVoucher import CreateVoucherRequest
from app.schemas.VoucherSchema.InforVoucher import VoucherResponseSchema
from app.schemas.VoucherSchema.DeleteVoucher import DeleteVoucher
from app.schemas.VoucherSchema.AvailableVoucher import AvailableVouchersRequest
from app.schemas.Message.Message import MessageSchema 

# Service imports
from app.service.Voucher.CreateVoucher import create_voucher
from app.service.Voucher.AvailableVouchers import get_available_vouchers
from app.service.Voucher.MyVoucher import get_user_vouchers  # Sửa import
from app.service.Voucher.DeleteVoucher import delete_voucher
from app.service.Voucher.GetAllVoucherAdmin import get_all_voucher_byAdmin  # Sửa import

# ✅ THÊM: Setup logging
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/voucher", tags=["Voucher"])

@router.post("/create-voucher-admin", response_model=MessageSchema)
async def create_voucher_admin( 
    voucher_new: CreateVoucherRequest,
    db: AsyncSession = Depends(get_async_session),
    admin_user: User = Depends(get_current_admin_user)  
):
    return await create_voucher(db, voucher_new)

@router.get("/all-voucher-admin", response_model=list[VoucherResponseSchema])
async def get_all_voucher_admin( 
    db: AsyncSession = Depends(get_async_session),
    admin_user: User = Depends(get_current_admin_user)  
):
    return await get_all_voucher_byAdmin(db)  # Sửa function call

@router.post("/delete-voucher-admin", response_model=MessageSchema)
async def delete_voucher_admin(
    voucher_delete: DeleteVoucher,
    db: AsyncSession = Depends(get_async_session),
    admin_user: User = Depends(get_current_admin_user)
):
    # Sửa function call để khớp với service signature
    return await delete_voucher(db, voucher_delete.id)

@router.get("/my-vouchers", response_model=list[VoucherResponseSchema]) 
async def get_my_voucher(
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user)
):
    return await get_user_vouchers(db, current_user.id)  # Sửa function call

@router.get("/available-vouchers", response_model=list[VoucherResponseSchema])
async def get_available_vouchers(
    available_vouchers_request: AvailableVouchersRequest,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user)
):
    return await get_available_vouchers(db, current_user.id, available_vouchers_request)