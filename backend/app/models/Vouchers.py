from .base import Base
from sqlalchemy import Column, Integer, String, DateTime, Enum as SAEnum, Boolean, Text
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from enum import Enum

class VoucherDiscountType(str, Enum):
    PERCENTAGE = "PERCENTAGE"
    FIXED = "FIXED"

class VoucherType(str, Enum):
    PUBLIC = "PUBLIC"          # Voucher công khai, ai cũng dùng được
    PERSONAL = "PERSONAL"      # Voucher cá nhân
    FIRST_TIME = "FIRST_TIME"  # Voucher cho user đầu tiên
    CATEGORY = "CATEGORY"      # Voucher theo category

class VoucherStatus(str, Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    EXPIRED = "EXPIRED"

class Voucher(Base):
    __tablename__ = "vouchers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String(50), unique=True, nullable=False, index=True)  # Mã voucher
    name = Column(String(200), nullable=False)  # Tên voucher
    description = Column(Text, nullable=True)   # Mô tả chi tiết
    
    # Discount settings
    discount_type = Column(SAEnum(VoucherDiscountType), nullable=False)
    discount_value = Column(Integer, nullable=False)  # % hoặc số tiền
    max_discount = Column(Integer, nullable=True)     # Giảm tối đa (cho %)
    min_order_amount = Column(Integer, default=0)     # Đơn hàng tối thiểu
    
    # Voucher type và targeting
    voucher_type = Column(SAEnum(VoucherType), default=VoucherType.PUBLIC)
    
    # Time settings
    start_date = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    expiration_date = Column(DateTime, nullable=False)
    
    # Usage limits
    usage_limit_total = Column(Integer, nullable=True)    #  giới hạn N lượt sd 
    usage_limit_per_user = Column(Integer, default=1)     # Giới hạn mỗi user
    usage_count = Column(Integer)  # đếm số lượt dùng đã dùng
    # Status
    status = Column(SAEnum(VoucherStatus), default=VoucherStatus.ACTIVE)
    is_active = Column(Boolean, default=True)
    
    # Metadata
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc),
                       onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    voucher_usages = relationship("VoucherUsage", back_populates="voucher")
