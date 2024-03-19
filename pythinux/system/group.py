def main(args):
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
        gr = groupList.byName(args[1])
        if not gr:
            print("ERROR: Invalid group.")
        elif gr.locked:
            print("ERROR: Group is locked.")
        else:
            print("Removing users in group...")

            print("Deleting group...")
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
        group = groupList.byName(args[1])
        if group:
            div()
            print("BASIC INFO")
            div()
            print("Name:       {}".format(group.name))
            print("Locked:     {}".format(group.locked))
            div()
            print("PERMISSIONS")
            div()
            print("CanApp:     {}".format(group.canApp))
            print("CanAppHigh: {}".format(group.canAppHigh))
            print("CanSys:     {}".format(group.canSys))
            print("CanSysHigh: {}".format(group.canSysHigh))
            print("CanSudo:    {}".format(group.canSudo))
            div()
        else:
            print("ERROR: Invalid group.")
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
