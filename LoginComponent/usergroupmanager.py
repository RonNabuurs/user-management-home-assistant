import logging
import yaml
import os
from LoginComponent.usergroup import UserGroup
from LoginComponent.scripts import utils

_LOGGER = logging.getLogger(__name__)
GROUPS_YAML_FILE = "groups.yaml"


class UserGroupManager:
    """Creates, updates, reads and deletes UserGroups."""

    def __init__(self):
        self.user_groups = self.read_groups()

    def create_group(self, group_name):
        """ Creates a UserGroup and adds it to the groups.yaml configuration
        file.
        :param group_name: The name of the group you want to create.
        :return: Returns true if the operation was successful and false if
        the operation failed.
        """
        if utils.parse_int(group_name) is not None:
            _LOGGER.error("An integer as usergroup name is not supported!")
            return False

        for user_group in self.user_groups:
            if user_group.get_name() == group_name:
                return False

        self.user_groups.append(UserGroup(group_name))
        self.write_user_groups_to_yaml()
        return True

    def write_user_groups_to_yaml(self):
        """
        Writes all user groups in self.user_groups to the groups.yaml file.
        """
        with open(GROUPS_YAML_FILE, 'w') as outfile:
            groups_dict = self.convert_groups_to_dict(self.user_groups)
            outfile.write(yaml.dump(groups_dict, default_flow_style=False))

    def convert_groups_to_dict(self, usergroups_list):
        """
        Converts the given list of usergroups to a dict.
        :param usergroups_list: The list of usergroups to convert to a dict.
        :return: Returns a dict of user groups if user groups were found,
        or an empty list if none were found.
        """
        groups_dict = {}
        for user_group in usergroups_list:
            groups_dict[user_group.get_name()] = {}
            groups_dict[user_group.get_name()]["users"] = []
            groups_dict[user_group.get_name()]["groups"] = []
            for i in range(0, len(user_group.get_groups())):
                groups_dict[user_group.get_name()]["groups"].append(
                    user_group.get_groups()[i])
            for i in range(0, len(user_group.get_users())):
                groups_dict[user_group.get_name()]["users"].append(
                    user_group.get_users()[i])
        return groups_dict

    def convert_dict_to_groups(self, usergroup_dict):
        """
        Converts the given dict of user groups to a list.
        :param usergroup_dict: A dict containing usergroups.
        :return:Returns true if the operation was successful and false if
        the operation failed.
        """
        user_groups = []
        for usergroup_name, user_group in usergroup_dict.items():
            user_groups.append(UserGroup(usergroup_name,
                                         list(user_group["users"]),
                                         list(user_group["groups"])))
        return user_groups

    def read_groups(self):
        """
        Reads all UserGroups from the groups.yaml file.
        :return: Returns a list of users if a list of users was found.
        Returns an empty list if none were found.
        """
        if os.path.isfile(GROUPS_YAML_FILE):
            group_dict = yaml.load(open(GROUPS_YAML_FILE, 'r'))
            if group_dict is not None:
                return self.convert_dict_to_groups(group_dict)
        return []

    def delete_usergroup(self, groupname):
        """
        Deletes groups from groups.yaml file.
        :param groupname: The group you'd like to delete from the
        groups.yaml file.
        :return: Returns true if the operation was successful and false if
        the operation failed.
        """
        for group in self.user_groups:
            if group.get_name() == groupname:
                self.user_groups.remove(group)
                self.write_user_groups_to_yaml()
                return True
        return False

    def add_user_to_usergroup(self, username, user_group, usermanager):
        """
        Adds a user to a usergroup.
        :param username: The username of the user to add to a  usergroup.
        :param user_group: The name of the usergroup to add a user to.
        :return: Returns true if the operation was successful and false if
        the operation failed.
        """
        if username in (user.get_username() for user in usermanager.users) \
                and username not in user_group.users:
            user_group.users.append(username)
            self.write_user_groups_to_yaml()
            return True
        return False

    def add_group_to_usergroup(self, groupname, user_group):
        """
        Add a Home Assistant group to a usergroup.
        :param groupname: The name of the Home Assistant group to add to a
        usergroup.
        :param user_group: The name of the usergroup to add a user to.
        :return: Returns true if the operation was successful and false if
        the operation failed.
        """
        if groupname not in user_group.groups:
            user_group.groups.append(groupname)
            self.write_user_groups_to_yaml()
            return True
        return False

    def remove_user_from_usergroup(self, username, user_group):
        """
        Remove a user from a usergroup.
        :param username: The username of the user to remove from a usergroup.
        :param user_group: The name of the usergroup to remove a user from.
        :return: Returns true if the operation was successful and false if
        the operation failed.
        """
        if username in user_group.users:
            user_group.users.remove(username)
            self.write_user_groups_to_yaml()
            return True
        return False

    def remove_group_from_usergroup(self, groupname, user_group):
        """
        Remove a Home Assistant group from a usergroup.
        :param groupname: The name of the Home Assistant group to remove from
        a usergroup.
        :param usergroupname: The name of the usergroup to remove a user from.
        :return: Returns true if the operation was successful and false if
        the operation failed.
        """
        if groupname in user_group.groups:
            user_group.groups.remove(groupname)
            self.write_user_groups_to_yaml()
            return True
        return False

    def update_user_in_usergroup(self, old_username, new_username,
                                 usermanager):
        """
        Goes through all user groups and replaces all occurences of the
        old_username with the new_username.
        :param old_username: The username you want to replace.
        :param new_username: The username you want the old username to be
        replaced with.
        :return: Returns true if the operation was successful and false if
        the operation failed.
        """
        if new_username in (user.get_username() for user in usermanager.users):
            for user_group in self.user_groups:
                for i in range(len(user_group.users)):
                    if user_group.users[i] == old_username:
                        user_group.users[i] = new_username
                        break
                else:
                    return True
                self.write_user_groups_to_yaml()
            return True
        return False

    def update_usergroup_name(self, old_name, new_name):
        """
        Changes the name of the usergroup named old_name to new_name.
        :param old_name: The current name of the usergroup.
        :param new_name: The new name of the usergroup.
        :return: Returns true if the operation was successful and false if
        the operation failed.
        """
        if utils.parse_int(new_name) is not None:
            _LOGGER.error("An integer as usergroup name is not supported!")
            return False

        if new_name not in (usergroup.get_name() for usergroup in
                            self.user_groups):
            for usergroup in self.user_groups:
                if usergroup.get_name() == old_name:
                    usergroup.set_name(new_name)
                    self.write_user_groups_to_yaml()
                    return True
        return False

    def get_usergroups(self):
        """
        Returns the usergroups in this usergroupmanager.
        :return: The usergroups in this usergroupmanager.
        """
        return self.user_groups
