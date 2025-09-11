from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.models.OrderDetail import OrderDetail
from app.models.Orders import Order
from app.models.Users import User
from app.schemas.OrderDetail.ResponseOrderDetailSchema import ResponseOrderDetailSchema


async def InformationOrderDetailService(
    id_order_detail: int, 
    db: AsyncSession, 
    user: User
) -> ResponseOrderDetailSchema:
    """Service lấy thông tin chi tiết order detail"""
    try:
        # Kiểm tra order detail có tồn tại và thuộc về user không
        query = await db.execute(
            select(OrderDetail)
            .join(Order)
            .options(
                selectinload(OrderDetail.type_product),
                selectinload(OrderDetail.order)
            )
            .where(
                OrderDetail.id == id_order_detail,
                Order.user_id == user.id
            )
        )
        
        order_detail = query.scalar_one_or_none()
        
        if not order_detail:
            raise HTTPException(
                status_code=404, 
                detail="Order detail not found or you don't have permission to access it"
            )

        return ResponseOrderDetailSchema(
            id=order_detail.id,
            time=order_detail.order.time,
            quantity=order_detail.quantity,
            total_amount=order_detail.total_amount,
            type_product_id=order_detail.type_product_id,
            accounts_info=order_detail.accounts_info
        )

    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Error fetching order detail: {str(e)}")
    




