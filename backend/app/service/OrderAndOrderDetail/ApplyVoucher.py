from sqlalchemy import select, func
from fastapi import HTTPException
from datetime import datetime, timezone
from app.models.Vouchers import Voucher
from app.models.VoucherUsage import VoucherUsage
from app.schemas.Order.ApplyVoucher import ApplyVoucherRequest, ApplyVoucherResponse
from  app.service.RedisService.RedisService import redis_service
from sqlalchemy.ext.asyncio import AsyncSession

async def apply_voucher(request: ApplyVoucherRequest, user_id: int, db: AsyncSession) -> ApplyVoucherResponse:
    try:
        # Tìm voucher theo mã
        voucher = await db.scalar(select(Voucher).where(Voucher.code == request.voucher_code))
        if not voucher:
            raise HTTPException(status_code=404, detail="Voucher not found")

        # Kiểm tra tính hợp lệ
        now = datetime.now(timezone.utc)
        if voucher.expiry_date < now:
            raise HTTPException(status_code=400, detail="Voucher has expired")
        if voucher.min_order_amount and request.cart_amount < voucher.min_order_amount:
            raise HTTPException(status_code=400, detail=f"Minimum order amount is {voucher.min_order_amount}")
        if voucher.status != "ACTIVE" or not voucher.is_active:
            raise HTTPException(status_code=400, detail="Voucher is not active")

        # Kiểm tra số lần sử dụng
        usage_query = select(func.count(VoucherUsage.id)).where(
            VoucherUsage.voucher_id == voucher.id,
            VoucherUsage.user_id == user_id,
            VoucherUsage.is_valid == True
        )
        usage_count = await db.scalar(usage_query)
        if voucher.usage_limit_per_user and usage_count >= voucher.usage_limit_per_user:
            raise HTTPException(status_code=400, detail="User exceeded voucher usage limit")
        if voucher.usage_limit_total and voucher.used_count >= voucher.usage_limit_total:
            raise HTTPException(status_code=400, detail="Voucher usage limit reached")

        # Kiểm tra voucher_type
        if voucher.voucher_type == "PERSONAL":
            assign_query = select(VoucherUsage).where(
                VoucherUsage.voucher_id == voucher.id,
                VoucherUsage.user_id == user_id
            )
            if not (await db.execute(assign_query)).scalar_one_or_none():
                raise HTTPException(status_code=400, detail="Voucher not assigned to this user")
        elif voucher.voucher_type == "FIRST_TIME" and usage_count > 0:
            raise HTTPException(status_code=400, detail="Voucher only for first-time use")
        elif voucher.voucher_type == "CATEGORY" and request.category_id:
            pass  # Giả định kiểm tra category_id

        # Tính toán giảm giá
        discount_amount = voucher.discount_value if voucher.discount_type == "fixed" else \
                         min(request.cart_amount * voucher.discount_value / 100, voucher.max_discount or float('inf'))
        total_after_discount = max(request.cart_amount - discount_amount, 0)

        # Lưu vào Redis
        cache_data = {
            "voucher_id": voucher.id,
            "code": voucher.code,
            "discount_amount": int(discount_amount),
            "total_after_discount": int(total_after_discount)
        }
        await redis_service.set_voucher_cache(user_id, cache_data)

        return ApplyVoucherResponse(
            voucher_id=voucher.id,
            code=voucher.code,
            discount_amount=int(discount_amount),
            total_after_discount=int(total_after_discount)
        )
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")