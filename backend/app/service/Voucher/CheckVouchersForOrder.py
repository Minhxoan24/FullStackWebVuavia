from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from datetime import datetime, timezone
from typing import List

from app.models.Vouchers import Voucher
from app.models.VoucherUsage import VoucherUsage
from app.models.TypeProduct import TypeProduct
from app.schemas.VoucherSchema.VoucherWithApplicabilitySchema import VoucherWithApplicabilitySchema
from app.schemas.Order.CheckVoucherRequest import CheckVoucherRequest

async def check_vouchers_for_order(
    request: CheckVoucherRequest, 
    user_id: int, 
    db: AsyncSession
) -> List[VoucherWithApplicabilitySchema]:
    """
    Kiểm tra tất cả voucher của user và xem voucher nào có thể áp dụng cho đơn hàng
    Trả về danh sách voucher với thông tin can_apply = True/False
    """
    try:
        # 1. Lấy thông tin sản phẩm và tính giá
        query_product = await db.execute(
            select(TypeProduct).where(TypeProduct.id == request.type_product_id)
        )
        type_product = query_product.scalar_one_or_none()
        if not type_product:
            raise HTTPException(status_code=404, detail="Type product not found")
        
        order_amount = type_product.price * request.quantity
        
        # 2. Lấy tất cả voucher active
        query_vouchers = select(Voucher).where(
            Voucher.status == "ACTIVE",
            Voucher.is_active == True,
            Voucher.expiration_date > datetime.now(timezone.utc)
        )
        result = await db.execute(query_vouchers)
        vouchers = result.scalars().all()
        
        voucher_list = []
        
        for voucher in vouchers:
            can_apply = True
            reason_cannot_apply = None
            discount_amount_preview = None
            total_after_discount_preview = None
            
            # 3. Kiểm tra các điều kiện áp dụng
            
            # 3.1. Kiểm tra giới hạn sử dụng tổng
            if voucher.usage_limit_total and voucher.used_count >= voucher.usage_limit_total:
                can_apply = False
                reason_cannot_apply = "Voucher đã hết lượt sử dụng"
            
            # 3.2. Kiểm tra giới hạn sử dụng per user
            if can_apply:
                usage_query = select(func.count(VoucherUsage.id)).where(
                    VoucherUsage.voucher_id == voucher.id,
                    VoucherUsage.user_id == user_id,
                    VoucherUsage.is_valid == True
                )
                usage_count = await db.scalar(usage_query)
                
                if voucher.usage_limit_per_user and usage_count >= voucher.usage_limit_per_user:
                    can_apply = False
                    reason_cannot_apply = "Bạn đã sử dụng hết lượt cho voucher này"
            
            # 3.3. Kiểm tra đơn hàng tối thiểu
            if can_apply and voucher.min_order_amount > order_amount:
                can_apply = False
                reason_cannot_apply = f"Đơn hàng tối thiểu {voucher.min_order_amount:,}đ"
            
            # 3.4. Kiểm tra loại voucher
            if can_apply and voucher.voucher_type == "PERSONAL":
                # Kiểm tra voucher có được assign cho user không
                assign_query = select(VoucherUsage).where(
                    VoucherUsage.voucher_id == voucher.id,
                    VoucherUsage.user_id == user_id
                )
                assign_result = await db.execute(assign_query)
                if not assign_result.scalar_one_or_none():
                    can_apply = False
                    reason_cannot_apply = "Voucher này không dành cho bạn"
            
            elif can_apply and voucher.voucher_type == "FIRST_TIME":
                # Kiểm tra user đã từng sử dụng voucher nào chưa
                first_time_query = select(func.count(VoucherUsage.id)).where(
                    VoucherUsage.user_id == user_id,
                    VoucherUsage.is_valid == True
                )
                total_usage = await db.scalar(first_time_query)
                if total_usage > 0:
                    can_apply = False
                    reason_cannot_apply = "Chỉ dành cho lần mua đầu tiên"
            
            # 4. Tính toán preview nếu có thể áp dụng
            if can_apply:
                if voucher.discount_type == "fixed":
                    discount_amount_preview = voucher.discount_value
                else:  # percentage
                    discount_amount_preview = min(
                        order_amount * voucher.discount_value / 100,
                        voucher.max_discount or float('inf')
                    )
                
                # Đảm bảo discount không vượt quá giá gốc
                discount_amount_preview = min(discount_amount_preview, order_amount)
                total_after_discount_preview = order_amount - discount_amount_preview
            
            # 5. Tạo response
            voucher_item = VoucherWithApplicabilitySchema(
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
                created_at=voucher.created_at,
                can_apply=can_apply,
                reason_cannot_apply=reason_cannot_apply,
                discount_amount_preview=int(discount_amount_preview) if discount_amount_preview else None,
                total_after_discount_preview=int(total_after_discount_preview) if total_after_discount_preview else None
            )
            
            voucher_list.append(voucher_item)
        
        # Sắp xếp: voucher có thể áp dụng lên đầu
        voucher_list.sort(key=lambda x: (not x.can_apply, -x.discount_amount_preview if x.discount_amount_preview else 0))
        
        return voucher_list
        
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error checking vouchers: {str(e)}")
