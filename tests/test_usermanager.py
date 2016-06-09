import unittest
import os
from LoginComponent.usermanager import UserManager


class test_groupmanager(unittest.TestCase):
    """Unit tests for groupmanager"""

    def setUp(self):
        self.user_manager = UserManager()
        self.user_manager.create_user('test_user', 'test_password')
        self.test_dict = ''

    def tearDown(self):
        if os.path.exists('users.yaml'):
            os.remove('users.yaml')

    # Create tests.
    def test_create_user(self):
        self.assertEqual(self.user_manager.create_user('test_user2',
                                                       'test_password'), True)

    def test_create_user_duplicate(self):
        self.assertEqual(self.user_manager.create_user('test_user',
                                                       'test_password'), False)

    def test_create_user_username_not_string(self):
        self.assertEqual(self.user_manager.create_user(1, 'test_password'),
                         False)

    def test_create_user_password_not_string(self):
        self.assertEqual(self.user_manager.create_user('test_user2', 1),
                         True)

    def test_create_user_both_not_string(self):
        self.assertEqual(self.user_manager.create_user(1, 1), False)

    # Read tests.
    def test_read_user_list(self):
        self.assertEqual(len(self.user_manager.read_users()), 1)

    def test_read_group_null(self):
        self.user_manager.delete_user('test_user')
        self.assertEqual(len(self.user_manager.read_users()), 0)

    # Update tests.
    def test_update_group_name(self):
        self.assertEqual(self.user_manager.update_user_username(
            'test_user', 'test_user_new'), True)

    # Delete tests.
    def test_delete_user(self):
        self.assertEqual(self.user_manager.delete_user(
            'test_user'), True)

    def test_delete_user_not_existing(self):
        self.assertEqual(self.user_manager.delete_user(
          'not_existant'), False)
