import hashlib


class User:
    """Stores the username and password of a user."""

    def __init__(self, username, password, hash_password=False):
        self.set_username(username)
        if hash_password:
            self.set_password_and_hash(password)
        else:
            self.set_password(password)

    def get_username(self):
        """
        Returns the username of this user.
        :return:
        """
        return self.username

    def get_password(self):
        """
        Returns the hashed password of this user.
        :return:
        """
        return self.password

    def set_username(self, new_username):
        """
        Sets the username of this user to the new_username.
        :param new_username: The new username of this user.
        :return:
        """
        self.username = new_username

    def set_password(self, new_password):
        """
        Sets the password of this user to the new_password.
        :param new_password: The new password of this user.
        :return:
        """
        self.password = new_password

    def set_password_and_hash(self, new_password):
        """
        Sets the password of this user and hashes it with sha512. Before
        hashing the password is converted to a string and encoded utf-8.
        :param new_password: The new password to be hashed.
        :return:
        """
        self.password = hashlib.sha512(str(new_password).encode(
                "utf-8")).hexdigest()
