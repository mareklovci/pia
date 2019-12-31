from datetime import date

from flask import Blueprint, redirect, render_template, request, url_for

from app import db
from app.invoices.forms import InvoiceForm
from app.models import Invoice, Item

invoices = Blueprint('invoices', __name__)


@invoices.route('/invoice/create', methods=['GET', 'POST'])
def create_invoice():
    form = InvoiceForm()

    if request.method == 'GET':
        form.issue_date.data = date.today()  # .strftime('%Y-%m-%d')
        form.due_date.data = date.today()

    if form.validate_on_submit():
        new_invoice = Invoice(issue_date=form.issue_date.data,
                              due_date=form.due_date.data,
                              payment_form=form.payment_form.data)
        db.session.add(new_invoice)

        total_sum = 0

        for item in form.items.data:
            new_item = Item(**item)
            new_item.total_price = new_item.count * new_item.price
            total_sum += new_item.total_price
            new_invoice.items.append(new_item)

        new_invoice.total_sum = total_sum
        db.session.commit()
        return redirect(url_for('invoices.invoice', invoice_id=new_invoice.id))

    return render_template('create_invoice.html', form=form)


@invoices.route('/invoice/<int:invoice_id>', methods=['GET'])
def invoice(invoice_id):
    """Show the details of a invoice"""
    bill = Invoice.query.get_or_404(invoice_id)
    return render_template('invoice.html', invoice=bill)


@invoices.route('/invoice', methods=['GET'])
def list_invoices():
    all_invoices = Invoice.query
    return render_template('list_invoices.html', invoices=all_invoices)