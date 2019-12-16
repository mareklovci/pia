from flask_testing import TestCase

from app.models import User
from app import create_app, db
import unittest


class UsersTestCase(TestCase):
    """A base test case"""

    SQLALCHEMY_DATABASE_URI = "sqlite://"
    TESTING = True

    def create_app(self):
        # pass in test configuration
        return create_app(self)

    def setUp(self) -> None:
        db.create_all()

    def tearDown(self) -> None:
        db.session.remove()
        db.drop_all()

    # noinspection PyArgumentList
    def test_user_creation(self):
        user = User(username='Test1',
                    password='12345',
                    email='test@a.a')
        db.session.add(user)
        db.session.commit()

        # this works
        self.assertIn(user, db.session)  # assert user in db.session


if __name__ == '__main__':
    unittest.main()
