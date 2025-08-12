from sqlalchemy import Column, Integer, String, ForeignKey 
from sqlalchemy.orm import relationship

from .base import Base

class TypeProduct(Base):
    __tablename__ = "type_products"  # Đổi tên table cho nhất quán

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200), nullable=False)
    price = Column(Integer, nullable=False)
    description = Column(String(500), nullable=True)
    image = Column(String(500), nullable=True)

    # Foreign Key
   
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False , ondelete="CASCADE")
    
    # Relationships
    category = relationship("Category", back_populates="type_products")
    account_vuavias = relationship("AccountVuavia", back_populates="type_product")
    order_details = relationship("OrderDetail", back_populates="type_product")
   