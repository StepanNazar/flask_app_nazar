import enum
from datetime import datetime, timezone

import sqlalchemy as sa
from sqlalchemy import orm as so

from app import db

class Category(enum.Enum):
    news = "news"
    publication = "publication"
    tech = "tech"
    other = "other"


class Post(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    title: so.Mapped[str] = so.mapped_column(sa.String(150), nullable=False)
    content: so.Mapped[str] = so.mapped_column(sa.Text(), nullable=False)
    posted: so.Mapped[datetime] = so.mapped_column(
        default=lambda: datetime.now(timezone.utc)
    )
    category: so.Mapped[Category] = so.mapped_column(sa.Enum(Category))
    is_active: so.Mapped[bool] = so.mapped_column(default=True)
    author: so.Mapped[str] = so.mapped_column(sa.String(20), default="Anonymous")

    def __repr__(self):
        return f"Post(id={self.id!r}, title={self.title!r}, category={self.category!r})"
