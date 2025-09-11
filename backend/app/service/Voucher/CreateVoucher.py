from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException
from datetime import datetime, timezone
from app.models.Vouchers import Voucher
from app.schemas.VoucherSchema.CreateVoucher import CreateVoucherRequest, CreateVoucherResponse


async def create_voucher(db: AsyncSession, request: CreateVoucherRequest) -> CreateVoucherResponse:
        # Kiểm tra mã voucher tồn tại
        existing = await db.scalar(select(Voucher).where(Voucher.code == request.code))
        if existing:
            raise HTTPException(status_code=400, detail="Voucher code already exists")

        now = datetime.now(timezone.utc)
        voucher = Voucher(
            code=request.code,
            name=request.name,
            description=request.description,
            discount_type=request.discount_type,
            discount_value=request.discount_value,
            max_discount=request.max_discount,
            min_order_amount=request.min_order_amount,
            voucher_type=request.voucher_type,
            start_date=request.start_date,
            expiration_date=request.expiration_date,
            usage_limit_total=request.usage_limit_total,
            usage_limit_per_user=request.usage_limit_per_user,
            used_count=0,
            status="ACTIVE" if request.is_active else "INACTIVE",
            is_active=request.is_active,
            created_at=now,
            updated_at=now
        )

        db.add(voucher)
        try:
            await db.commit()
            await db.refresh(voucher)
        except Exception as e:
            await db.rollback()
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

        return CreateVoucherResponse.model_validate(voucher)
