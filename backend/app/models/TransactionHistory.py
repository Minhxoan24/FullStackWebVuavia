from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum as SAEnum
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum
from datetime import datetime
from .base import Base

class TransactionType(PyEnum):
    DEPOSIT = "Deposit"
    WITHDRAW = "Withdraw"

class TransactionStatus(PyEnum):
    PENDING = "Pending"
    SUCCESS = "Success"
    FAILED = "Failed"

class TransactionHistory(Base):
    __tablename__ = "transaction_histories"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    amount = Column(Integer, nullable=False)
    type = Column(SAEnum(TransactionType), nullable=False)
    status = Column(SAEnum(TransactionStatus), nullable=False, default=TransactionStatus.PENDING)
    description = Column(String(255), nullable=True)  # Ví dụ: Nạp qua Casso
    reference_code = Column(String(100), nullable=True)  # Mã giao dịch Casso
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="transaction_histories")
