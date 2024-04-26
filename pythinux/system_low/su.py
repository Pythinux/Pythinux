import getpass
shell = load_program("shell", currentUser, libMode=True)
var = load_program("var", currentUser, libMode=True)
sudo = load_program("sudo", currentUser, libMode=True)

def main(args):
    if currentUser.group.canSudo:
        if sudo.confirmPassword(currentUser):
            rootGroup = groupList.byName("root")
            rootUser = User(rootGroup, currentUser.username, currentUser.password)
            shell.terminal(rootUser)
        else:
            print("ERROR: Identity confirmation failed.")
    else:
        print("ERROR: Your group does not have the permission to run this command.")
