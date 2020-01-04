from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required

from app import db
from app.models import Company, Contact, Roles
from app.utils import roles_required
from app.companies.forms import ContactForm

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
    form = ContactForm()
    if form.validate_on_submit():
        comp = Company.query.get_or_404(1)
        new_contact = Contact(name=form.name.data,
                              residence=form.residence.data,
                              ic=form.ic.data,
                              dic=form.dic.data,
                              phone=form.phone.data,
                              email=form.email.data,
                              contact_author=comp)
        db.session.add(new_contact)
        db.session.commit()
        flash('Your contact has been created!', 'success')
        return redirect(url_for('companies.contact', contact_id=new_contact.id))
    return render_template('create_contact.html', title='Create Contact', form=form)


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
    current_contact: Contact = Contact.query.get_or_404(contact_id)
    form = ContactForm()
    if form.validate_on_submit():
        current_contact.name = form.name.data
        current_contact.residence = form.residence.data
        current_contact.dic = form.dic.data
        current_contact.ic = form.ic.data
        current_contact.email = form.email.data
        current_contact.phone = form.phone.data

        db.session.commit()
        flash('Your contact has been updated!', 'success')
        return redirect(url_for('companies.contact', contact_id=current_contact.id))
    elif request.method == 'GET':
        form.name.data = current_contact.name
        form.residence.data = current_contact.residence
        form.dic.data = current_contact.dic
        form.ic.data = current_contact.ic
        form.email.data = current_contact.email
        form.phone.data = current_contact.phone
    return render_template('create_contact.html', title='Update Contact', form=form)


@companies.route('/company', methods=['GET'])
def company(company_id=1):
    comp = Company.query.get_or_404(company_id)
    return render_template('company.html', company=comp)
