from .base import Base
from sqlalchemy import Column, Integer, ForeignKey, DateTime, Boolean , Float
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

class VoucherUsage(Base):
    __tablename__ = "voucher_usages"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    voucher_id = Column(Integer, ForeignKey("vouchers.id", ondelete="CASCADE"), nullable=False) # Voucher 1-N VoucherUsage 
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False) # User 1-N VoucherUsage
    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"), nullable=True) # Order 1-1 VoucherUsage

    discount_amount = Column(Float, nullable=False)  # Số tiền được giảm
    used_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    is_valid = Column(Boolean, default=True)  # Có thể bị hủy nếu order bị hủy
    
    # Relationships
    voucher = relationship("Voucher", back_populates="voucher_usages")
    user = relationship("User", back_populates="voucher_usages")  
    order = relationship("Order", back_populates="voucher_usage") 