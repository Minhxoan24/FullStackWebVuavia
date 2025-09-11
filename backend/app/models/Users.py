from sqlalchemy import Column, Float, Integer, String, Enum as SAEnum , DateTime
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum
from .base import Base
from .UserRole import user_roles  # nếu bạn có bảng role

class StatusUserEnum(PyEnum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    surname = Column(String(200), nullable=False)
    avatar = Column(String(300), nullable=True)
    accountname = Column(String(200), unique=True, nullable=False)
    email = Column(String(200), unique=True, nullable=False)
    phone = Column(String(10), unique=True, nullable=False)
    password = Column(String(200), nullable=False)
    balance = Column(Float, default=0)
    status = Column(SAEnum(StatusUserEnum), nullable=False, default=StatusUserEnum.ACTIVE)

    # Quan hệ
    roles = relationship("Role", secondary=user_roles, back_populates="users")
    orders = relationship("Order", back_populates="user")
    
    transaction_histories = relationship("TransactionHistory", back_populates="user")

    voucher_usages = relationship("VoucherUsage", back_populates="user")

