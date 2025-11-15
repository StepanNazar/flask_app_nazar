"""rename product table to products

Revision ID: f131cf6401ed
Revises: 3d4f09fa94eb
Create Date: 2025-11-15 14:12:30.804903

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f131cf6401ed'
down_revision = '3d4f09fa94eb'
branch_labels = None
depends_on = None


def upgrade():
    op.rename_table('product', 'products')


def downgrade():
    op.rename_table('products', 'product')
