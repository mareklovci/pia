from datetime import datetime
from enum import Enum

from flask import current_app
from flask_login import UserMixin
from itsdangerous import SignatureExpired, TimedJSONWebSignatureSerializer as Serializer

from app import db, login_manager
from app.utils import get_count


class Roles(Enum):
    GUEST = 'guest'
    ADMIN = 'administrator'
    ACCOUNTANT = 'accountant'


class Payment(Enum):
    Cash = 1, 'Cash'
    CashOnDelivery = 2, 'Cash on Delivery'
    CreditCard = 3, 'Credit Card'
    BankTransfer = 4, 'Bank Transfer'


class InvoiceType(Enum):
    All = 1, 'All'
    Inbound = 2, 'Inbound'
    Outbound = 3, 'Outbound'


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
    invoices = db.relationship('Invoice', backref='invoice_author', lazy=True)

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
    payment_form = db.Column(db.Integer())  # forma uhrady
    type = db.Column(db.Integer())

    serial_id = db.Column(db.Integer())
    serial_number = db.Column(db.String(256))
    total_sum = db.Column(db.Integer())

    # Foreign keys
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))
    buyer_id = db.Column(db.Integer, db.ForeignKey('contact.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    # Relationships
    items = db.relationship('Item', backref='item_invoice', lazy='dynamic', collection_class=list)

    def create_serial_number(self):
        invoice_type = self.get_type()
        serial_number = ''  # initialize serial number
        q = Invoice.query.filter(Invoice.type == self.type).order_by(Invoice.id.desc()).all()

        # retrieve last invoice
        try:
            q = q[1]
        except IndexError:
            q = None

        # assign serial_id
        if q is None:
            self.serial_id = 1
        else:
            self.serial_id = q.serial_id + 1

        # create serial_number
        if invoice_type == InvoiceType.Outbound:
            serial_number = f'IO{self.serial_id:05d}'
        elif invoice_type == InvoiceType.Inbound:
            serial_number = f'II{self.serial_id:05d}'

        # assign serial number to attribute
        self.serial_number = serial_number

    def get_type(self) -> InvoiceType:
        identifier = [item.value for item in InvoiceType if item.value[0] == self.type][0]
        return InvoiceType(identifier)


class Item(db.Model):
    id = db.Column(db.Integer(), primary_key=True)

    # Fields
    count = db.Column(db.Float())
    unit = db.Column(db.String(50))
    desc = db.Column(db.String(256))
    vat = db.Column(db.Integer())  # % DPH (Value-added tax)
    price = db.Column(db.Float())

    # Calculated fields
    total_price = db.Column(db.Float())

    # Foreign keys
    invoice_id = db.Column(db.Integer, db.ForeignKey('invoice.id'))


class Company(db.Model):
    id = db.Column(db.Integer(), primary_key=True)

    name = db.Column(db.String(50), unique=True)
    dic = db.Column(db.String(50), unique=True)
    residence = db.Column(db.String(50), unique=False, default='')

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

    # Relationships
    invoices = db.relationship('Invoice', backref='invoice_buyer', lazy=True)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)

    # Foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"
