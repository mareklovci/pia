from flask import Blueprint, flash, redirect, render_template, request, url_for
from app.invoices.forms import InvoiceForm
from wtforms import FieldList
from app.models import Invoice, Item
from app import db

invoices = Blueprint('invoices', __name__)


@invoices.route('/invoice/create', methods=['GET', 'POST'])
def create_invoice():
    form = InvoiceForm()

    if form.validate_on_submit():
        new_invoice = Invoice()
        db.session.add(new_invoice)

        for item in form.items.data:
            new_item = Item(**item)
            new_invoice.items.append(new_item)

        db.session.commit()

    all_invoices = Invoice.query

    return render_template('create_invoice.html', title='Create new Invoice', form=form, invoices=all_invoices)


@invoices.route('/<invoice_id>', methods=['GET'])
def show_invoice(invoice_id):
    """Show the details of a invoice"""
    invoice = Invoice.query.filter_by(id=invoice_id).first()

    return render_template('invoice.html', invoice=invoice)
