import getpass
def sudo(user, password, command):
    """
    Runs a command as administrator.
    """

    if not user.group.canSudo:
        return "ERROR: The {} group is disallowed from running sudo.".format(user.group.name)

    if password != user.password:
        return "ERROR: Invalid authentication provided."

    rootGroup = loadGroupList().byName("root")
    rootUser = User(rootGroup, "root")
    runCommand(rootUser, command, shell="sudo")

def main(args):
    if args:
        cmd = " ".join(args)
        passwd = getpass.getpass("[sudo] Password for {}: ".format(user.name))
        sudo(currentUser, )
    else:
        div()
        print("sudo <command>")
        div()
        print("Run a command as root.")
        div()
