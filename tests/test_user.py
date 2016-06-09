import unittest
from LoginComponent.user import User


class test_user(unittest.TestCase):
    """ Unittests for the user class """

    def setUp(self):
        self.user = User("testuser", "secretpass")
        self.hasheduser = User("testuser", "secretpass", True)

    # Create tests.
    def test_user_constructor_username(self):
        self.assertEqual(self.user.username, "testuser")

    def test_user_constructor_password(self):
        self.assertEqual(self.user.password, "secretpass")

    def test_user_constructor_hashed_username(self):
        self.assertEqual(self.hasheduser.username, "testuser")

    def test_user_constructor_hashed_password(self):
        self.assertNotEquals(self.hasheduser.password, "secretpass")

    def test_user_get_username(self):
        self.assertEqual(self.user.get_username(), "testuser")

    def test_user_get_password(self):
        self.assertEqual(self.user.get_password(), "secretpass")

    def test_user_set_username(self):
        self.user.set_username("newpass")
        self.assertNotEquals(self.user.username, "secretpass")
        self.assertEquals(self.user.username, "newpass")

    def test_user_set_password(self):
        self.user.set_password("newpass")
        self.assertNotEquals(self.user.password, "secretpass")
        self.assertEquals(self.user.password, "newpass")

    def test_user_set_password_and_hash(self):
        self.user.set_password_and_hash("newpass")
        self.assertNotEquals(self.user.password, "secretpass")
        self.assertNotEquals(self.user.password, "newpass")
