from pydantic import BaseModel
from typing import Optional

class AvailableVouchersRequest(BaseModel):
    cart_amount: int  # Tổng giá trị đơn hàng (giỏ hàng)
    category: Optional[str] = None  # Danh mục sản phẩm (nếu có)
