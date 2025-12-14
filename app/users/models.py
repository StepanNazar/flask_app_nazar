import sqlalchemy as sa
from datetime import datetime, timezone
from flask_login import UserMixin
from sqlalchemy import orm as so
from typing import Optional

from app import db, bcrypt, login_manager


@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(100), unique=True, nullable=False)
    email: so.Mapped[str] = so.mapped_column(sa.String(150), unique=True, nullable=False)
    password_hash: so.Mapped[str] = so.mapped_column(sa.String(256), nullable=False)
    image: so.Mapped[Optional[str]] = so.mapped_column(sa.String(255), nullable=True, default='profile_default.jpg')
    about_me: so.Mapped[Optional[str]] = so.mapped_column(sa.Text, nullable=True)
    last_seen: so.Mapped[Optional[datetime]] = so.mapped_column(sa.DateTime, nullable=True, default=lambda: datetime.now(timezone.utc))
    posts = so.relationship("Post", back_populates="user", cascade="all, delete-orphan")

    def __init__(self, password: str = "", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_password(password)

    def set_password(self, password: str) -> None:
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password: str) -> bool:
        if not isinstance(password, str):
            return False
        return bcrypt.check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"User(id={self.id!r}, username={self.username!r}, email={self.email!r})"