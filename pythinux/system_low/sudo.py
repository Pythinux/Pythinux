if args:
    args = " ".join(args)
    if currentUser.group.canSudo:
        if sudo(currentUser):
            g = groupList.byName("root")
            u = User(g,currentUser.username, currentUser.password)
            main(u,args)
        else:
            print("ERROR: Failed to authenticate.")
            print("Please try again.")
    else:
        print("ERROR: The current user does not have sudo priveleges.")
        print("Contact your sysadmin.")
else:
    div()
    print("sudo <command>")
    div()
    print("Runs a command as a root user, with the same username and password as the current one.")
    print("The current user requires sudo priveleges.")
    print("Can you run sudo: {}".format("Yes" if currentUser.group.canSudo else "No"))
    div()