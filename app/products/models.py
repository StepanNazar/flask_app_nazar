from datetime import datetime, UTC

import sqlalchemy as sa
from sqlalchemy import orm as so

from app import db


class Product(db.Model):
    __tablename__ = 'products'
    id: so.Mapped[int] = so.mapped_column(sa.Integer, primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(100), nullable=False)
    price: so.Mapped[float] = so.mapped_column(sa.Float, nullable=False)
    content: so.Mapped[str] = so.mapped_column(sa.Text(), nullable=False)
    active: so.Mapped[bool] = so.mapped_column(sa.Boolean, nullable=False, default=True)
    created_at: so.Mapped[datetime] = so.mapped_column(
        sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()
    )
    category_id: so.Mapped[int | None] = so.mapped_column(sa.Integer, sa.ForeignKey('categories.id'))
    category: so.Mapped["Category"] = so.relationship('Category', back_populates='products')

class Category(db.Model):
    __tablename__ = 'categories'
    id: so.Mapped[int] = so.mapped_column(sa.Integer, primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(128), nullable=False, unique=True)
    products: so.Mapped[list["Product"]] = so.relationship(
        'Product',
        back_populates='category',
        lazy='joined'
    )

products = [
    {
        "id": 1,
        "name": "Laptop",
        "price": 1200,
        "content": "Потужний ноутбук з процесором Intel Core i7, 16 ГБ оперативної пам’яті та SSD на 512 ГБ."
    },
    {
        "id": 2,
        "name": "Phone",
        "price": 800,
        "content": "Смартфон із 6.5-дюймовим OLED-дисплеєм, подвійною камерою та акумулятором на 5000 мА·год."
    },
    {
        "id": 3,
        "name": "PC",
        "price": 1800,
        "content": "Настільний комп’ютер для ігор або роботи з графікою: RTX 4070, 32 ГБ RAM, 1 ТБ SSD."
    }
]

class ProductRepository:
    def __init__(self):
        # Тимчасова заглушка з продуктами
        self._products = products

    # --- CRUD ---
    def get_all(self):
        return self._products

    def get_by_id(self, product_id):
        return next((p for p in self._products if p["id"] == product_id), None)

product_repo = ProductRepository()