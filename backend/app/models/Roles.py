from sqlalchemy import Column, Integer, Enum as SAEnum
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum
from .base import Base
from .UserRole import user_roles

class RoleEnum(PyEnum):
    USER = "USER"
    ADMIN = "ADMIN"

class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(SAEnum(RoleEnum), nullable=False, default=RoleEnum.USER)

    # Quan hệ N-N với User qua bảng trung gian user_roles
    users = relationship("User", secondary=user_roles, back_populates="roles")
