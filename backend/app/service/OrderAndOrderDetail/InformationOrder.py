from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.schemas.Order.ResponseOrder import OrderResponseSchema
from app.models.Orders import Order
from app.models.Users import User


async def InformationOrderService(db: AsyncSession, user: User) -> list[OrderResponseSchema]:
    """Service lấy thông tin tất cả orders của user"""
    try:
        query = await db.execute(
            select(Order)
            .options(
                selectinload(Order.order_detail),
                selectinload(Order.voucher)
            )
            .where(Order.user_id == user.id)
            .order_by(Order.time.desc())
        )
        orders = query.scalars().all()

        if not orders:
            return []  # Trả về list rỗng thay vì raise exception

        # Convert sang response schema
        result = []
        for order in orders:
            result.append(OrderResponseSchema(
                order_id=order.id,
                time=order.time,
                quantity=order.quantity,
                total_amount=order.total_amount,
                order_detail_id=order.order_detail_id,
                status=order.status.value
            ))

        return result

    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Error fetching orders: {str(e)}")
