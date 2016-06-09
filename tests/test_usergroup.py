import unittest
from LoginComponent.usergroup import UserGroup


class test_user(unittest.TestCase):
    """ Unittests for the user class """

    def setUp(self):
        self.empty_usergroup = UserGroup("emptygroup")
        self.filled_usergroup = UserGroup("filledgroup", ["user1", "user2"],
                                          ["group1", "group2"])

    # Create tests.
    def test_usergroup_constructor_name(self):
        self.assertEqual(self.empty_usergroup.name, "emptygroup")

    def test_usergroup_constructor_name_filled(self):
        self.assertEqual(self.filled_usergroup.name, "filledgroup")

    def test_usergroup_constructor_users_empty(self):
        self.assertEqual(self.empty_usergroup.users, [])

    def test_usergroup_constructor_groups_empty(self):
        self.assertEqual(self.empty_usergroup.groups, [])

    def test_usergroup_constructor_groups_empty(self):
        self.assertEqual(self.empty_usergroup.groups, [])

    def test_usergroup_constructor_users_filled(self):
        self.assertEqual(self.filled_usergroup.users, ["user1", "user2"])

    def test_usergroup_constructor_groups_filled(self):
        self.assertEqual(self.filled_usergroup.groups, ["group1", "group2"])

    def test_usergroup_get_name(self):
        self.assertEqual(self.empty_usergroup.get_name(), "emptygroup")

    def test_usergroup_set_name(self):
        self.empty_usergroup.set_name("newname")
        self.assertEqual(self.empty_usergroup.name, "newname")

    def test_usergroup_add_user(self):
        self.empty_usergroup.add_user("newuser")
        self.assertEqual(self.empty_usergroup.users, ["newuser"])

    def test_usergroup_add_group(self):
        self.empty_usergroup.add_group("newgroup")
        self.assertEqual(self.empty_usergroup.groups, ["newgroup"])

    def test_usergroup_remove_user(self):
        self.filled_usergroup.remove_user("user1")
        self.assertEqual(self.filled_usergroup.users, ["user2"])

    def test_usergroup_remove_group(self):
        self.filled_usergroup.remove_group("group1")
        self.assertEqual(self.filled_usergroup.groups, ["group2"])
