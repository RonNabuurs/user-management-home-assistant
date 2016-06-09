import unittest
import os
from LoginComponent.usergroupmanager import UserGroupManager
from LoginComponent.usermanager import UserManager


class test_usergroupmanager(unittest.TestCase):
    'Unit tests for the usergroupmanager'

    def setUp(self):
        self.user_group_manager = UserGroupManager()
        self.user_group_manager.create_group('test_group')
        self.test_dict = ''

    def tearDown(self):
        if os.path.exists('groups.yaml'):
            os.remove('groups.yaml')
        if os.path.exists('users.yaml'):
            os.remove('users.yaml')

    # Create tests.
    def test_create_group(self):
        self.assertEqual(self.user_group_manager.create_group('test_group2'),
                         True)

    def test_create_group_duplicate(self):
        self.assertEqual(self.user_group_manager.create_group('test_group'),
                         False)

    def test_create_group_not_string_name(self):
        self.assertEqual(self.user_group_manager.create_group(1), False)

    def test_create_group_weird_string(self):
        self.assertEqual(self.user_group_manager.create_group('~*&^%$#'
                                                              ), True)

    def test_create_group_same_string_int_name(self):
        self.assertEqual(self.user_group_manager.create_group('1'), False)

    def test_add_user_to_usergroup(self):
        self.user_manager = UserManager()
        self.user_manager.create_user('test_user',
                                      'test_password')
        self.assertEqual(self.user_group_manager.add_user_to_usergroup(
            'test_user', self.user_group_manager.user_groups[0],
            self.user_manager),
            True)

    # Read tests.
    def test_read_group_list(self):
        self.assertEqual(len(self.user_group_manager.read_groups()), 1)

    def test_read_group_null(self):
        self.user_group_manager.delete_usergroup('test_group')
        self.assertEqual(len(self.user_group_manager.read_groups()), 0)

    # Update tests.
    def test_update_group_name(self):
        self.assertEqual(self.user_group_manager.update_usergroup_name(
            'test_group', 'test_group2'), True)

    def test_update_group_name_to_int(self):
        self.assertEqual(self.user_group_manager.update_usergroup_name(
            'test_group', 1), False)

    def test_update_user_in_usergroup(self):
        self.user_manager = UserManager()
        self.user_manager.create_user('test_user', 'test_password')
        self.user_manager.create_user('test_user_new', 'test_password')
        self.user_group_manager.add_user_to_usergroup('test_user',
                                                      self.user_group_manager.
                                                      user_groups[0],
                                                      self.user_manager)
        self.assertEqual(self.user_group_manager.update_user_in_usergroup(
            'test_user', 'test_user_new', self.user_manager), True)

    def test_update_user_in_usergroup_not_existant_user(self):
        self.user_manager = UserManager()
        self.user_manager.create_user('test_user', 'test_password')
        self.user_group_manager.add_user_to_usergroup('test_user',
                                                      self.user_group_manager.
                                                      user_groups[0],
                                                      self.user_manager)
        self.assertEqual(self.user_group_manager.update_user_in_usergroup(
            'test_user', 'not_existing', self.user_manager), False)

    # Delete tests.
    def test_delete_group(self):
        self.assertEqual(self.user_group_manager.delete_usergroup(
            'test_group'), True)

    def test_delete_group_not_existing(self):
        self.assertEqual(self.user_group_manager.delete_usergroup(
            'not_existant'), False)

    def test_delete_user_from_usergroup(self):
        self.user_manager = UserManager()
        self.user_manager.create_user('test_user',
                                      'test_password')
        self.user_group_manager.add_user_to_usergroup('test_user',
                                                      self.user_group_manager.
                                                      user_groups[0],
                                                      self.user_manager)
        self.assertEqual(self.user_group_manager.remove_user_from_usergroup(
            'test_user', self.user_group_manager.user_groups[0]), True)

    def test_delete_user_from_usergroup_not_existing(self):
        self.assertEqual(self.user_group_manager.remove_user_from_usergroup(
            'test_user', self.user_group_manager.user_groups[0]), False)
