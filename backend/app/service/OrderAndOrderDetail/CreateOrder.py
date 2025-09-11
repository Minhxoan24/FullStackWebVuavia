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
    try:
        # Lấy user
        query_user = await db.execute(select(User).where(User.id == user_id))
        user = query_user.scalar_one_or_none()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Kiểm tra type_product
        query_product = await db.execute(select(TypeProduct).where(TypeProduct.id == new_order.type_product_id))
        type_product = query_product.scalar_one_or_none()
        if not type_product:
            raise HTTPException(status_code=404, detail="Type product not found")

        # Kiểm tra giá
        if new_order.price != type_product.price * new_order.quantity:
            raise HTTPException(status_code=400, detail="Invalid price")

        # Kiểm tra số lượng tài khoản
        count_account = await CountAccountVuaviaService(new_order.type_product_id, db)
        if new_order.quantity > count_account:
            raise HTTPException(status_code=400, detail="Not enough accounts in stock")

        # Kiểm tra voucher (nếu có)
        discount_amount = new_order.discount_amount or 0
        if new_order.voucher_id:
            # Lấy từ Redis
            cached_voucher = await redis_service.get_voucher_cache(user_id)
            if not cached_voucher:
                raise HTTPException(status_code=400, detail="No voucher applied")

            if cached_voucher["voucher_id"] != new_order.voucher_id or cached_voucher["discount_amount"] != new_order.discount_amount:
                raise HTTPException(status_code=400, detail="Voucher mismatch")

            # Kiểm tra lại voucher
            query_voucher = await db.execute(select(Voucher).where(Voucher.id == new_order.voucher_id))
            voucher = query_voucher.scalar_one_or_none()
            if not voucher:
                raise HTTPException(status_code=400, detail="Voucher not found")

            if (voucher.status != "ACTIVE" or not voucher.is_active or
                voucher.expiry_date <= datetime.now(timezone.utc) or
                voucher.min_order_amount > new_order.price):
                raise HTTPException(status_code=400, detail="Voucher not valid")

            # Kiểm tra giới hạn sử dụng
            usage_query = select(VoucherUsage).where(
                VoucherUsage.voucher_id == voucher.id,
                VoucherUsage.user_id == user_id,
                VoucherUsage.is_valid == True
            )
            usage_count = len((await db.execute(usage_query)).scalars().all())
            if voucher.usage_limit_per_user and usage_count >= voucher.usage_limit_per_user:
                raise HTTPException(status_code=400, detail="User exceeded voucher usage limit")
            if voucher.usage_limit_total and voucher.used_count >= voucher.usage_limit_total:
                raise HTTPException(status_code=400, detail="Voucher usage limit reached")

            # Tính lại discount_amount
            calculated_discount = voucher.discount_value if voucher.discount_type == "fixed" else \
                                 min(new_order.price * voucher.discount_value / 100, voucher.max_discount or float('inf'))
            if calculated_discount != new_order.discount_amount:
                raise HTTPException(status_code=400, detail="Invalid discount amount")

        # Kiểm tra số dư
        total_amount = new_order.price - discount_amount
        if user.balance < total_amount:
            raise HTTPException(status_code=400, detail="Insufficient balance")

        # Lấy danh sách tài khoản
        list_account = await SelectAccountVuaviaService(new_order.quantity, new_order.type_product_id, db)
        if not list_account:
            raise HTTPException(status_code=404, detail="No available accounts found")

        # Tạo OrderDetail
        order_detail = OrderDetail(
            type_product_id=new_order.type_product_id,
            quantity=new_order.quantity,
            total_amount=new_order.price,  # Giá trước giảm giá
            accounts_info=[
                {
                    "id": account.id,
                    "login_name": account.login_name,
                    "password": account.password
                }
                for account in list_account
            ],
        )
        db.add(order_detail)
        await db.flush()

        # Tạo Order
        order = Order(
            user_id=user_id,
            quantity=new_order.quantity,
            total_amount=total_amount,  # Giá sau giảm giá
            order_detail_id=order_detail.id,
            status=OrderStatus.COMPLETED,
            time=datetime.now(timezone.utc)
        )
        db.add(order)
        await db.flush()

        # Tạo VoucherUsage (nếu có)
        if new_order.voucher_id:
            voucher_usage = VoucherUsage(
                voucher_id=new_order.voucher_id,
                user_id=user_id,
                order_id=order.id,
                discount_amount=discount_amount,
                used_at=datetime.now(timezone.utc),
                is_valid=True
            )
            db.add(voucher_usage)

            # Cập nhật Voucher
            voucher.used_count += 1
            if voucher.usage_limit_total and voucher.used_count >= voucher.usage_limit_total:
                voucher.status = "INACTIVE"
                voucher.is_active = False

        # Cập nhật trạng thái tài khoản
        for account in list_account:
            account.status = StatusAccountVuavia.SOLD
            account.orderdetail_id = order_detail.id

        # Trừ tiền user
        user.balance -= total_amount

        # Xóa cache voucher
        if new_order.voucher_id:
            await redis_service.delete_voucher_cache(user_id)

        
        # ghi lịch sử giao dịch trừ tiền 
        transaction = TransactionHistory(
            user_id=user_id,
            type=TransactionType.PURCHASE,
            amount=-total_amount,  # Âm để biểu thị trừ tiền
            description=f"Mua {new_order.quantity} account {type_product.name} với order_id {order.id}",
            order_id=order.id,
            created_at=datetime.now(timezone.utc)
        )
        db.add(transaction)
        await db.commit()
        
        return MessageSchema(message="Order created successfully")

    except HTTPException as http_ex:
        await db.rollback()
        raise http_ex
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")