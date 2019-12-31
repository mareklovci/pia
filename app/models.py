from datetime import datetime
from enum import Enum

from flask import current_app
from flask_login import UserMixin
from itsdangerous import SignatureExpired, TimedJSONWebSignatureSerializer as Serializer

from app import db, login_manager


class Roles(Enum):
    GUEST = 'guest'
    ADMIN = 'administrator'
    ACCOUNTANT = 'accountant'
    SECRETARY = 'secretary'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)

    # User information
    name = db.Column(db.String(100), nullable=False, server_default='')
    birth_number = db.Column(db.String(100), nullable=False, server_default='')
    address = db.Column(db.String(100), nullable=False, server_default='')
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(50), nullable=False, server_default='')
    card_number = db.Column(db.String(50), nullable=False, server_default='')
    account_number = db.Column(db.String(50), nullable=False, server_default='')

    # User authentication information
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(60), nullable=False)

    # Extras
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')

    # Foreign keys
    role_id = db.Column(db.Integer(), db.ForeignKey('role.id'))

    # Relationships
    posts = db.relationship('Post', backref='post_author', lazy=True, cascade='delete')

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except SignatureExpired:
            return None
        return User.query.get(user_id)

    def is_admin(self):
        return self.user_role.name == Roles.ADMIN.value

    def allowed(self, roles):
        return self.user_role.name in roles

    def __repr__(self):
        return f'User({self.username}, {self.email}, {self.image_file})'


# Define the Role data model
class Role(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)

    # Relationships
    users = db.relationship('User', backref='user_role', lazy=True)


class Invoice(db.Model):
    id = db.Column(db.Integer(), primary_key=True)

    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)  # datum vystaveni
    issue_date = db.Column(db.DateTime())  # datum zdanitelneho plneni
    due_date = db.Column(db.DateTime())  # splatnost
    payment_form = db.Column(db.String(256))  # forma uhrady

    serial_number = db.Column(db.Integer(), db.Sequence('invoice_serial_number_seq'))
    total_sum = db.Column(db.Integer())

    # Relationships
    company = db.Column(db.Integer, db.ForeignKey('company.id'))
    items = db.relationship('Item', backref='item_invoice', lazy='dynamic', collection_class=list)


class Item(db.Model):
    id = db.Column(db.Integer(), primary_key=True)

    # Fields
    count = db.Column(db.Float())
    unit = db.Column(db.String(50))
    desc = db.Column(db.String(255))
    vat = db.Column(db.Integer())  # % DPH (Value-added tax)
    price = db.Column(db.Float())

    # Calculated fields
    total_price = db.Column(db.Float())

    # Relationships
    invoice = db.Column(db.Integer, db.ForeignKey('invoice.id'))


class Company(db.Model):
    id = db.Column(db.Integer(), primary_key=True)

    name = db.Column(db.String(50), unique=True)
    dic = db.Column(db.String(50), unique=True)
    residence = db.Column(db.String(50), unique=False, default='')

    # Foreign keys
    secretary_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    # Relationships
    invoices = db.relationship('Invoice', backref='invoice_company', lazy=True)
    contacts = db.relationship('Contact', backref='contact_author', lazy=True)


class Contact(db.Model):
    id = db.Column(db.Integer(), primary_key=True)

    name = db.Column(db.String(50), unique=True)
    residence = db.Column(db.String(50), unique=False, default='')
    ic = db.Column(db.String(50), unique=True)
    dic = db.Column(db.String(50), unique=True)
    phone = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    # Foreign keys
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)

    # Foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"
