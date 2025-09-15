from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB
from .base import Base

class InforTypeProduct(Base):
    __tablename__ = "information_type_products"  # Nên thống nhất plural

    id = Column(Integer, primary_key=True, index=True)
    describe = Column(JSONB, nullable=False)

    # Sửa ForeignKey: phải đúng với __tablename__ của TypeProduct
    type_product_id = Column(Integer, ForeignKey("type_products.id", ondelete="CASCADE"), nullable=False)

    type_product = relationship("TypeProduct", back_populates="information")
