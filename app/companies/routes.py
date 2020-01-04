from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required

from app import db
from app.models import Company, Contact, Roles
from app.utils import roles_required

companies = Blueprint('companies', __name__)


@companies.route('/contact', methods=['GET'])
def list_contacts():
    page = request.args.get('page', default=1, type=int)
    contacts = Contact.query.order_by(Contact.name.asc()).paginate(page=page, per_page=5)
    return render_template('list_contacts.html', contacts=contacts)


@companies.route('/contact/<int:contact_id>', methods=['GET'])
def contact(contact_id):
    cont = Contact.query.get_or_404(contact_id)
    return render_template('contact.html', contact=cont)


@companies.route('/contact/create', methods=['GET', 'POST'])
@login_required
@roles_required([Roles.ACCOUNTANT.value])
def create_contact():
    pass


@companies.route('/contact/<int:contact_id>/delete', methods=['POST'])
@login_required
@roles_required([Roles.ACCOUNTANT.value])
def delete_contact(contact_id):
    cont = Contact.query.get_or_404(contact_id)
    db.session.delete(cont)
    db.session.commit()
    flash('Your contact has been deleted!', 'success')
    return redirect(url_for('companies.list_contacts'))


@companies.route('/contact/<int:contact_id>/update', methods=['GET', 'POST'])
@login_required
@roles_required([Roles.ACCOUNTANT.value])
def update_contact(contact_id):
    pass


@companies.route('/company', methods=['GET'])
def company(company_id=1):
    comp = Company.query.get_or_404(company_id)
    return render_template('company.html', company=comp)
