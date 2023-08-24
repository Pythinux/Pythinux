if args == ["add"]:
    div()
    print("group add <name> <canApp> <canAppHigh> <canSys> <canSysHigh> <canSudo>")
    div()
    print("Creates a group to add users to.")
    print("")
elif "add" in args and len(args) == 7:
    name = args[1]
    canApp = bool(doCalc(args[2]))
    canAppHigh = bool(doCalc(args[3]))
    canSys = bool(doCalc(args[4]))
    canSysHigh = bool(doCalc(args[5]))
    canSudo = bool(doCalc(args[6]))
    g = Group(name,canApp,canAppHigh,canSys,canSysHigh, canSudo)
    pprint(g)
elif args == ["remove"]:
    div()
    print("group remove <name>")
    div()
    print("Remove a group (and all of its users).")
    div()
elif "remove" in args and len(args) == 2:
    print("Removing users in group...")
    for user in userList.list():
        if user.group.name == args[1]:
            removeUser(userList,user)
            print("Removed '{}'.".format(user.username))
    print("Deleting group...")
    gr = groupList.byName(args[1])
    groupList.remove(gr)
    saveGroupList(groupList)
    saveUserList(userList)
    print("Successfully removed '{}'.".format(args[1]))
elif args == ["info"]:
    div()
    print("group info <name>")
    div()
    print("Prints info about a group.")
    div()
elif "info" in args and len(args) == 2:
    gr = groupList.byName(args[1])
    pprint(gr)
elif args == ["list"]:
    div()
    for item in groupList.list():
        print(item.name)
    div()
else:
    div()
    print("group [args]")
    div()
    print("Create, view and edit user groups.")
    div()
    print("Positional Arguments:")
    print("    add: add a group")
    print("    remove: remove a group (potentially dangerous)")
    print("    info: info about a group")
    print("    list: list of groups")
    div()