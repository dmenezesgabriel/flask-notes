import unittest
from src import create_app
from src.extensions import db
from src.models import User
from config import TestConfig


class UserModelCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_hashing(self):
        user = User(username='gabriel', email='gabriel@example.com')
        user.set_password('123')
        self.assertFalse(user.check_password('456'))
        self.assertTrue(user.check_password('123'))

    def test_avatar(self):
        user = User(username='gabriel', email='gabriel@example.com')
        self.assertEqual(user.avatar(128), ('https://www.gravatar.com/avatar/'
                                            '4f5949422fb4d90d82141bac43ee654d'
                                            '?d=identicon&s=128'))


if __name__ == '__main__':
    unittest.main(verbosity=2)
