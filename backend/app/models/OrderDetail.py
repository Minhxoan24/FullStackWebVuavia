from sqlalchemy import Column, Integer, ForeignKey , JSON
from sqlalchemy.orm import relationship
from .base import Base
from .Orders import Order


class OrderDetail(Base):
    __tablename__ = "order_details"
    id = Column(Integer, primary_key=True, autoincrement=True)
    type_product_id = Column(Integer, ForeignKey("type_products.id", ondelete="CASCADE"), nullable=False)
    quantity = Column(Integer, nullable=False)
    price_at_order_time = Column(Integer, nullable=False)  # lưu giá tại thời điểm mua
    accounts_info = Column(JSON, nullable=False)

    order = relationship("Order", back_populates="order_detail", uselist=False)
    account_vuavias = relationship("AccountVuavia", back_populates="order_detail")
    type_product = relationship("TypeProduct")  # để join ra tên sản phẩm
