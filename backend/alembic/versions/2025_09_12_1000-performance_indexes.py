"""Init fresh baseline

Revision ID: init_fresh_2025_09_28
Revises: None
Create Date: 2025-09-28 15:45:00.000000

"""

from alembic import op
import sqlalchemy as sa


# Revision identifiers, used by Alembic
revision = "init_fresh_2025_09_28"
down_revision = None   # Đây là revision gốc
branch_labels = None
depends_on = None


def upgrade() -> None:
    """
    Vì đây là baseline, bạn có thể để trống (coi DB hiện tại là đúng rồi).
    Nếu muốn ghi cấu trúc bảng thì có thể dump model ra, 
    nhưng thường baseline chỉ để trống.
    """
    pass


def downgrade() -> None:
    """
    Không cần downgrade vì đây là baseline.
    """
    pass
