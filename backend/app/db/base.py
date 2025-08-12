"""
Import tất cả model để Alembic và Base.metadata nhận biết.
Chỉ import ở đây, không khởi tạo gì khác.
"""

from app.models.base import Base

# Import toàn bộ model vào để Base.metadata chứa đầy đủ table
from app.models.Users import User
from app.models.Roles import Role
from app.models.UserRole import user_roles
from app.models.TypeProduct import TypeProduct
from app.models.AccountVuavia import AccountVuavia
from app.models.Category import Category
from app.models.OrderDetail import OrderDetail
from app.models.TransactionHistory import TransactionHistory
from app.models.Vouchers import Voucher
from app.models.Orders import Order

__all__ = [
    "Base", "User", "Order", "Role", "user_roles", "TypeProduct",
    "AccountVuavia", "Category", "OrderDetail", "TransactionHistory", "Voucher"
]