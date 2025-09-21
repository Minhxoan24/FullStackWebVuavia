from sqlalchemy import select
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timezone
import logging

from app.schemas.Order.CreateOrderSchema import CreateOrderSchema
from app.models.TypeProduct import TypeProduct
from app.models.Orders import Order, OrderStatus

# Comment voucher-related imports (tạm thời disable)
# from app.models.Vouchers import Voucher
from app.models.OrderDetail import OrderDetail
from app.schemas.Message.Message import MessageSchema
from app.service.AccountVuavias.CountAccount import CountAccountVuaviaService
from app.service.AccountVuavias.SelectAccount import SelectAccountVuaviaService , MarkAccountsAsSoldService
# from app.models.VoucherUsage import VoucherUsage
from app.models.Users import User
from app.service.RedisService.RedisService import redis_service
from app.models.TransactionHistory import TransactionType
from app.Utils.HashPassword import verify_password

from app.models.TransactionHistory import TransactionHistory

logger = logging.getLogger(__name__)

async def caculator_total_amount(quantity: int, price: int, discount_amount: int = 0) -> int:
    return max(quantity * price - discount_amount, 0)

async def CreateOrderService(
    new_order: CreateOrderSchema, db: AsyncSession, current_user: int
) -> MessageSchema:
    try:
        # Lấy thông tin user
        user = await db.execute(select(User).where(User.id == current_user))
        user = user.scalar_one_or_none()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        balance_user = user.balance

        # Kiểm tra TypeProduct
        query = await db.execute(select(TypeProduct).where(TypeProduct.id == new_order.type_product_id))
        type_product = query.scalar_one_or_none()
        if not type_product:
            raise HTTPException(status_code=404, detail="TypeProduct not found")

        # Kiểm tra số lượng account
        count_account = await CountAccountVuaviaService(new_order.type_product_id, db)
        if new_order.quantity > count_account:
            raise HTTPException(status_code=400, detail="Not enough products in stock")

        # Tính giá tổng
        total_price = await caculator_total_amount(new_order.quantity, type_product.price, new_order.discount_amount)
        if total_price <= 0:
            raise HTTPException(status_code=400, detail="Invalid total amount")
        if total_price > balance_user:
            raise HTTPException(status_code=400, detail="Not enough money to create order")

        # Trừ tiền user (KHÔNG commit)
        user.balance -= total_price
        db.add(user)
        await db.flush()  # Flush thay vì commit

        # Lấy account
        accounts = await SelectAccountVuaviaService(new_order.type_product_id, new_order.quantity, db)
        if len(accounts) < new_order.quantity:
            raise HTTPException(status_code=400, detail="Not enough products in stock")

        # Cập nhật trạng thái account đã bán
        await MarkAccountsAsSoldService([acc.id for acc in accounts], db)

        # Tạo OrderDetail
        order_detail = OrderDetail(
            type_product_id=new_order.type_product_id,
            quantity=new_order.quantity,
            total_amount=total_price,
            accounts_info=[
                {
                    "id": account.id,
                    "login_name": account.login_name,
                    "password": account.password  # Lưu trực tiếp (plain text để deliver)
                }
                for account in accounts
            ],
        )
        db.add(order_detail)
        await db.flush()

        # Update orderdetail_id for accounts
        for acc in accounts:
            acc.orderdetail_id = order_detail.id
        await db.flush()

        # Tạo Order
        order = Order(
            user_id=current_user,
            quantity=new_order.quantity,
            total_amount=total_price,
            order_detail_id=order_detail.id,
            status=OrderStatus.COMPLETED,
            time=datetime.now(timezone.utc).replace(tzinfo=None)  # Sửa: naive datetime
        )
        db.add(order)
        await db.flush()

        # Ghi lịch sử giao dịch
        transaction = TransactionHistory(
            user_id=current_user,
            order_id=order.id,
            amount=total_price,
            type=TransactionType.PURCHASE,
            description=f"Order payment for product {type_product.name}",
            created_at=datetime.now(timezone.utc).replace(tzinfo=None)  # Sửa: naive datetime
        )
        db.add(transaction)

        # Commit TẤT CẢ một lần ở cuối
        await db.commit()

        return MessageSchema(status="success", message="Order created successfully")

    except HTTPException as http_ex:
        await db.rollback()
        raise http_ex
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")