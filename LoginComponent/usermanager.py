import yaml
import os
import logging
from LoginComponent.user import User
from LoginComponent.scripts import utils

_LOGGER = logging.getLogger(__name__)
USERS_YAML_FILE = "users.yaml"


class UserManager:
    """Creates, updates, reads and deletes users."""

    def __init__(self):
        self.users = self.read_users()

    def create_user(self, username, password):
        """
        Creates a user and adds it to the yaml configuration file.
        :param username: The name of the user you'd like to create.
        :param password: The password of the user you'd like to create.
        :return: Returns true if the operation was successful and false if
        the operation failed.
        """
        if utils.parse_int(username) is not None:
            _LOGGER.error("An integer as username is not supported!")
            return False

        for user in self.users:
            if user.get_username() == username:
                logging.error("A user with the username \"" + username +
                              "\" already exists!")
                return False

        self.users.append(User(username, password, True))
        self.write_users_to_yaml()
        return True

    def write_users_to_yaml(self):
        """ Write the list of users in self.users to the users.yaml file. """
        with open(USERS_YAML_FILE, 'w') as outfile:
            users_dict = self.convert_users_to_dict(self.users)
            outfile.write(yaml.dump(users_dict, default_flow_style=False))

    def convert_users_to_dict(self, user_list):
        """
        Convert a list of users to a dict.
        :param user_list: A list of user objects.
        :return: Returns the dict representation of the list of users.
        """
        users_dict = {}
        for user in user_list:
                users_dict[user.get_username()] = {}
                users_dict[user.get_username()]["password"] = \
                    user.get_password()
        return users_dict

    def convert_dict_to_users(self, user_dict):
        """
        Convert a dict of users to a list of user objects.
        :param user_dict: A dict filled with users.
        :return: Returns a list if users if there were users in the given
        dict. If the given dict did not contain any users, it'll return an
        empty list.
        """
        users = []
        for username, user_information in user_dict.items():
            users.append(User(username, user_information['password']))
        return users

    def read_users(self):
        """
        Reads all users from the users.yaml file.
        :return: Returns a list of users if they were successfully loaded,
        or an empty is if not.
        """
        if os.path.isfile(USERS_YAML_FILE):
            user_dict = yaml.load(open(USERS_YAML_FILE, 'r'))
            if user_dict is not None:
                return self.convert_dict_to_users(user_dict)
        return []

    def delete_user(self, username):
        """
        Deletes users from users.yaml file.
        :return: Returns true if the operation was successful and false if
        the operation failed.
        """
        for user in self.users:
            if user.get_username() == username:
                self.users.remove(user)
                self.write_users_to_yaml()
                return True
        return False

    def update_user_username(self, old_username, new_username):
        """
        Update the username of a single user.
        :param old_username: The current username of the user whose username
        you'd like to update.
        :param new_username: The username you'd like to change the current
        username to.
        :return: Returns true if the operation was successful and false if
        the operation failed.
        """
        if utils.parse_int(new_username) is not None:
            _LOGGER.error("An integer as username is not supported!")
            return False

        if new_username not in (user.get_username() for user in self.users):
            for user in self.users:
                if user.get_username() == old_username:
                    user.set_username(new_username)
                    self.write_users_to_yaml()
                    return True
        return False

    def update_user_password(self, username, password):
        """
        Update the password of a single user.
        :param username: The username of the user whose password
        you'd like to change.
        :param password: The new password you'd like to change the current
        password of that user to.
        :return: Returns true if the operation was successful and false if
        the operation failed.
        """
        for user in self.users:
            if user.get_username() == username:
                user.set_password_and_hash(password)
                self.write_users_to_yaml()
                return True
        return False

    def get_users(self):
        """
        Returns the users in this usermanager.
        :return: The users in this usermanager.
        """
        return self.users
