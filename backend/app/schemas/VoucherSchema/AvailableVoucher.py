from pydantic import BaseModel
from typing import Optional

class AvailableVouchersRequest(BaseModel):
    cart_amount: int  # Tổng giá trị đơn hàng (giỏ hàng)
    category_id: Optional[int] = None  # ID danh mục sản phẩm (nếu có)
