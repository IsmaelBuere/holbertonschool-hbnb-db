# tests/test_user.py

import unittest
from src import create_app, db
from src.models.user import User
from src.persistence.repository import RepositoryManager
from src.config import get_config

class TestUserRepository(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config.from_object(get_config())
        self.app.config['TESTING'] = True
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.repo = RepositoryManager()
        self.repo.init_app(self.app)
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_user_in_memory(self):
        self.app.config['REPOSITORY'] = 'memory'
        self.repo.init_app(self.app)
        self._clear_users_table()
        user_data = {
            "email": "test@example.com",
            "first_name": "Test",
            "last_name": "User",
            "password": "password",
            "is_admin": False
        }
        user = User.create(user_data)
        self.assertIsNotNone(user.id)
        self.assertEqual(user.email, "test@example.com")

    def test_create_user_in_file(self):
        self.app.config['REPOSITORY'] = 'file'
        self.repo.init_app(self.app)
        self._clear_users_table()
        user_data = {
            "email": "test2@example.com",
            "first_name": "Test2",
            "last_name": "User2",
            "password": "password2",
            "is_admin": False
        }
        user = User.create(user_data)
        self.assertIsNotNone(user.id)
        self.assertEqual(user.email, "test2@example.com")

    def test_create_user_in_db(self):
        self.app.config['REPOSITORY'] = 'db'
        self.repo.init_app(self.app)
        self._clear_users_table()
        user_data = {
            "email": "test3@example.com",
            "first_name": "Test3",
            "last_name": "User3",
            "password": "password3",
            "is_admin": False
        }
        user = User.create(user_data)
        self.assertIsNotNone(user.id)
        self.assertEqual(user.email, "test3@example.com")

    def _clear_users_table(self):
        User.query.delete()
        db.session.commit()

if __name__ == "__main__":
    unittest.main()