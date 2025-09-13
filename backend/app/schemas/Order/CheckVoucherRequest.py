from pydantic import BaseModel

class CheckVoucherRequest(BaseModel):
    """Request để kiểm tra voucher cho đơn hàng"""
    type_product_id: int
    quantity: int
    
    class Config:
        from_attributes = True
