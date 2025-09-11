from  sqlalchemy import select , func
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from app.models.Vouchers import Voucher
from app.models.Users import User
from app.models.VoucherUsage import VoucherUsage
from app.schemas.VoucherSchema.InforVoucher import VoucherResponseSchema

async def get_all_voucher_byAdmin(db: AsyncSession) -> list[VoucherResponseSchema]:
    try:
        result = await db.execute(select(Voucher))
        vouchers = result.scalars().all()
        return [VoucherResponseSchema.from_orm(voucher) for voucher in vouchers]
    except HTTPException as httpex:
        raise httpex
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting all vouchers: {str(e)}")