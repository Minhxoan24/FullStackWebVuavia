from sqlalchemy import select
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timezone
from app.schemas.Order.CreateOrderSchema import CreateOrderSchema
from app.models.TypeProduct import TypeProduct
from app.models.Orders import Order, OrderStatus
from app.models.AccountVuavia import AccountVuavia, StatusAccountVuavia
from app.models.Vouchers import Voucher
from app.models.OrderDetail import OrderDetail
from app.schemas.Message.Message import MessageSchema
from app.service.AccountVuavias.CountAccount import CountAccountVuaviaService
from app.service.AccountVuavias.SelectAccount import SelectAccountVuaviaService
from app.models.VoucherUsage import VoucherUsage
from app.models.Users import User
from app.service.RedisService.RedisService import redis_service
from app.models.TransactionHistory import TransactionType
from app.models.TransactionHistory import TransactionHistory

async def CreateOrderService(
    new_order: CreateOrderSchema,
    db: AsyncSession,
    user_id: int,
) -> MessageSchema:
    """
    Service tạo order trực tiếp - KHÔNG qua giỏ hàng
    Flow: User chọn sản phẩm + số lượng → Mua ngay
    """
    try:
        # 1. Lấy user
        query_user = await db.execute(select(User).where(User.id == user_id))
        user = query_user.scalar_one_or_none()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # 2. Kiểm tra type_product và lấy giá
        query_product = await db.execute(select(TypeProduct).where(TypeProduct.id == new_order.type_product_id))
        type_product = query_product.scalar_one_or_none()
        if not type_product:
            raise HTTPException(status_code=404, detail="Type product not found")

        # 3. Tính giá gốc (từ DB, không từ client)
        original_price = type_product.price * new_order.quantity

        # 4. Kiểm tra số lượng tài khoản available
        count_account = await CountAccountVuaviaService(new_order.type_product_id, db)
        if new_order.quantity > count_account:
            raise HTTPException(status_code=400, detail=f"Not enough accounts. Available: {count_account}")

        # 5. Xử lý voucher (nếu có)
        discount_amount = 0
        voucher = None
        if new_order.voucher_id:
            # Kiểm tra voucher từ cache Redis
            cached_voucher = await redis_service.get_voucher_cache(user_id)
            if not cached_voucher or cached_voucher.get("voucher_id") != new_order.voucher_id:
                raise HTTPException(status_code=400, detail="Voucher not applied or expired")

            # Validate voucher từ DB
            query_voucher = await db.execute(select(Voucher).where(Voucher.id == new_order.voucher_id))
            voucher = query_voucher.scalar_one_or_none()
            if not voucher:
                raise HTTPException(status_code=400, detail="Voucher not found")

            # Validate voucher rules
            if (voucher.status != "ACTIVE" or not voucher.is_active or
                voucher.expiry_date <= datetime.now(timezone.utc) or
                voucher.min_order_amount > original_price):
                raise HTTPException(status_code=400, detail="Voucher not valid")

            # Tính discount
            if voucher.discount_type == "fixed":
                discount_amount = voucher.discount_value
            else:  # percentage
                discount_amount = min(
                    original_price * voucher.discount_value / 100,
                    voucher.max_discount or float('inf')
                )
            
            # Đảm bảo discount không vượt quá giá gốc
            discount_amount = min(discount_amount, original_price)

        # 6. Tính tổng tiền phải trả
        total_amount = original_price - discount_amount
        
        # 7. Kiểm tra số dư
        if user.balance < total_amount:
            raise HTTPException(status_code=400, detail=f"Insufficient balance. Required: {total_amount}, Available: {user.balance}")

        # 8. Lấy accounts (với pessimistic locking)
        list_account = await SelectAccountVuaviaService(new_order.quantity, new_order.type_product_id, db)
        if len(list_account) < new_order.quantity:
            raise HTTPException(status_code=404, detail="Not enough available accounts")

        # 9. Tạo OrderDetail
        order_detail = OrderDetail(
            type_product_id=new_order.type_product_id,
            quantity=new_order.quantity,
            total_amount=original_price,  # Giá gốc (trước discount)
            accounts_info=[
                {
                    "id": account.id,
                    "login_name": account.login_name,
                    "password": account.password  # Lưu password để deliver cho customer
                }
                for account in list_account
            ],
        )
        db.add(order_detail)
        await db.flush()

        # 10. Tạo Order
        order = Order(
            user_id=user_id,
            quantity=new_order.quantity,
            total_amount=total_amount,  # Giá sau discount
            order_detail_id=order_detail.id,
            status=OrderStatus.COMPLETED,
            time=datetime.now(timezone.utc)
        )
        db.add(order)
        await db.flush()

        # 11. Tạo VoucherUsage (nếu có voucher)
        if voucher:
            voucher_usage = VoucherUsage(
                voucher_id=voucher.id,
                user_id=user_id,
                order_id=order.id,
                discount_amount=discount_amount,
                used_at=datetime.now(timezone.utc),
                is_valid=True
            )
            db.add(voucher_usage)

            # Cập nhật Voucher usage count
            voucher.used_count += 1
            if voucher.usage_limit_total and voucher.used_count >= voucher.usage_limit_total:
                voucher.status = "INACTIVE"
                voucher.is_active = False

        # 12. Cập nhật trạng thái accounts
        for account in list_account:
            account.status = StatusAccountVuavia.SOLD
            account.orderdetail_id = order_detail.id

        # 13. Trừ tiền user
        user.balance -= total_amount

        # 14. Ghi transaction history
        transaction = TransactionHistory(
            user_id=user_id,
            type=TransactionType.PURCHASE,
            amount=-total_amount,
            description=f"Mua {new_order.quantity} account {type_product.name}",
            order_id=order.id,
            created_at=datetime.now(timezone.utc)
        )
        db.add(transaction)

        # 15. Xóa voucher cache
        if new_order.voucher_id:
            await redis_service.delete_voucher_cache(user_id)

        # 16. Commit tất cả
        await db.commit()
        
        return MessageSchema(message=f"Order completed! You received {new_order.quantity} accounts.")

    except HTTPException as http_ex:
        await db.rollback()
        raise http_ex
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")