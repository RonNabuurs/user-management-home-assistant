"""
LoginComponent cli
"""

import click

from LoginComponent.usermanager import UserManager
from LoginComponent.usergroupmanager import UserGroupManager
from LoginComponent.scripts import utils

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

METAVAR_COMMAND = "<options>"

SHORT_ARGUMENT_USERNAME = "-u"
LONG_ARGUMENT_USERNAME = "--username"
METAVAR_USERNAME = "<username>"
HELP_USERNAME = "The username of the user you'd like to add."

SHORT_ARGUMENT_PASSWORD = "-p"
LONG_ARGUMENT_PASSWORD = "--password"
METAVAR_PASSWORD = "<password>"
HELP_PASSWORD = "The password of the user you'd like to add/change."
SHORT_HELP_CREATE_USER = "Creates a user and adds it to the yaml " \
                         "configuration file."

SHORT_ARGUMENT_USERGROUP = "-ug"
LONG_ARGUMENT_USERGROUP = "--user-group"
METAVAR_USERGROUP = "<name>"
HELP_CREATE_USERGROUP = "The name of the group you'd like to add."
HELP_READ_USERGROUP = "The name of the group you'd like to read the data " \
                        "from."
SHORT_HELP_CREATE_GROUP = "Creates a usergroup and adds it to the yaml " \
                          "configuration file."

SHORT_HELP_UPDATE_USER = "Edit a user."

SHORT_HELP_DELETE_USER = "Deletes a user by given username and " \
                        "updates the yaml configuration file."
SHORT_HELP_DELETE_GROUP = "Deletes a usergroup by given usergroupname and " \
                            "configuration file."
HELP_DELETE_USERGROUP = "The name of the usergroup you'd like to delete."
SHORT_HELP_READ_USERS = "Returns a list of all users."
SHORT_HELP_READ_USER = "Returns a user based on the given username."

SHORT_HELP_ADD_USER_TO_USERGROUP = "Adds a user to a usergroup"
HELP_UPDATE_USERGROUP = "The name of the usergroup you'd like to update."
SHORT_HELP_ADD_GROUP_TO_USERGROUP = "Adds a group to a usergroup"
SHORT_HELP_REMOVE_USER_FROM_USERGROUP = "Removes a user from a usergroup"
SHORT_HELP_REMOVE_GROUP_FROM_USERGROUP = "Removes a group to from a usergroup"

SHORT_ARGUMENT_GROUP = "-g"
LONG_ARGUMENT_GROUP = "--groupname"
METAVAR_GROUP = "<name>"
HELP_CREATE_GROUP = "The name of the Home Assistant group you'd like " \
                    "to add to the usergroup."
SHORT_HELP_READ_GROUPS = "Returns a list of all groups and their users."
SHORT_HELP_READ_GROUP = "Returns a group based on the given groupname."

SHORT_ARGUMENT_USERGROUP_NAME = "-n"
LONG_ARGUMENT_USERGROUP_NAME = "--new-name"
METAVAR_USERGROUP_NAME = "<name>"
HELP_USERGROUP_NAME = "The new name of this usergroup."


@click.group(context_settings=CONTEXT_SETTINGS)
def cli():
    """ Creates, updates, reads and deletes users and groups. """
    click.clear()
    pass


@cli.command(options_metavar=METAVAR_COMMAND,
             short_help=SHORT_HELP_CREATE_USER)
@click.option(SHORT_ARGUMENT_USERNAME, LONG_ARGUMENT_USERNAME,
              metavar=METAVAR_USERNAME, help=HELP_USERNAME, prompt=True)
@click.option(SHORT_ARGUMENT_PASSWORD, LONG_ARGUMENT_PASSWORD,
              metavar=METAVAR_PASSWORD, help=HELP_PASSWORD, prompt=True,
              hide_input=True, confirmation_prompt=True)
def create_user(username, password):
    """
    Creates a user and adds it to the yaml configuration file.
    \b
    :param username: The username of the user you'd like to add.
    :param password: The password of the user you'd like to add.
    """
    usermanager = UserManager()
    if usermanager.create_user(username, password):
        click.secho("Successfully created the user " + username,
                    fg="green", bold=True)


@cli.command(options_metavar=METAVAR_COMMAND,
             short_help=SHORT_HELP_CREATE_GROUP)
@click.option(SHORT_ARGUMENT_USERGROUP, LONG_ARGUMENT_USERGROUP,
              metavar=METAVAR_USERGROUP, help=HELP_CREATE_USERGROUP,
              prompt=True)
def create_usergroup(user_group):
    """
    Creates a usergroup and adds it to the yaml configuration file.
    \b
    :param group_name: The name of the group you'd like to add.
    """
    groupmanager = UserGroupManager()
    if groupmanager.create_group(user_group):
        click.secho("Successfully created a group with the name " +
                    user_group, fg="green", bold=True)
    else:
        click.secho("A group with the name \"" + user_group + " already "
                    "exists!", fg="red", bold=False)


@cli.command(options_metavar=METAVAR_COMMAND,
             short_help=SHORT_HELP_UPDATE_USER)
@click.option(SHORT_ARGUMENT_USERNAME, LONG_ARGUMENT_USERNAME,
              metavar=METAVAR_USERNAME, help=HELP_USERNAME, default=None)
def update_user(username):
    """
    Edit a user. The username is an optional argument. If not entered,
    the list of users will be shown to choose a user from.
    \b
    :param username: The name of the user you'd like to edit.
    """
    usermanager = UserManager()
    groupmanager = UserGroupManager()
    if username is None:
        username = select_user_from_list(usermanager)

    if username not in (username.get_username() for username in
                        usermanager.users):
        click.secho("The given user does not exist!", fg="red", bold=True)
        return

    while True:
        click.echo("What fields of this user would you like to edit?")
        click.echo(click.style("[1]", fg="cyan") + " The username")
        click.echo(click.style("[2]", fg="cyan") + " The password")
        click.echo(click.style("[3]", fg="cyan") + " All above fields")
        edit_fields = click.prompt("", type=int)
        if edit_fields in range(1, 4):
            break

    if edit_fields == 1 or edit_fields == 3:
        while True:
            new_username = click.prompt("Please type the new username "
                                        "for this user.", type=str)
            if usermanager.update_user_username(username, new_username) and \
                    groupmanager.update_user_in_usergroup(
                            username, new_username, usermanager):
                click.secho("Succesfully changed the username " + username +
                            " to " + new_username + "!", fg="green", bold=True)
                username = new_username
                break
            else:
                click.secho("There is already a user with this username!",
                            fg="red", bold=True)

    if edit_fields == 2 or edit_fields == 3:
        new_password = click.prompt("Please type the new password "
                                    "for this user.", type=str)
        if usermanager.update_user_password(username, new_password):
            click.secho("Succesfully changed the password of " + username +
                        " to " + new_password + "!", fg="green", bold=True)


def select_user_from_list(usermanager):
    """
    Shows a list of users and prompts what user to edit/delete/update
    :param usermanager: The usermanager object
    :return: Returns the username of the selected user.
    """
    if len(usermanager.users) > 0:
        print_users(usermanager)
        while True:
            username = click.prompt("Please type the name of the user "
                                    "you'd like to use.", type=str)
            if utils.parse_int(username) is None:
                if username not in (username.get_username() for username in
                                    usermanager.users):
                    click.secho("The given user does not exist!", fg="red",
                                bold=True)
                else:
                    return username
            else:
                try:
                    return usermanager.users[utils.parse_int(
                            username)-1].get_username()
                except IndexError:
                    click.secho(username + " is not a valid number!",
                                fg="red", bold=True)
    else:
        click.secho("There are no users!", fg="red", bold=True)
        exit()


def select_usergroup_from_list(groupmanager):
    """
    Shows a list of usergroups and prompts what usergroup to edit/delete/update
    :param groupmanager: The groupmanager object
    :return: Returns the name of the selected usergroup.
    """
    if len(groupmanager.user_groups) > 0:
        print_groups(groupmanager)
        while True:
            groupname = click.prompt("Please type the name of the group "
                                     "you'd like to use.", type=str)
            if utils.parse_int(groupname) is None:
                if groupname not in (usergroup.get_name() for usergroup in
                                     groupmanager.user_groups):
                    click.secho("The given usergroup does not exist!",
                                fg="red", bold=True)
                else:
                    return groupname
            else:
                try:
                    return groupmanager.user_groups[utils.parse_int(
                            groupname)-1].get_name()
                except IndexError:
                    click.secho(groupname+" is not a valid number!",
                                fg="red", bold=True)
    else:
        click.secho("There are no usergroups!", fg="red", bold=True)
        exit()


@cli.command(options_metavar=METAVAR_COMMAND,
             short_help=SHORT_HELP_ADD_USER_TO_USERGROUP)
@click.option(SHORT_ARGUMENT_USERGROUP, LONG_ARGUMENT_USERGROUP,
              metavar=METAVAR_USERGROUP, help=HELP_UPDATE_USERGROUP,
              default=None)
@click.option(SHORT_ARGUMENT_USERGROUP_NAME, LONG_ARGUMENT_USERGROUP_NAME,
              metavar=METAVAR_USERGROUP_NAME, help=HELP_USERGROUP_NAME,
              prompt=True)
def update_usergroup_name(user_group, new_name):
    """
    Adds a user to a usergroup.
    \b
    :param user_group: The name of the usergroup you'd like to add a user to.
    :param new_name: The new name of this usergroup.
    """
    groupmanager = UserGroupManager()

    if user_group is None:
        user_group = select_usergroup_from_list(groupmanager)

    if user_group in (usergroup.get_name() for usergroup in
                      groupmanager.user_groups):
        if groupmanager.update_usergroup_name(user_group, new_name):
            click.secho("The group " + user_group + " has succesfully "
                        "been renamed to " + new_name + ".", fg="green",
                        bold=True)
        else:
            click.secho("There is already a group named " + new_name + "!",
                        fg="red", bold=True)
    else:
        click.secho("There is no usergroup with the name " + user_group +
                    "!", fg="red", bold=True)


@cli.command(options_metavar=METAVAR_COMMAND,
             short_help=SHORT_HELP_ADD_USER_TO_USERGROUP)
@click.option(SHORT_ARGUMENT_USERNAME, LONG_ARGUMENT_USERNAME,
              metavar=METAVAR_USERNAME, help=HELP_USERNAME, default=None)
@click.option(SHORT_ARGUMENT_USERGROUP, LONG_ARGUMENT_USERGROUP,
              metavar=METAVAR_USERGROUP, help=HELP_UPDATE_USERGROUP,
              default=None)
def add_user_to_usergroup(username, user_group):
    """
    Adds a user to a usergroup.
    \b
    :param username: Optional. The username of the user you'd like to add to a
    usergroup.
    :param user_group: Optional. The name of the usergroup you'd like to
    add a user to.
    """
    usermanager = UserManager()
    groupmanager = UserGroupManager()

    if username is None:
        username = select_user_from_list(usermanager)

    if user_group is None:
        user_group = select_usergroup_from_list(groupmanager)

    if username in (user.get_username() for user in usermanager.users):
        for usergroup in groupmanager.user_groups:
            if usergroup.name == user_group:
                if groupmanager.add_user_to_usergroup(username, usergroup,
                                                      usermanager):
                    click.secho("The user " + username + " has succesfully "
                                "been added to the usergroup " +
                                user_group + ".", fg="green", bold=True)
                else:
                    click.secho("The user " + username + " is already in the "
                                "usergroup " + user_group + "!", fg="red",
                                bold=True)
                break
        else:
            click.secho("There is no usergroup with the name " +
                        user_group + "!", fg="red", bold=True)
    else:
        click.secho("The user " + username + " does not exist!", fg="red",
                    bold=True)


@cli.command(options_metavar=METAVAR_COMMAND,
             short_help=SHORT_HELP_ADD_GROUP_TO_USERGROUP)
@click.option(SHORT_ARGUMENT_GROUP, LONG_ARGUMENT_GROUP,
              metavar=METAVAR_GROUP, help=HELP_CREATE_GROUP, prompt=True)
@click.option(SHORT_ARGUMENT_USERGROUP, LONG_ARGUMENT_USERGROUP,
              metavar=METAVAR_USERGROUP, help=HELP_UPDATE_USERGROUP,
              default=None)
def add_group_to_usergroup(groupname, user_group):
    """
    Add a Home Assistant group to a usergroup.
    \b
    :param groupname: Required. The name of the Home Assistant group you'd
    like to add to a usergroup.
    :param user_group: Optional. The name of the usergroup you'd like to
    add a user to.
    """
    groupmanager = UserGroupManager()

    if user_group is None:
        user_group = select_usergroup_from_list(groupmanager)

    for usergroup in groupmanager.user_groups:
        if usergroup.name == user_group:
            if groupmanager.add_group_to_usergroup(groupname, usergroup):
                click.secho("The group " + groupname + " has succesfully been "
                            "added to the usergroup " + user_group + ".",
                            fg="green", bold=True)
            else:
                click.secho("The group " + groupname + " is already in the "
                            "usergroup " + user_group + "!", fg="red",
                            bold=True)
            break
    else:
        click.secho("There is no usergroup with the name " + groupname + "!",
                    fg="red", bold=True)


@cli.command(options_metavar=METAVAR_COMMAND,
             short_help=SHORT_HELP_REMOVE_USER_FROM_USERGROUP)
@click.option(SHORT_ARGUMENT_USERNAME, LONG_ARGUMENT_USERNAME,
              metavar=METAVAR_USERNAME, help=HELP_USERNAME, default=None)
@click.option(SHORT_ARGUMENT_USERGROUP, LONG_ARGUMENT_USERGROUP,
              metavar=METAVAR_USERGROUP, help=HELP_UPDATE_USERGROUP,
              default=None)
def remove_user_from_usergroup(username, user_group):
    """
    Remove a user from a usergroup.
    \b
    :param username: Optional. The username of the user you'd like to remove
    from a usergroup.
    :param user_group: Optional. The name of the usergroup you'd like to
    remove a user from.
    """
    usermanager = UserManager()
    groupmanager = UserGroupManager()

    if username is None:
        username = select_user_from_list(usermanager)

    if user_group is None:
        user_group = select_usergroup_from_list(groupmanager)

    if username in (user.get_username() for user in usermanager.users):
        for usergroup in groupmanager.user_groups:
            if usergroup.name == user_group:
                if groupmanager.remove_user_from_usergroup(username,
                                                           usergroup):
                    click.secho("The user " + username + " has succesfully "
                                "been removed from the usergroup " +
                                user_group + ".", fg="green", bold=True)
                else:
                    click.secho("The user " + username + " is not in the "
                                "usergroup " + user_group + "!", fg="red",
                                bold=True)
                break
        else:
            click.secho("There is no usergroup with the name " + user_group +
                        "!", fg="red", bold=True)
    else:
        click.secho("The user " + username + " does not exist!", fg="red",
                    bold=True)


@cli.command(options_metavar=METAVAR_COMMAND,
             short_help=SHORT_HELP_REMOVE_GROUP_FROM_USERGROUP)
@click.option(SHORT_ARGUMENT_GROUP, LONG_ARGUMENT_GROUP,
              metavar=METAVAR_GROUP, help=HELP_CREATE_GROUP, prompt=True)
@click.option(SHORT_ARGUMENT_USERGROUP, LONG_ARGUMENT_USERGROUP,
              metavar=METAVAR_USERGROUP, help=HELP_UPDATE_USERGROUP,
              default=None)
def remove_group_from_usergroup(groupname, user_group):
    """
    Remove a Home Assistant group from a usergroup.
    \b
    :param groupname: Required. The name of the Home Assistant group you'd
    like to remove from a usergroup.
    :param usergroupname: Optional. The name of the usergroup you'd like to
    remove a user from.
    """
    groupmanager = UserGroupManager()

    if user_group is None:
        user_group = select_usergroup_from_list(groupmanager)

    for usergroup in groupmanager.user_groups:
        if usergroup.name == user_group:
            if groupmanager.remove_group_from_usergroup(groupname, usergroup):
                click.secho("The group " + groupname + " has succesfully been "
                            "removed from the usergroup " + user_group + ".",
                            fg="green", bold=True)
            else:
                click.secho("The group " + groupname + " is not in the "
                            "usergroup " + user_group + "!", fg="red",
                            bold=True)
            break
    else:
        click.secho("There is no usergroup with the name " + user_group + "!",
                    fg="red", bold=True)


@cli.command(options_metavar=METAVAR_COMMAND,
             short_help=SHORT_HELP_READ_USERS)
def read_users():
    """ Prints all user's username and password. """
    usermanager = UserManager()
    for user in usermanager.users:
        click.echo("Username: " + user.get_username() +
                   " & Password: " + user.get_password())


@cli.command(options_metavar=METAVAR_COMMAND,
             short_help=SHORT_HELP_READ_USER)
@click.option(SHORT_ARGUMENT_USERNAME, LONG_ARGUMENT_USERNAME,
              metavar=METAVAR_USERNAME, help=HELP_USERNAME)
def read_user(username):
    """
    Prints the username and password of the user that matches the given
    username
    :param username: The username of which you'd like to see the username
    and password.
    """
    usermanager = UserManager()

    if username is None:
        username = select_user_from_list(usermanager)

    for user in usermanager.users:
        if username == user.get_username():
                click.echo("Username: " + user.get_username() +
                           " & Password: " + user.get_password())
                break
        else:
            click.secho("There is no user by the username: " + username,
                        fg="red", bold=True)


def print_users(usermanager):
    """
    Prints the users stored in a UserManager.
    :param usermanager: an instance of UserManager.
    """
    for i in range(len(usermanager.users)):
        click.echo(click.style("[" + str(i+1) + "] ", fg='cyan') +
                   usermanager.users[i].get_username())


@cli.command(options_metavar=METAVAR_COMMAND,
             short_help=SHORT_HELP_READ_GROUPS)
def read_groups():
    """ Prints all usergroups. """
    usergroupmanager = UserGroupManager()
    for user_group in usergroupmanager.user_groups:
        click.echo("------")
        click.echo("Name of the usergroup: " + user_group.get_name())
        click.echo("Users in this usergroup: ")
        click.echo(user_group.get_users())
        click.echo("Home Assistant groups in this usergroup: ")
        click.echo(user_group.get_groups())


@cli.command(options_metavar=METAVAR_COMMAND,
             short_help=SHORT_HELP_READ_GROUP)
@click.option(SHORT_ARGUMENT_USERGROUP, LONG_ARGUMENT_USERGROUP,
              metavar=METAVAR_USERGROUP, help=HELP_READ_USERGROUP)
def read_group(user_group):
    """ Prints a group based on the given groupname. """
    usergroupmanager = UserGroupManager()

    if user_group is None:
        user_group = select_usergroup_from_list(usergroupmanager)

    for usergroup in usergroupmanager.user_groups:
        if usergroup.get_name() == user_group:
            click.echo("------")
            click.echo("Name of the usergroup: " + usergroup.get_name())
            click.echo("Users in this usergroup: ")
            click.echo(usergroup.get_users())
            click.echo("Home Assistant groups in this usergroup: ")
            click.echo(usergroup.get_groups())
            break
        else:
            click.secho("There is no group by the groupname: " + user_group,
                        fg="red", bold=True)


def print_groups(usergroupmanager):
    """
    Prints all groups stored in a UserGroupManager.
    :param usergroupmanager: an instance of UserGroupManager.
    """
    for i in range(len(usergroupmanager.user_groups)):
        click.echo(click.style("[" + str(i+1) + "] ", fg='cyan') +
                   usergroupmanager.user_groups[i].get_name())


@cli.command(options_metavar=METAVAR_COMMAND,
             short_help=SHORT_HELP_DELETE_USER)
@click.option(SHORT_ARGUMENT_USERNAME, LONG_ARGUMENT_USERNAME,
              metavar=METAVAR_USERNAME, help=HELP_USERNAME)
def delete_user(username):
    """
    Deletes a user by given username.
    :param username: The username of the user you'd like to delete.
    """
    usermanager = UserManager()

    if username is None:
        username = select_user_from_list(usermanager)

    if click.confirm("Are you sure you want to delete the user "
                     "with username: " + username):
        if usermanager.delete_user(username):
            click.secho("Successfully deleted user with username: " +
                        username, fg="green", bold=True)


@cli.command(options_metavar=METAVAR_COMMAND,
             short_help=SHORT_HELP_DELETE_GROUP)
@click.option(SHORT_ARGUMENT_USERGROUP, LONG_ARGUMENT_USERGROUP,
              metavar=METAVAR_USERGROUP, help=HELP_DELETE_USERGROUP)
def delete_usergroup(user_group):
    """
    Deletes a group by given usergroup name.
    :param groupname: The name of the usergroup you'd like to delete.
    """
    groupmanager = UserGroupManager()

    if user_group is None:
        user_group = select_usergroup_from_list(groupmanager)

    if click.confirm("Are you sure you want to delete the usergroup"
                     " with name: " + user_group):
        if groupmanager.delete_usergroup(user_group):
            click.secho("Successfully deleted the group with name: " +
                        user_group, fg="green", bold=True)
        else:
            click.secho("The usergroup "+user_group+" does not exist!",
                        fg="red", bold=True)
