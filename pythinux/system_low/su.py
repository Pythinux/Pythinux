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

import getpass
shell = load_program("shell", currentUser, libMode=True)
var = load_program("var", currentUser, libMode=True)
sudo = load_program("sudo", currentUser, libMode=True)

def main(args):
    def createRootUser():
        """
        This function is inside main() to hide it from API access.
        """
        def createRootGroup():
            rootGroup = Group("root", True, True, True, locked=True)
            groupList.add(rootGroup)
        rootGroup = groupList.byName("root")
        if not rootGroup:
            if input("ERROR: No root group exists. Would you like me to create one for you? [y/N] $").lower() == "y":
                createRootGroup()
            else:
                print("ERROR: No root user was created.")
            return
        rootUser = User(rootGroup, "root", locked=True, disabled=True)
        createUser(userList, rootUser)

    if currentUser.group.canSudo:
        if sudo.confirmPassword(currentUser):
            rootUser = userList.byName("root")
            if not rootUser:
                if input("ERROR: No root user exists. Would you like me to create one for you? [y/N] $").lower() == "y":
                    createRootUser()
                return
            shell.terminal(rootUser)
        else:
            print("ERROR: Identity confirmation failed.")
    else:
        print("ERROR: Your group does not have the permission to run this command.")
