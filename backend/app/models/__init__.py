from .base import Base

# Import tất cả models để SQLAlchemy có thể tạo relationships
from .Users import User
from .Roles import Role  
from .UserRole import user_roles
from .Orders import Order
from .OrderDetail import OrderDetail
from .TransactionHistory import TransactionHistory
from .Vouchers import Voucher
from .AccountVuavia import AccountVuavia
from .TypeProduct import TypeProduct
from .Category import Category

__all__ = [
    "Base",
    "User", 
    "Role",
    "user_roles", 
    "Order",
    "OrderDetail",
    "TransactionHistory", 
    "Voucher",
    "AccountVuavia",
    "TypeProduct",
    "Category"
]