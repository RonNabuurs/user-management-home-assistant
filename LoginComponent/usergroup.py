class UserGroup:
    """Stores users and the Home Assistant groups they may access."""

    def __init__(self, name, users=None, groups=None):
        self.name = name
        if users is None:
            self.users = []
        else:
            self.users = users
        if groups is None:
            self.groups = []
        else:
            self.groups = groups

    def get_users(self):
        """
        Returns the list of users in this usergroup.
        :return: The list of users in this usergroup.
        """
        return self.users

    def get_groups(self):
        """
        Returns the list of Home Assistant groups in this usergroup.
        :return: The list of Home Assistant groups in this usergroup.
        """
        return self.groups

    def add_user(self, user):
        """
        Adds a user to this UserGroup.
        :param user: The username of the user you'd like to add.
        """
        self.users.append(user)

    def add_group(self, group):
        """
        Adds a Home Assistant group to this UserGroup.
        :param group: The Home Assistant group you'd like to add.
        """
        self.groups.append(group)

    def remove_user(self, user):
        """
        Removes a user from this UserGroup.
        :param user: The username of the user you'd like to remove.
        """
        self.users.remove(user)

    def remove_group(self, group):
        """
        Removes a Home Assistant group from this UserGroup.
        :param group: The Home Assistant group you'd like to remove.
        """
        self.groups.remove(group)

    def get_name(self):
        """
        Returns the name of this usergroup.
        :return: The name of this usergroup.
        """
        return self.name

    def set_name(self, name):
        """
        Sets the name of this UserGroup to the given name.
        :param name: The new name of this UserGroup.
        """
        self.name = name
