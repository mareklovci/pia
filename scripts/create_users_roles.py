from app import bcrypt, create_app, db
from app.models import Role, Roles, User


# noinspection PyArgumentList
def main():
    app = create_app()

    with app.app_context():

        # Create 'Administrator' role
        administrator = Role(name=Roles.ADMIN.value)

        if not Role.query.filter(Role.name == Roles.ADMIN.value).first():
            db.session.add(administrator)

        # Create 'Accountant' role
        accountant = Role(name=Roles.ACCOUNTANT.value)

        if not Role.query.filter(Role.name == Roles.ACCOUNTANT.value).first():
            db.session.add(accountant)

        # Create 'Administrator'
        admin001 = User(name='Admin Adminovic',
                        birth_number='000000/0000',
                        address='Address 1',
                        email='admin001@test.com',
                        phone='000 000 000',
                        card_number='00000000',
                        account_number='00000000',
                        username='Admin001',
                        password=hash_password('1234'),
                        role_id=administrator.id)

        if not User.query.filter(User.username == 'Admin001').first():
            db.session.add(admin001)

        # Create 'Users'
        user001 = User(name='User001 Userovic',
                       birth_number='000000/0000',
                       address='Address 2',
                       email='user0001@test.com',
                       phone='000 000 000',
                       card_number='00000000',
                       account_number='00000000',
                       username='User0001',
                       password=hash_password('0001'),
                       role_id=accountant.id)

        user002 = User(name='User002 Userovic',
                       birth_number='000000/0000',
                       address='Address 3',
                       email='user0002@test.com',
                       phone='000 000 000',
                       card_number='00000000',
                       account_number='00000000',
                       username='User0002',
                       password=hash_password('0002'),
                       role_id=accountant.id)

        if not User.query.filter(User.username == 'User001').first():
            db.session.add(user001)

        if not User.query.filter(User.username == 'User002').first():
            db.session.add(user002)

        db.session.commit()


def hash_password(password):
    return bcrypt.generate_password_hash(password).decode('utf-8')


if __name__ == '__main__':
    main()
