from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum as SAEnum , DateTime , Float
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum
from datetime import datetime, timezone
from .base import Base
class TransactionType(PyEnum):
    PURCHASE = "PURCHASE"  # Trừ tiền khi mua hàng
    DEPOSIT = "DEPOSIT"    # Cộng tiền khi nạp

class TransactionHistory(Base):
    __tablename__ = "transaction_histories"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # Liên kết với user
    type = Column(SAEnum(TransactionType), nullable=False)  # Loại giao dịch
    amount = Column(Float, nullable=False)  # Số tiền (âm cho trừ, dương cho cộng)
    description = Column(String(255), nullable=True)  # Mô tả (ví dụ: "Mua 5 account Facebook", "Nạp từ ngân hàng BIDV")
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=True)  # Liên kết với order nếu là PURCHASE
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships (tùy chọn)
    user = relationship("User", back_populates="transaction_histories")
    order = relationship("Order", back_populates="transaction_history")
