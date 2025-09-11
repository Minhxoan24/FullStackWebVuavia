from  sqlalchemy import select , func
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from app.models.Vouchers import Voucher
from app.models.VoucherUsage import VoucherUsage
from app.models.Users import User
from datetime import datetime, timezone
from app.schemas.VoucherSchema.InforVoucher import VoucherResponseSchema

async def get_user_vouchers(db: AsyncSession, user_id: int) -> list[VoucherResponseSchema]:
        """Lấy tất cả voucher khả dụng của người dùng"""
        # Query tất cả voucher đang hoạt động
        query = select(Voucher).where(
            Voucher.status == "ACTIVE",
            Voucher.is_active == True,
            Voucher.expiration_date > datetime.now(timezone.utc)
        )
        result = await db.execute(query)
        vouchers = result.scalars().all()

        user_vouchers = []
        for voucher in vouchers:
            # Kiểm tra giới hạn sử dụng tổng
            if voucher.used_count >= voucher.usage_limit_total and voucher.usage_limit_total is not None:
                continue

            # Kiểm tra giới hạn sử dụng mỗi người dùng
            usage_query = select(VoucherUsage).where(
                VoucherUsage.voucher_id == voucher.id,
                VoucherUsage.user_id == user_id,
                VoucherUsage.is_valid == True
            )
            usage_result = await db.execute(usage_query)
            usage_count = len(usage_result.scalars().all())

            if usage_count >= voucher.usage_limit_per_user:
                continue

            # Kiểm tra điều kiện theo loại voucher
            include_voucher = False
            if voucher.voucher_type == "PUBLIC":
                include_voucher = True
            elif voucher.voucher_type == "PERSONAL":
                # Kiểm tra xem voucher có được gán cho user không
                assign_query = select(VoucherUsage).where(
                    VoucherUsage.voucher_id == voucher.id,
                    VoucherUsage.user_id == user_id
                )
                assign_result = await db.execute(assign_query)
                if assign_result.scalar_one_or_none():
                    include_voucher = True
            elif voucher.voucher_type == "FIRST_TIME" and usage_count == 0:
                include_voucher = True
            elif voucher.voucher_type == "CATEGORY":
                # Giả sử có logic kiểm tra danh mục, ví dụ: liên kết với order_details
                include_voucher = True  # Cần điều chỉnh nếu có bảng danh mục

            if include_voucher:
                user_vouchers.append(VoucherResponseSchema(
                    id=voucher.id,
                    code=voucher.code,
                    name=voucher.name,
                    description=voucher.description,
                    discount_type=voucher.discount_type,
                    discount_value=voucher.discount_value,
                    max_discount=voucher.max_discount,
                    min_order_amount=voucher.min_order_amount,
                    voucher_type=voucher.voucher_type,
                    start_date=voucher.start_date,
                    expiration_date=voucher.expiration_date,
                    usage_limit_total=voucher.usage_limit_total,
                    usage_limit_per_user=voucher.usage_limit_per_user,
                    used_count=voucher.used_count,
                    status=voucher.status,
                    is_active=voucher.is_active,
                    created_at=voucher.created_at
                ))

        return user_vouchers