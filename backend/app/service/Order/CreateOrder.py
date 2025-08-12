
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.OrderSchema.CreateOrderSchema import CreateOrderSchema
from app.models.Orders import Order

async def CreateOrderService(new_order: CreateOrderSchema, db: AsyncSession):
    """ 
    Dịch vụ tạo đơn hàng mới    
    """
    # Tạo đơn hàng mới
    new_order_instance = Order(
        id_TypeProduct=new_order.id_TypeProduct,
        quanlity=new_order.quanlity
    )