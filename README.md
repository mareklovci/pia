# pia
KIV/PIA

## Users

| Title         | email                | password   |
|---------------|----------------------|------------|
| Administrator | mareklovci@gmail.com | admin      |
| TestUser1     | testuser1@gmail.com  | testing321 |
| TestUser2     | TestUser2            | testing987 |

## Create database from Model

```python
from accounting import db
from accounting import User, Post
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