User = User
if args == ["list"]:
    for item in userList.list():
        if not item.hidden:
            div()
            print(f"Username: {item.username}")
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
        u = User(g, args[1],args[2])
        userList = createUser(userList,u)
        saveUserList(userList)
    else:
        print("ERROR: Invalid group name.")
        print("       For a list, run `group list`.")
elif args == ["remove"]:
    div()
    print("user remove <user>")
    div()
    print("Removes <user> from system.")
    div()
elif "remove" in args and len(args) == 2:
    if userList.removeByName(args[1]):
        print("Successfully removed {}.".format(args[1]))
    else:
        print("Invalid User:  {}".format(args[1]))
elif args == ["info"]:
    div()
    print("user info <username>")
    div()
    print("Lists info about a user.")
    div()
elif "info" in args and len(args) == 2:
    u = userList.byName(args[1])
    div()
    print("Username: {}".format(u.username))
    print("Password: {}".format(u.password))
    print("Group: {}".format(u.group.name))
    print("Hidden: {}".format("Yes" if u.hidden else "No"))
    div()
else:
    div()
    print("user [args]")
    print("Program for creating and managing users.")
    div()
    print("Arguments:")
    print("    add: adds a user")
    print("    list: lists all users")
    print("    remove: removes a user")
    div()
