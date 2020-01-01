from app import db, create_app
from app.models import Post, User, Company, Contact, Invoice, Item
import json
import datetime as dt


def load_posts(file='../data/posts.json'):
    input_file = open(file, encoding='utf-8')
    json_array = json.load(input_file)

    for item in json_array:
        user = User.query.get(item['user_id'])
        post = Post(title=item['title'],
                    content=item['content'],
                    post_author=user)
        db.session.add(post)
    db.session.commit()


def load_companies(file='../data/companies.json'):
    input_file = open(file, encoding='utf-8')
    json_array = json.load(input_file)

    for item in json_array:
        company = Company(name=item['name'],
                          dic=item['dic'],
                          residence=item['residence'])
        db.session.add(company)
    db.session.commit()


def load_contacts(file='../data/contacts.json'):
    input_file = open(file, encoding='utf-8')
    json_array = json.load(input_file)

    for item in json_array:
        company = Company.query.get(item['company_id'])
        contact = Contact(name=item['name'],
                          residence=item['residence'],
                          ic=item['ic'],
                          dic=item['dic'],
                          phone=item['phone'],
                          email=item['email'],
                          contact_author=company)
        db.session.add(contact)
    db.session.commit()


def load_invoices(file='../data/invoices.json'):
    input_file = open(file, encoding='utf-8')
    json_array = json.load(input_file)

    for inv in json_array:
        company = Company.query.get(inv['company_id'])
        buyer = Contact.query.get(inv['buyer_id'])

        issue_date = dt.datetime.strptime(inv['issue_date'], '%Y-%m-%d')
        due_date = dt.datetime.strptime(inv['due_date'], '%Y-%m-%d')

        invoice = Invoice(issue_date=issue_date,
                          due_date=due_date,
                          payment_form=inv['payment_form'],
                          type=inv['type'],
                          invoice_buyer=buyer,
                          invoice_company=company)
        invoice.create_serial_number()
        db.session.add(invoice)
        load_invoice_items(inv['items'], invoice)
        invoice.total_sum = sum([item['total_price'] for item in inv['items']])
    db.session.commit()


def load_invoice_items(items, invoice):
    for item in items:
        it = Item(count=item['count'],
                  unit=item['unit'],
                  desc=item['desc'],
                  vat=item['vat'],
                  price=item['price'],
                  total_price=item['total_price'],
                  item_invoice=invoice)
        db.session.add(it)


def main():
    app = create_app()

    with app.app_context():
        load_posts()
        load_companies()
        load_contacts()
        load_invoices()


if __name__ == '__main__':
    main()
