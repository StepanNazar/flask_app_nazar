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

post_tags = db.Table(
    'post_tags',
    db.Column('post_id', db.Integer, db.ForeignKey('post.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'), primary_key=True)
)

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
    tags: so.Mapped[list["Tag"]] = so.relationship(secondary=post_tags, back_populates="posts")

    def __repr__(self):
        return f"Post(id={self.id!r}, title={self.title!r}, category={self.category!r})"

class Tag(db.Model):
    __tablename__ = 'tags'
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String, unique=True, nullable=False)
    posts: so.Mapped[list["Post"]] = so.relationship(secondary=post_tags, back_populates="tags")

    def repr(self):
        return f"Tag(id={self.id!r}, name={self.name!r})"
