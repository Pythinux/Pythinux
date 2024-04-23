import getpass
shell = load_program("shell", currentUser, libMode=True)
var = load_program("var", currentUser, libMode=True)

def main(args):
    if currentUser.group.canSudo:
        passwd = getpass.getpass("Password $")
        if verifyHash(passwd, currentUser.password):
            rootUser = loadUserList().byName("root")
            if rootUser:
                allow_cls = var.getbool("SHELL_ALLOW_EXIT", False)
                var.set("SHELL_ALLOW_EXIT", "true")
                shell.terminal(rootUser)
                var.set("SHELL_ALLOW_EXIT", allow_cls)
            else:
                print("ERROR: `root` is not a valid user.")
        else:
            print("ERROR: Invalid password.")
    else:
        print("ERROR: Insufficient priveleges.")
