def terminal(user, manager):
    cmd = input("{}@{} $".format(user.group.name, user.username))
    if cmd == "ps":
        pids = manager.list()
        print("PID\tNAME")
        for x in pids:
            print("{}\t{}".format(x, pids[x]))
    elif cmd in ["quit", "exit"]:
        return
    else:
        main(user, cmd)
    terminal(user, manager)
