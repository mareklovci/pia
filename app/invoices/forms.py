from flask_wtf import FlaskForm
from wtforms import FieldList, FloatField, Form, FormField, IntegerField, SelectField, StringField, SubmitField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired

from app.models import Contact, InvoiceType, Payment


class FilterForm(FlaskForm):
    """Invoices filter form"""
    date_from = DateField('Issue Date From')
    date_till = DateField('Issue Date Till')
    invoice_type = SelectField('Invoice Type', choices=[item.value for item in InvoiceType])
    submit = SubmitField('Filter View', )


class ItemForm(Form):
    """Invoices subform

    CSRF is disabled for this subform (using `Form` as parent class) because it is never used by itself.
    """
    count = FloatField('Count', default=0.0)
    unit = StringField('Unit', validators=[
        DataRequired()
    ])
    desc = StringField('Description', validators=[
        DataRequired()
    ])
    vat = IntegerField('VAT', default=0)
    price = FloatField('Price', default=0.0)


class InvoiceForm(FlaskForm):
    issue_date = DateField('Date of Issue', validators=[
        DataRequired()
    ])
    due_date = DateField('Date of Taxable Supply', validators=[
        DataRequired()
    ])
    payment_form = SelectField('Form of Payment', coerce=int, choices=[item.value for item in Payment])
    type = SelectField('Invoice Type', coerce=int, choices=[InvoiceType.Inbound.value,
                                                            InvoiceType.Outbound.value])
    buyer = QuerySelectField('Buyer', query_factory=lambda: Contact.query.all(), get_label='name')
    items = FieldList(FormField(ItemForm))

    submit = SubmitField('Submit')
