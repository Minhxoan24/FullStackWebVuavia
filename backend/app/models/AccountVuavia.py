from .base import Base
from sqlalchemy import Column, ForeignKey, Integer, String, Enum as SEA, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from enum import Enum as PyEnum


class StatusAccountVuavia(PyEnum):
    AVAILABLE = "AVAILABLE"
    HOLD = "HOLD"
    SOLD = "SOLD"
    EXPIRED = "EXPIRED"


class AccountVuavia(Base):
    __tablename__ = "account_vuavia"

    id = Column(Integer, primary_key=True, autoincrement=True)
    login_name = Column(String(200), nullable=False, unique=True, index=True)  # Thêm unique + index
    password = Column(String(200), nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
 # Index cho timeout cleanup
    status = Column(
        SEA(StatusAccountVuavia, name="status_account_vuavia"),
        nullable=False,
        default=StatusAccountVuavia.AVAILABLE,
        index=True  # Index cho filter by status
    )

    # Foreign Keys với index
    orderdetail_id = Column(Integer, ForeignKey("order_details.id", ondelete="CASCADE"), nullable=True)
    type_product_id = Column(Integer, ForeignKey("type_products.id", ondelete="CASCADE"), nullable=True, index=True)  # Index cho filter

    # Relationships
    order_detail = relationship("OrderDetail", back_populates="account_vuavias", uselist=False)
    type_product = relationship("TypeProduct", back_populates="account_vuavias")
