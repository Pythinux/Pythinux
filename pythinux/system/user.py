import warnings

class UserError(PythinuxError):
    pass


def listUsers():
    for user in userList.list():
        div()
        print("Username: {} {}".format(user.username, "(Disabled)" if user.disabled else ""))
        print("Password: {}".format(user.password))
        print("Group: {}".format(user.group.name))
    div()


def addUser(username, group_name):
    group = groupList.byName(group_name)
    if not group:
        raise UserError("Invalid group.")
    user = User(group, username)
    userList = createUser(loadUserList(), user)
    saveUserList(userList)
    warnings.warn("Changes will only apply after restarting Pythinux")


def removeUser(username):
    user = userList.byName(username)
    if not user:
        raise UserError("Invalid user")
    if user.locked:
        raise UserError("Cannot remove locked user")
    userList.remove(user)
    saveUserList(userList)
    warnings.warn("Changes will only apply after restarting Pythinux")


def disableUser(username):
    user = userList.byName(username)
    user.disabled = True
    user.password = ""
    saveUserList(userList)


def enableUser(username):
    user = userList.byName(username)
    user.disabled = False
    saveUserList(userList)
    runCommand(user, "passwd")
    saveUserList(userList)

def main(args):
    userList = loadUserList()
    if args == ["list"]:
        listUsers()
    elif args == ["add"]:
        div()
        print("user add <username> <group_name>")
        div()
        print("Creates a user with no password.")
        div()
    elif "add" in args and len(args) == 3:
        args.remove("add")
        addUser(args[0], args[1])
    elif args == ["remove"]:
        div()
        print("user remove <user>")
        div()
        print("Removes <user> from system.")
        div()
    elif "remove" in args and len(args) == 2:
        args.remove("remove")
        removeUser(args[0])
    elif args == ["disable"]:
        div()
        print("user disable <username>")
        div()
        print("Disable a user.")
        div()
    elif "disable" in args and len(args) == 2:
        args.remove("disable")
        disableUser(args[0])
    elif args == ["enable"]:
        div()
        print("user enable <username>")
        div()
        print("Enable a user.")
        div()
    elif "enable" in args and len(args) == 2:
        args.remove("enable")
        enableUser(args[0])
    else:
        div()
        print("user [args]")
        print("Program for creating and managing users.")
        div()
        print("Arguments:")
        print("    add: adds a user")
        print("    list: lists all users")
        print("    remove: removes a user")
        print("    disable: disable a user")
        print("    enable: enable a user")
        div()
