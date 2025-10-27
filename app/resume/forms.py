from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.fields.choices import SelectField
from wtforms.validators import DataRequired, Length, Email, Regexp


class ContactForm(FlaskForm):
    name = StringField( 'Name', validators=[DataRequired(), Length(4, 10)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone: +380?????????', validators=[Regexp(r'^\+380\d{9}$')])
    subject = SelectField(
        'Subject',
        choices=[('general', 'General Inquiry'), ('job', 'Job Opportunity'), ('other', 'Other')],
        validators=[DataRequired()]
    )
    message = StringField('Message', validators=[DataRequired(), Length(max=500)])
    submit = SubmitField('Contact Me')