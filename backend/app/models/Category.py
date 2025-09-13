from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import Base
class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200), nullable=False)
    description = Column(String(500), nullable=True)
    

    # relationship
    type_products = relationship("TypeProduct", back_populates="category")

