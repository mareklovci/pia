from flask import Blueprint, render_template, request
from app.models import Contact

companies = Blueprint('companies', __name__)


@companies.route('/contact', methods=['GET'])
def list_contacts():
    page = request.args.get('page', default=1, type=int)
    contacts = Contact.query.order_by(Contact.name.desc()).paginate(page=page, per_page=5)
    return render_template('list_contacts.html', contacts=contacts)


@companies.route('/contact/<int:contact_id>', methods=['GET'])
def contact(contact_id):
    cont = Contact.query.get_or_404(contact_id)
    return render_template('contact.html', contact=cont)
