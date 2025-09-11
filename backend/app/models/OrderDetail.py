from sqlalchemy import Column, Integer, ForeignKey , JSON , Float
from sqlalchemy.orm import relationship
from .base import Base
from .Orders import Order


class OrderDetail(Base):
    __tablename__ = "order_details"
    id = Column(Integer, primary_key=True, autoincrement=True)
    type_product_id = Column(Integer, ForeignKey("type_products.id", ondelete="CASCADE"), nullable=False)
    quantity = Column(Integer, nullable=False)
    total_amount = Column(Float, nullable=False)  # lưu giá tại thời điểm mua
    accounts_info = Column(JSON, nullable=False)

    order = relationship("Order", back_populates="order_detail", uselist=False)
    account_vuavias = relationship("AccountVuavia", back_populates="order_detail")
    type_product = relationship("TypeProduct" , back_populates="order_details") 
