from app import db, create_app
from app.models import Post, User, Company, Contact
import json


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


def load_invoices():
    pass


def main():
    app = create_app()

    with app.app_context():
        load_posts()
        load_companies()
        load_contacts()


if __name__ == '__main__':
    main()
