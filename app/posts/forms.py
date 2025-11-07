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

from app.posts.models import Category


class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(min=2, max=150)])
    content = TextAreaField("Content", render_kw={"rows": 5, "cols": 40}, validators=[DataRequired()])
    is_active = BooleanField("Active Post")
    category = SelectField("Category", choices=[(cat.value, cat.name) for cat in Category], validators=[DataRequired()])
    posted = DateTimeLocalField('Publish Date', format="%Y-%m-%dT%H:%M")
    submit = SubmitField("Add Post")

class DeletePostForm(FlaskForm):
    submit = SubmitField("Delete Post")