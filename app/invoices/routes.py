import datetime
from datetime import date

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app import db
from app.invoices.forms import FilterForm, InvoiceForm, ItemForm
from app.models import Company, Invoice, InvoiceType, Item, Roles
from app.utils import roles_required

invoices = Blueprint('invoices', __name__)


@invoices.route('/invoice/create', methods=['GET', 'POST'])
def create_invoice():
    form = InvoiceForm()

    if request.method == 'GET':
        form.issue_date.data = date.today()  # .strftime('%Y-%m-%d')
        form.due_date.data = date.today()

    if form.validate_on_submit():
        company = Company.query.get_or_404(1)  # we have only one company (id 1)
        new_invoice = Invoice(issue_date=form.issue_date.data,
                              due_date=form.due_date.data,
                              payment_form=form.payment_form.data,
                              type=form.type.data,
                              invoice_buyer=form.buyer.data,
                              invoice_author=current_user,
                              invoice_company=company)
        new_invoice.create_serial_number()
        db.session.add(new_invoice)

        total_sum = 0
        for item in form.items.data:
            new_item = Item(**item)
            new_item.total_price = new_item.count * new_item.price
            total_sum += new_item.total_price
            db.session.add(new_item)
            new_invoice.items.append(new_item)

        new_invoice.total_sum = total_sum
        db.session.commit()
        flash('Your invoice has been created!', 'success')
        return redirect(url_for('invoices.invoice', invoice_id=new_invoice.id))

    return render_template('create_invoice.html', title='Create Invoice', form=form)


@invoices.route('/invoice/<int:invoice_id>', methods=['GET'])
def invoice(invoice_id):
    """Show the details of a invoice"""
    bill = Invoice.query.get_or_404(invoice_id)
    return render_template('invoice.html', invoice=bill)


@invoices.route('/invoice', methods=['GET', 'POST'])
def search_invoices():
    search = FilterForm()
    if request.method == 'POST':
        return list_invoices()
    return render_template('search_invoices.html', filter=search)


@invoices.route('/invoice/search', methods=['POST'])
def list_invoices():
    def _filter(q, it):
        """Filter Query by Invoice Type.

        :param q: SQLAlchemy Query
        :param it: Invoice Type
        :return: List of Invoices in the filtered Query
        """
        if it == InvoiceType.All.value[0]:  # it == 'All'
            q = q.order_by(Invoice.id.desc())
        else:
            q = q.filter(Invoice.type == it) \
                .order_by(Invoice.id.desc())
        return q.all()

    search = request.form

    date_from = search['date_from']
    date_till = search['date_till']

    if date_from:
        date_from = datetime.datetime.strptime(search['date_from'], '%Y-%m-%d')
    if date_till:
        date_till = datetime.datetime.strptime(search['date_till'], '%Y-%m-%d')
    invoice_type = int(search['invoice_type'])

    query = Invoice.query

    if not date_from and not date_till:  # no dates
        results = _filter(query, invoice_type)
    elif date_from and not date_till:  # date_from only
        query = query.filter(date_from <= Invoice.issue_date)
        results = _filter(query, invoice_type)
    elif not date_from and date_till:  # date_till only
        query = query.filter(date_till <= Invoice.issue_date)
        results = _filter(query, invoice_type)
    else:  # both dates
        query = query \
            .filter(date_from <= Invoice.issue_date) \
            .filter(date_till >= Invoice.issue_date)
        results = _filter(query, invoice_type)

    if not results:
        flash('No results found!', 'warning')
        return redirect(url_for('invoices.search_invoices'))
    else:
        # display results
        return render_template('list_invoices.html', invoices=results)


@invoices.route('/invoice/<int:invoice_id>/update', methods=['GET', 'POST'])
@login_required
@roles_required([Roles.ACCOUNTANT.value])
def update_invoice(invoice_id):
    current_invoice: Invoice = Invoice.query.get_or_404(invoice_id)
    form = InvoiceForm(request.form)
    if form.validate_on_submit():
        current_invoice.issue_date = form.issue_date.data
        current_invoice.due_date = form.due_date.data
        current_invoice.payment_form = form.payment_form.data
        current_invoice.type = form.type.data
        current_invoice.invoice_buyer = form.buyer.data

        for item in current_invoice.items:
            Item.query.filter_by(id=item.id).delete()

        total_sum = 0
        for item in form.items.data:
            new_item = Item(**item)
            new_item.total_price = new_item.count * new_item.price
            total_sum += new_item.total_price
            db.session.add(new_item)
            current_invoice.items.append(new_item)

        current_invoice.total_sum = total_sum

        db.session.commit()
        flash('Your invoice has been updated!', 'success')
        return redirect(url_for('invoices.invoice', invoice_id=invoice_id))
    elif request.method == 'GET':
        form.issue_date.data = current_invoice.issue_date
        form.due_date.data = current_invoice.due_date
        form.payment_form.data = current_invoice.payment_form
        form.type.data = current_invoice.type
        form.buyer.data = current_invoice.invoice_buyer

        current_item: Item
        for current_item in current_invoice.items:
            item = ItemForm()
            item.desc = current_item.desc
            item.count = current_item.count
            item.price = current_item.price
            item.unit = current_item.unit
            item.vat = current_item.vat

            form.items.append_entry(item)

    return render_template('create_invoice.html', title='Update Invoice', form=form)


@invoices.route('/invoice/<int:invoice_id>/delete', methods=['POST'])
@login_required
@roles_required([Roles.ACCOUNTANT.value])
def delete_invoice(invoice_id):
    bill = Invoice.query.get_or_404(invoice_id)
    db.session.delete(bill)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('invoices.search_invoices'))
