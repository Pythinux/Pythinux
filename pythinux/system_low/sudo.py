import getpass
import time

var = load_program("var", currentUser, libMode=True)

def confirmPassword(user, max=10, attempt=1):
    """
    Asks the user to enter their password. Returns True if successful.
    After `max` failed attempts, returns False.
    """
    password = getpass.getpass("[sudo] password for {}: ".format(user.username))
    if user.check(user.username, password):
        return True
    if attempt >= max:
        return False
    else:
        print("ERROR: Incorrect password.")
        return confirmPassword(user, max, attempt+1)

def sudo(user, command, max=10):
    """
    Run a command as root, provided the user in question has sufficient privileges.
    """
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

    if not verifyUser(user):
        raise PythinuxError("User is not an instance of User")
    if user.group.canSudo:
        if confirmPassword(user, max):
            rootUser = userList.byName("root")
            if not rootUser:
                if input("ERROR: No root user exists. Would you like me to create one for you? [y/N]").lower() == "y":
                    createRootUser()
                return
            runCommand(rootUser, command)
        else:
            print("ERROR: Identity confirmation failed.")
    else:
        print("ERROR: This group has insufficient permissions to run sudo.")
def main(args):
    if args:
        cmd = " ".join(args)
        sudo(currentUser, cmd, var.getint("SUDO_MAX_ATTEMPTS", fallback=10))
    else:
        div()
        print("sudo <command>")
        div()
        print("Run a command as root.")
        div()
