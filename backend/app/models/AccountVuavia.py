from click import DateTime
from .base import Base
from sqlalchemy import Column, ForeignKey  , Integer, String , Enum as SEA 
from sqlalchemy.orm import relationship
from datetime import datetime, timezone 
from enum import Enum as PyEnum
class StatusAccountVuavia(PyEnum):
    AVAILAYBLE = "Available"
    RESERVED = "Reserved"
    SOLD = "Sold"
    EXPIRED = "Expired"


class AccountVuavia(Base):
    __tablename__ = "account_vuavia"
    id = Column(Integer, primary_key=True, autoincrement=True)
    login_name = Column(String(200), nullable=False ) 
    password = Column(String(200), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, nullable=False, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
    status = Column(SEA(StatusAccountVuavia), nullable=False, default=StatusAccountVuavia.AVAILAYBLE.value)



    # Foreign Keys 
    orderdetail_id = Column(Integer, ForeignKey("order_details.id"), nullable=True, ondelete="CASCADE")
    type_product_id = Column(Integer, ForeignKey("type_products.id"), nullable=True, ondelete="CASCADE")

    # Relationships
    order_detail = relationship("OrderDetail", back_populates="account_vuavias", uselist=False)
    type_product = relationship("TypeProduct", back_populates="account_vuavias")


    