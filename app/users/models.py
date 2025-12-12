import sqlalchemy as sa
from sqlalchemy import orm as so

from app import db, bcrypt


class User(db.Model):
    __tablename__ = 'users'
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(100), unique=True, nullable=False)
    email: so.Mapped[str] = so.mapped_column(sa.String(150), unique=True, nullable=False)
    password_hash: so.Mapped[str] = so.mapped_column(sa.String(256), nullable=False)
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