from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .base import Base

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, autoincrement=True)
    time = Column(DateTime, nullable=False)
    sum = Column(Integer, nullable=False)

    voucher_id = Column(Integer, ForeignKey("vouchers.id"), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    order_detail_id = Column(Integer, ForeignKey("order_details.id", ondelete="CASCADE"), unique=True)

    # Quan hệ
    voucher = relationship("Voucher", back_populates="orders")
    user = relationship("User", back_populates="orders")
    order_detail = relationship("OrderDetail", back_populates="order", uselist=False)

