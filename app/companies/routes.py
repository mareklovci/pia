from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import Contact, Company
from app import db

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


@companies.route('/contact/<int:contact_id>/delete', methods=['POST'])
def delete_contact(contact_id):
    cont = Contact.query.get_or_404(contact_id)
    db.session.delete(cont)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('companies.list_contacts'))


@companies.route('/contact/<int:contact_id>/update', methods=['GET', 'POST'])
def update_contact(contact_id):
    pass


@companies.route('/company', methods=['GET'])
def company(company_id=1):
    comp = Company.query.get_or_404(company_id)
    return render_template('company.html', company=comp)
