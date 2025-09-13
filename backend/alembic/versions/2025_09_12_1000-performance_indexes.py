"""Add indexes and constraints for AccountVuavia performance

Revision ID: performance_indexes_2025_09_12
Revises: previous_revision
Create Date: 2025-09-12 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers
revision = 'performance_indexes_2025_09_12'
down_revision = 'cdafc1a6e4ad'  # Update này với revision gần nhất
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Thêm unique constraint cho login_name nếu chưa có
    op.create_unique_constraint('uq_account_vuavia_login_name', 'account_vuavia', ['login_name'])
    
    # Thêm indexes để tối ưu performance
    op.create_index('ix_account_vuavia_login_name', 'account_vuavia', ['login_name'])
    op.create_index('ix_account_vuavia_status', 'account_vuavia', ['status'])
    op.create_index('ix_account_vuavia_type_product_id', 'account_vuavia', ['type_product_id'])
    op.create_index('ix_account_vuavia_updated_at', 'account_vuavia', ['updated_at'])
    
    # Composite index cho common queries
    op.create_index('ix_account_vuavia_status_type', 'account_vuavia', ['status', 'type_product_id'])
    op.create_index('ix_account_vuavia_hold_timeout', 'account_vuavia', ['status', 'updated_at'])

def downgrade() -> None:
    # Xóa indexes
    op.drop_index('ix_account_vuavia_hold_timeout', 'account_vuavia')
    op.drop_index('ix_account_vuavia_status_type', 'account_vuavia')
    op.drop_index('ix_account_vuavia_updated_at', 'account_vuavia')
    op.drop_index('ix_account_vuavia_type_product_id', 'account_vuavia')
    op.drop_index('ix_account_vuavia_status', 'account_vuavia')
    op.drop_index('ix_account_vuavia_login_name', 'account_vuavia')
    
    # Xóa unique constraint
    op.drop_constraint('uq_account_vuavia_login_name', 'account_vuavia', type_='unique')
