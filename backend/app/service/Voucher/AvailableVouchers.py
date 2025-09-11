from  sqlalchemy import select , func
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from app.models.Vouchers import Voucher
from app.models.Users import User
from app.models.VoucherUsage import VoucherUsage
from app.models.Category import Category
from app.schemas.VoucherSchema.InforVoucher import VoucherResponseSchema
from datetime import datetime, timezone
from app.schemas.VoucherSchema.AvailableVoucher import AvailableVouchersRequest 
from app.service.Voucher.MyVoucher import get_user_vouchers 


async def get_available_vouchers(db: AsyncSession,user_id : int ,  AvailableVouchersRequest: AvailableVouchersRequest) -> list[VoucherResponseSchema]:
    try: 
        """Lấy tất cả voucher khả dụng dựa trên yêu cầu"""
        all_voucher_user = await get_user_vouchers(db, user_id)
        if all_voucher_user is None:
            raise HTTPException(status_code=404, detail="User not found or no vouchers available")
        available_vouchers = []
        for voucher in all_voucher_user:
            if AvailableVouchersRequest.order_amount >= voucher.min_order_amount:
                available_vouchers.append(voucher)
        
        return available_vouchers
    except HTTPException as httpex:
        raise httpex
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting available vouchers: {str(e)}")