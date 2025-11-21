from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    TextAreaField,
    SelectField,
    SubmitField,
    BooleanField,
    DateTimeLocalField,
)
from wtforms.validators import Length, DataRequired
import sqlalchemy as sa

from app import db
from app.posts.models import Category
from app.users.models import User


class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(min=2, max=150)])
    content = TextAreaField("Content", render_kw={"rows": 5, "cols": 40}, validators=[DataRequired()])
    is_active = BooleanField("Active Post")
    category = SelectField("Category", choices=[(cat.value, cat.name) for cat in Category], validators=[DataRequired()])
    posted = DateTimeLocalField('Publish Date', format="%Y-%m-%dT%H:%M")
    author_id = SelectField("Author", coerce=int)
    submit = SubmitField("Add Post")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.author_id.choices = [
            (author.id, author.username)
            for author in db.session.execute(sa.select(User).order_by(User.id)).scalars().all()
        ]

class DeletePostForm(FlaskForm):
    submit = SubmitField("Delete Post")