from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email


class ContactForm(FlaskForm):
    name = StringField('Name', validators=[
        DataRequired()
    ])
    residence = StringField('Residence', validators=[
        DataRequired()
    ])
    ic = StringField('IČ', validators=[
        DataRequired()
    ])
    dic = StringField('DIČ', validators=[
        DataRequired()
    ])
    phone = StringField('Phone Number', validators=[
        DataRequired()
    ])
    email = StringField('Email', validators=[
        DataRequired(),
        Email()
    ])
    submit = SubmitField('Submit')
