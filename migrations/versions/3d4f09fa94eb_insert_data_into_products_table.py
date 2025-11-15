"""Insert data into products table

Revision ID: 3d4f09fa94eb
Revises: b182b011223b
Create Date: 2025-11-15 13:57:56.004891

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column


# revision identifiers, used by Alembic.
revision = '3d4f09fa94eb'
down_revision = 'b182b011223b'
branch_labels = None
depends_on = None


def upgrade():
    categories_table = table(
        "categories", column("id", sa.Integer), column("name", sa.String)
    )

    products_table = table(
        "product",
        column("name", sa.String),
        column("price", sa.Float),
        column("content", sa.Text),
        column("active", sa.Boolean),
        column("category_id", sa.Integer),
    )

    op.bulk_insert(
        categories_table,
        [
            {"name": "Electronics"},
            {"name": "Books"},
            {"name": "Clothing"},
        ],
    )

    op.bulk_insert(
        products_table,
        [
            {"name": "Laptop", "price": 1200.0, "active": True, "category_id": 1, "content": "No description"},
            {"name": "Smartphone LG", "price": 800.0, "active": True, "category_id": 1, "content": "No description"},
            {"name": "Novel", "price": 20.0, "active": True, "category_id": 2, "content": "No description"},
            {"name": "T-Shirt", "price": 25.0, "active": False, "category_id": 3, "content": "No description"},
        ],
    )


def downgrade():
    op.execute("""
               DELETE FROM product
               WHERE name IN ('Ultrabook', 'Laptop', 'Smartphone LG', 'Novel', 'T-Shirt');
               """)

    op.execute("""
               DELETE FROM categories
               WHERE name IN ('Electronics', 'Books', 'Clothing');
               """)
