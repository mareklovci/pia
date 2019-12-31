from wtforms import FieldList, Form, FormField, IntegerField, SelectField, StringField, SubmitField, FloatField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm


class ItemForm(Form):
    """Invoices subform

    CSRF is disabled for this subform (using `Form` as parent class) because it is never used by itself.
    """
    count = FloatField('Count', validators=[
        DataRequired()
    ])
    unit = StringField('Unit', validators=[
        DataRequired()
    ])
    desc = StringField('Description', validators=[
        DataRequired()
    ])
    vat = IntegerField('VAT', validators=[
        DataRequired()
    ])
    price = FloatField('Price', validators=[
        DataRequired()
    ])


class InvoiceForm(FlaskForm):
    issue_date = DateField('Date of Issue', validators=[
        DataRequired()
    ])
    due_date = DateField('Date of Taxable Supply', validators=[
        DataRequired()
    ])
    payment_form = SelectField('Form of Payment', choices=[('form1', 'Cash'),
                                                           ('form2', 'Cash on Delivery'),
                                                           ('form3', 'Credit Card'),
                                                           ('form4', 'Bank Transfer')])
    items = FieldList(FormField(ItemForm), min_entries=1)

    submit = SubmitField('Create Invoice')
