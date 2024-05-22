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
