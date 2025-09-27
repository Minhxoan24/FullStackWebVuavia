from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float, Enum as SAEnum
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum
from .base import Base
from datetime import datetime, timezone

class DepositStatus(PyEnum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class DepositRequest(Base):
    __tablename__ = "deposit_requests"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    amount = Column(Float, nullable=False)
    transaction_code = Column(String(50), unique=True, nullable=False)  # Mã giao dịch duy nhất
    status = Column(SAEnum(DepositStatus), default=DepositStatus.PENDING)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc).replace(tzinfo=None))  # Sửa thành naive
    completed_at = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="deposit_requests")  # Quan hệ với User
