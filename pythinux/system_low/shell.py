import traceback
def terminal(user, manager):
    cmd = input("{}@{} $".format(user.group.name, user.username))
    if cmd == "ps":
        pids = manager.list()
        print("PID\tNAME\t\tRUNNING")
        for x in pids:
            running = pids[x]["running"]
            running = running if running is not None else "Unknown"
            print("{}\t{}\t\t{}".format(x, pids[x]["name"],running))
    elif cmd == "":
        pass
    elif cmd in ["quit", "exit"]:
        return
    else:
        try:
            main(user, cmd)
        except Exception as e:
            print(traceback.format_exc())
    terminal(user, manager)

print("ERROR: Cannot launch `shell` directly.")
