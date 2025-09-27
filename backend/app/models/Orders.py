from datetime import datetime, timezone
from sqlalchemy import Column, Integer, ForeignKey, DateTime, Enum as SAEnum , Float
from sqlalchemy.orm import relationship
from .base import Base
from enum import Enum as PyEnum

class OrderStatus(PyEnum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    CANCELED = "CANCELED"

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, autoincrement=True)
    time = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc).replace(tzinfo=None))
    quantity = Column(Integer, nullable=False)
    total_amount = Column(Float, nullable=False)
    status = Column(SAEnum(OrderStatus), nullable=False, default=OrderStatus.PENDING)
    
    # Foreign Keys - CẬP NHẬT CASCADE BEHAVIOR
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
   
    order_detail_id = Column(Integer, ForeignKey("order_details.id", ondelete="CASCADE"), unique=True)
    transaction_history_id = Column(Integer, ForeignKey("transaction_histories.id", ondelete="SET NULL"), unique=True, nullable=True)

    # Relationships
    user = relationship("User", back_populates="orders")
   
    order_detail = relationship("OrderDetail", back_populates="order", uselist=False)
    
  
    voucher_usage = relationship("VoucherUsage", back_populates="order", uselist=False)
    transaction_history = relationship("TransactionHistory", back_populates="order", uselist=False)
