from app import bcrypt, create_app, db
from app.models import Role, User, Roles


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

        # Create 'Secretary' role
        secretary = Role(name=Roles.SECRETARY.value)

        if not Role.query.filter(Role.name == Roles.SECRETARY.value).first():
            db.session.add(secretary)

        # Create 'Administrator'
        admin001 = create_user('Admin001', '1234', 'admin001@test.com', administrator)

        if not User.query.filter(User.username == 'Admin001').first():
            db.session.add(admin001)

        # Create 'Users'
        user001 = create_user('User0001', '0001', 'user0001@test.com', accountant)
        user002 = create_user('User0002', '0002', 'user0002@test.com', accountant)
        user003 = create_user('User0003', '0003', 'user0003@test.com', secretary)
        user004 = create_user('User0004', '0004', 'user0004@test.com', secretary)

        if not User.query.filter(User.username == 'User001').first():
            db.session.add(user001)

        if not User.query.filter(User.username == 'User002').first():
            db.session.add(user002)

        if not User.query.filter(User.username == 'User003').first():
            db.session.add(user003)

        if not User.query.filter(User.username == 'User004').first():
            db.session.add(user004)

        db.session.commit()


# noinspection PyArgumentList
def create_user(username, password, email, role: Role):
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    user = User(username=username,
                email=email,
                password=hashed_password,
                role_id=role.id)
    return user


if __name__ == '__main__':
    main()
