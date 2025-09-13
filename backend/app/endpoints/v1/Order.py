from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.auth import get_current_user
from app.db.DataBase import get_async_session
from app.models.Users import User
from app.schemas.Order.CreateOrderSchema import CreateOrderSchema
from app.schemas.Order.ResponseOrder import OrderResponseSchema  
from app.schemas.OrderDetail.ResponseOrderDetailSchema import ResponseOrderDetailSchema  
from app.schemas.Message.Message import MessageSchema
from app.schemas.Order.ApplyVoucher import ApplyVoucherRequest, ApplyVoucherResponse
from app.schemas.Order.CheckVoucherRequest import CheckVoucherRequest
from app.schemas.VoucherSchema.VoucherWithApplicabilitySchema import VoucherWithApplicabilitySchema

from app.service.OrderAndOrderDetail.CreateOrder import CreateOrderService
from app.service.OrderAndOrderDetail.CancleVoucher import cancel_voucher as order_cancel_voucher
from app.service.OrderAndOrderDetail.ApplyVoucher import apply_voucher
from app.service.OrderAndOrderDetail.InformationOrder import InformationOrderService
from app.service.OrderAndOrderDetail.InformationOrderDetail import InformationOrderDetailService
from app.service.Voucher.CheckVouchersForOrder import check_vouchers_for_order

router = APIRouter(tags=["Order"], prefix="/orders")

@router.post("/checkout", response_model=MessageSchema)
async def checkout(
    new_order: CreateOrderSchema,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session)
):
    try:
        return await CreateOrderService(new_order, db, current_user.id)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during checkout: {str(e)}")

@router.post("/vouchers/apply", response_model=ApplyVoucherResponse)
async def apply_voucher_endpoint(
    request: ApplyVoucherRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session)
):
    try:
        return await apply_voucher(request, current_user.id, db)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error applying voucher: {str(e)}")

@router.post("/vouchers/cancel", response_model=MessageSchema)
async def cancel_voucher_endpoint(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session)
):
    try:
        return await order_cancel_voucher(current_user.id, db)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error cancelling voucher: {str(e)}")

@router.post("/vouchers/check", response_model=list[VoucherWithApplicabilitySchema])
async def check_vouchers_for_order_endpoint(
    request: CheckVoucherRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session)
):
    """
    Kiểm tra tất cả voucher của user và trả về với thông tin can_apply = True/False
    Sử dụng khi user chọn sản phẩm và số lượng, trước khi áp dụng voucher
    """
    try:
        return await check_vouchers_for_order(request, current_user.id, db)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error checking vouchers: {str(e)}")

@router.get("/my-orders", response_model=list[OrderResponseSchema])  
async def get_my_orders(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session)
):
    """Lấy danh sách đơn hàng của người dùng"""
    try:
        return await InformationOrderService(db, current_user)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting orders: {str(e)}")

@router.get("/order/orderDetail{order_id}", response_model=ResponseOrderDetailSchema)  
async def get_order_detail(
    order_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session)
):
    """Lấy thông tin chi tiết của một đơn hàng"""
    try:
        return await InformationOrderDetailService(order_id, db, current_user)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting order detail: {str(e)}")


