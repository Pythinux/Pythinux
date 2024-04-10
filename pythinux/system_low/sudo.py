import getpass
def sudo(user, command):
    if user.group.canSudo:
        if pythinux.sudo(user):
            group = groupList.byName("root")
            runCommand(User(group, "root", ""), command)
def main(args):
    if args:
        cmd = " ".join(args)
        sudo(currentUser, cmd)
    else:
        div()
        print("sudo <command>")
        div()
        print("Run a command as root.")
        div()
