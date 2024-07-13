"""
██████╗ ██╗   ██╗████████╗██╗  ██╗██╗███╗   ██╗██╗   ██╗██╗  ██╗
██╔══██╗╚██╗ ██╔╝╚══██╔══╝██║  ██║██║████╗  ██║██║   ██║╚██╗██╔╝
██████╔╝ ╚████╔╝    ██║   ███████║██║██╔██╗ ██║██║   ██║ ╚███╔╝ 
██╔═══╝   ╚██╔╝     ██║   ██╔══██║██║██║╚██╗██║██║   ██║ ██╔██╗ 
██║        ██║      ██║   ██║  ██║██║██║ ╚████║╚██████╔╝██╔╝ ██╗
╚═╝        ╚═╝      ╚═╝   ╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚═╝  ╚═╝

Copyright (C) 2024 Pythinux Team

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
"""
class GroupError(PythinuxError):
    pass

def listGroups():
    div()
    for group in groupList.list():
        print(group.name)
    div()

def showGroupInfo(group_name):
    assertTrue(isinstance(group_name, str))
    group = groupList.byName(group_name)
    if not group:
        raise GroupError("Invalid group")
    div()
    print("BASIC INFO")
    div()
    print("Name:       {}".format(group.name))
    print("Locked:     {}".format(group.locked))
    div()
    print("PERMISSIONS")
    div()
    print("canApp:     {}".format(group.canApp))
    print("canAppHigh: {}".format(group.canAppHigh))
    print("canSys:     {}".format(group.canSys))
    print("canSudo:    {}".format(group.canSudo))
    div()

def setPermission(group_name, permission, value):
    assertTrue(isinstance(group_name, str))
    assertTrue(isinstance(permission, str))
    assertTrue(isinstance(value, bool))
    if permission not in ["canApp", "canAppHigh", "canSys", "canSudo"]:
        raise GroupError("Invalid permission name")
    group = groupList.byName(group_name)
    if not group:
        raise GroupError("Invalid group")

    setattr(group, permission, value)
    saveGroupList(groupList)

def main(args):
    if "-v" in args:
        args.remove("-v")
        verbose = True
    else:
        verbose = False

    if args == ["add"]:
        div()
        print("group add <name> <canApp> <canAppHigh> <canSys> <canSudo>")
        div()
        print("Creates a group to add users to.")
        print("")
    elif "add" in args and len(args) == 6:
        name = args[1]
        canApp = bool(doCalc(args[2]))
        canAppHigh = bool(doCalc(args[3]))
        canSys = bool(doCalc(args[4]))
        canSudo = bool(doCalc(args[5]))
        g = Group(name,canApp,canAppHigh,canSys, canSudo)
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
        args.remove("info")
        showGroupInfo(args[0])
    elif args == ["list"]:
        listGroups()
    elif args == ["set"]:
        div()
        print("group set <group name> <permisison> <true|false>")
        div()
        print("Edits permissions for groups.")
        div()
    elif "set" in args and len(args) == 4:
        args.remove("set")
        group_name, permission, value = args[0], args[1], True if args[2] in ["True", "true", "1"] else False
        setPermission(group_name, permission, value)
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
        print("    set: edit permissions for groups")
        div()
