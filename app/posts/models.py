import enum
from datetime import datetime, timezone
from typing import TYPE_CHECKING

import sqlalchemy as sa
from sqlalchemy import orm as so

from app import db
if TYPE_CHECKING:
    from app.users.models import User


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
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("users.id"), nullable=True)
    user: so.Mapped["User"] = so.relationship(back_populates="posts")

    def __repr__(self):
        return f"Post(id={self.id!r}, title={self.title!r}, category={self.category!r})"
