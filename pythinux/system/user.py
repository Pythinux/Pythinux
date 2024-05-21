def main(args):
    userList = loadUserList()
    if args == ["list"]:
        for item in userList.list():
            div()
            print(f"Username: {item.username} {'(Disabled)' if item.disabled else ''}")
            print(f"Password: {item.password}")
            print(f"Group: {item.group.name}")
        div()
    elif args == ["add"]:
        div()
        print("user add <username> <password> <group_name>")
        div()
        print("For a list of groups:")
        print("group list")
        div()
    elif "add" in args and len(args) == 4:
        gl = loadGroupList()
        g = gl.byName(args[3])
        if g:
            u = User(g, args[1],hashString(args[2]))
            userList = createUser(userList,u)
            saveUserList(userList)
        else:
            print("ERROR: Invalid group name. For a list, run `group list`.")
    elif args == ["remove"]:
        div()
        print("user remove <user>")
        div()
        print("Removes <user> from system.")
        div()
    elif "remove" in args and len(args) == 2:
        args.remove("remove")
        try:
            user = userList.byName(args[0])
        except PythinuxError:
            print("ERROR: Invalid user.")
            return
        if user.locked:
            print("ERROR: User is locked.")
            return
        userList.removeByName(user.username)
        saveUserList(userList)
        print("Successfully removed user.")
    elif args == ["info"]:
        div()
        print("user info <username>")
        div()
        print("Lists info about a user.")
        div()
    elif "info" in args and len(args) == 2:
        u = userList.byName(args[1])
        pprint(u)
    elif args == ["disable"]:
        div()
        print("user disable <username>")
        div()
        print("Disable a user.")
        div()
    elif "disable" in args and len(args) == 2:
        args.remove("disable")
        user = userList.byName(args[0])
        user.disabled = True
        user.password = ""
        saveUserList(userList)
    elif args == ["enable"]:
        div()
        print("user enable <username>")
        div()
        print("Enable a user.")
        div()
    elif "enable" in args and len(args) == 2:
        args.remove("enable")
        user = userList.byName(args[0])
        user.disabled = False
        runCommand(user, "passwd")
        saveUserList(userList)
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
