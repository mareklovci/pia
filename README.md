# pia
KIV/PIA

## Pre-filled data

## Users

Administrator and 2 users from each role

| Title         | email                | password   |
|---------------|----------------------|------------|
| Administrator | mareklovci@gmail.com | admin      |
| TestUser1     | testuser1@gmail.com  | testing321 |
| TestUser2     | TestUser2            | testing987 |

| Login    | password | Role          |
|----------|----------|---------------|
| Admin001 | 1234     | administrator |
| User0001 | 0001     | accountant    |
| User0002 | 0002     | accountant    |
| User0003 | 0003     | secretary     |
| User0004 | 0004     | secretary     |

## Invoices

Two invoices for each user.

## Create database from Model

```python
from accounting import db
from accounting import User, Post, Role, UserRoles
from accounting import create_app

app = create_app()
app.app_context().push()
db.create_all()
```

### Create default users

```python
from accounting import User, Post
from accounting import db

user_admin = User(username='admin', email='mareklovci@gmail.com', password='admin')
db.session.add(user_admin)

user_1 = User(username='TestUser1', email='user1@users.com', password='testing321')
db.session.add(user_1)

db.session.commit()
```

## Create secret key

```python
import secrets

secrets.token_hex(16)
```