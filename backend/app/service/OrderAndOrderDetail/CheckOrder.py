from datetime import datetime, timezone
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.Order.CreateOrderSchema import CreateOrderSchema
from app.models.TypeProduct import TypeProduct

from app.service.AccountVuavias.CountAccount import CountAccountVuaviaService
from app.service.AccountVuavias.SelectAccount import SelectAccountVuaviaService
from app.service.OrderAndOrderDetail.CaculatorTotalAmount import caculator_total_amount
from backend.app.models.Users import User

async def caculator_total_amount(quantity: int, price: int, discount_amount: int = 0) -> int:
    return max(quantity * price - discount_amount, 0)

async def checkOrder(new_order: CreateOrderSchema, balance_user: float, db: AsyncSession) -> int:
    try:
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

        return total_price
    except HTTPException as http_ex:
        raise http_ex
    except Exception as ex:
        raise HTTPException(status_code=500, detail="Internal Server Error")























