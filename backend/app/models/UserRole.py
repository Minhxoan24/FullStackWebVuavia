from sqlalchemy import Column, Integer, ForeignKey , UniqueConstraint # unique constraint để đảm bảo mỗi user chỉ có một role duy nhất
from sqlalchemy.orm import relationship
from .base import Base

from sqlalchemy import Table, Column, Integer, ForeignKey, UniqueConstraint

user_roles = Table(
    "user_roles",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
    Column("role_id", Integer, ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True),
    UniqueConstraint("user_id", "role_id", name="uq_user_role")
)