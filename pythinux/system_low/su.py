if args == ["--help"]:
    main(currentUser,"man su")
else:
    if currentUser.group.canSudo:
        if sudo(currentUser):
            g = groupList.byName("root")
            u = User(g, currentUser.username,currentUser.password)
            tty = getTerm()
            main(u,tty)
        else:
            print("ERROR: Failed to authenticate.")
    else:
        print("ERROR: Insifficient priveleges. Contact your sysadmin.")