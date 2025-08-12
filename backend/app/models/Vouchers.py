from .base import Base
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime 
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

class Voucher(Base):
    __tablename__ = "vouchers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String(50), nullable=False, unique=True)
    discount_type = Column(String(50), nullable=False)  # 'percentage' hoặc 'fixed'
    discount_value = Column(Integer, nullable=False)
    start_date = Column(DateTime, nullable=False, default=datetime.now(timezone.utc))
    expiration_date = Column(DateTime, nullable=False)
    use_limit = Column(Integer, nullable=False, default=1)

    # Khóa ngoại để biết voucher thuộc về ai
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    # Quan hệ
    user = relationship("User", back_populates="vouchers")
    orders = relationship("Order", back_populates="voucher")




# from .base import Base 
# from sqlalchemy import Column, Integer, String, ForeignKey
# from sqlalchemy.orm import relationship
# from sqlalchemy import DateTime
# from datetime import datetime, timezone

# class Voucher(Base):
#     __tablename__ = "vouchers"
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     code = Column(String(50), nullable=False, unique=True)
#     discount_type = Column(String(50), nullable=False)  # e.g., 'percentage', 'fixed'
#     discount_value = Column(Integer, nullable=False)
#     start_date = Column(DateTime, nullable=False, default=  datetime.now(timezone.utc))
#     expiration_date = Column(DateTime, nullable=False)
#     use_limit = Column(Integer, nullable=False, default=1)
#     user_id = Column(Integer, ForeignKey("users.id"), nullable=False , ondelete="CASCADE")

    
#     order = relationship("Order", back_populates="voucher")
