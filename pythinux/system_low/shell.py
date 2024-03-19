import traceback

def run(user, cmd, shell="shell"):
    if cmd == "":
        pass
    elif cmd in ["quit", "exit"]:
        return
    else:
        runCommand(user, cmd, shell=shell)


def terminal(user):
    cmd = input("{}@{} $".format(user.group.name, user.username))
    run(user, cmd)
    terminal(user)

def runScript(user, filename):
    with open(filename) as f:
        for cmd in f.read():
            run(user, cmd, "script")
def main(args):
    if args:
        for arg in args:
            runScript(currentUser, arg)
    else:
        div()
        print("shell <script_name.xx>")
        div()
        print("Runs a shell script.")
        div()
